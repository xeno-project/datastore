# Copyright 2017, Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import threading
import time

import mock
import pytest

import google.api_core.exceptions
from google.auth import credentials
from google.cloud.pubsub_v1 import publisher
from google.cloud.pubsub_v1 import types
from google.cloud.pubsub_v1.publisher import exceptions
from google.cloud.pubsub_v1.publisher._batch.base import BatchStatus
from google.cloud.pubsub_v1.publisher._batch import thread
from google.cloud.pubsub_v1.publisher._batch.thread import Batch


def create_client():
    creds = mock.Mock(spec=credentials.Credentials)
    return publisher.Client(credentials=creds)


def create_batch(autocommit=False, topic="topic_name", **batch_settings):
    """Return a batch object suitable for testing.

    Args:
        autocommit (bool): Whether the batch should commit after
            ``max_latency`` seconds. By default, this is ``False``
            for unit testing.
        topic (str): The name of the topic the batch should publish
            the messages to.
        batch_settings (dict): Arguments passed on to the
            :class:``~.pubsub_v1.types.BatchSettings`` constructor.

    Returns:
        ~.pubsub_v1.publisher.batch.thread.Batch: A batch object.
    """
    client = create_client()
    settings = types.BatchSettings(**batch_settings)
    return Batch(client, topic, settings, autocommit=autocommit)


def test_init():
    """Establish that a monitor thread is usually created on init."""
    client = create_client()

    # Do not actually create a thread, but do verify that one was created;
    # it should be running the batch's "monitor" method (which commits the
    # batch once time elapses).
    with mock.patch.object(threading, "Thread", autospec=True) as Thread:
        batch = Batch(client, "topic_name", types.BatchSettings())
        Thread.assert_called_once_with(
            name="Thread-MonitorBatchPublisher", target=batch.monitor
        )

    # New batches start able to accept messages by default.
    assert batch.status == BatchStatus.ACCEPTING_MESSAGES


def test_init_infinite_latency():
    batch = create_batch(max_latency=float("inf"))
    assert batch._thread is None


@mock.patch.object(threading, "Lock")
def test_make_lock(Lock):
    lock = Batch.make_lock()
    assert lock is Lock.return_value
    Lock.assert_called_once_with()


def test_client():
    client = create_client()
    settings = types.BatchSettings()
    batch = Batch(client, "topic_name", settings, autocommit=False)
    assert batch.client is client


def test_commit():
    batch = create_batch()
    with mock.patch.object(threading, "Thread", autospec=True) as Thread:
        batch.commit()

        # A thread should have been created to do the actual commit.
        Thread.assert_called_once_with(
            name="Thread-CommitBatchPublisher", target=batch._commit
        )
        Thread.return_value.start.assert_called_once_with()

    # The batch's status needs to be something other than "accepting messages",
    # since the commit started.
    assert batch.status != BatchStatus.ACCEPTING_MESSAGES
    assert batch.status == BatchStatus.STARTING


def test_commit_no_op():
    batch = create_batch()
    batch._status = BatchStatus.IN_PROGRESS
    with mock.patch.object(threading, "Thread", autospec=True) as Thread:
        batch.commit()

    # Make sure a thread was not created.
    Thread.assert_not_called()

    # Check that batch status is unchanged.
    assert batch.status == BatchStatus.IN_PROGRESS


def test_blocking__commit():
    batch = create_batch()
    futures = (
        batch.publish({"data": b"This is my message."}),
        batch.publish({"data": b"This is another message."}),
    )

    # Set up the underlying API publish method to return a PublishResponse.
    publish_response = types.PublishResponse(message_ids=["a", "b"])
    patch = mock.patch.object(
        type(batch.client.api), "publish", return_value=publish_response
    )
    with patch as publish:
        batch._commit()

    # Establish that the underlying API call was made with expected
    # arguments.
    publish.assert_called_once_with(
        "topic_name",
        [
            types.PubsubMessage(data=b"This is my message."),
            types.PubsubMessage(data=b"This is another message."),
        ],
    )

    # Establish that all of the futures are done, and that they have the
    # expected values.
    assert futures[0].done()
    assert futures[0].result() == "a"
    assert futures[1].done()
    assert futures[1].result() == "b"


def test_client_api_publish_not_blocking_additional_publish_calls():
    batch = create_batch(max_messages=1)
    api_publish_called = threading.Event()

    def api_publish_delay(_, messages):
        api_publish_called.set()
        time.sleep(1.0)
        message_ids = [str(i) for i in range(len(messages))]
        return types.PublishResponse(message_ids=message_ids)

    api_publish_patch = mock.patch.object(
        type(batch.client.api), "publish", side_effect=api_publish_delay
    )

    with api_publish_patch:
        batch.publish({"data": b"first message"})

        start = datetime.datetime.now()
        event_set = api_publish_called.wait(timeout=1.0)
        if not event_set:
            pytest.fail("API publish was not called in time")
        batch.publish({"data": b"second message"})
        end = datetime.datetime.now()

    # While a batch commit in progress, waiting for the API publish call to
    # complete should not unnecessariliy delay other calls to batch.publish().
    assert (end - start).total_seconds() < 1.0


@mock.patch.object(thread, "_LOGGER")
def test_blocking__commit_starting(_LOGGER):
    batch = create_batch()
    batch._status = BatchStatus.STARTING

    batch._commit()
    assert batch._status == BatchStatus.SUCCESS

    _LOGGER.debug.assert_called_once_with("No messages to publish, exiting commit")


@mock.patch.object(thread, "_LOGGER")
def test_blocking__commit_already_started(_LOGGER):
    batch = create_batch()
    batch._status = BatchStatus.IN_PROGRESS

    batch._commit()
    assert batch._status == BatchStatus.IN_PROGRESS

    _LOGGER.debug.assert_called_once_with(
        "Batch is already in progress, exiting commit"
    )


def test_blocking__commit_no_messages():
    batch = create_batch()
    with mock.patch.object(type(batch.client.api), "publish") as publish:
        batch._commit()

    assert publish.call_count == 0


def test_blocking__commit_wrong_messageid_length():
    batch = create_batch()
    futures = (
        batch.publish({"data": b"blah blah blah"}),
        batch.publish({"data": b"blah blah blah blah"}),
    )

    # Set up a PublishResponse that only returns one message ID.
    publish_response = types.PublishResponse(message_ids=["a"])
    patch = mock.patch.object(
        type(batch.client.api), "publish", return_value=publish_response
    )

    with patch:
        batch._commit()

    for future in futures:
        assert future.done()
        assert isinstance(future.exception(), exceptions.PublishError)


def test_block__commmit_api_error():
    batch = create_batch()
    futures = (
        batch.publish({"data": b"blah blah blah"}),
        batch.publish({"data": b"blah blah blah blah"}),
    )

    # Make the API throw an error when publishing.
    error = google.api_core.exceptions.InternalServerError("uh oh")
    patch = mock.patch.object(type(batch.client.api), "publish", side_effect=error)

    with patch:
        batch._commit()

    for future in futures:
        assert future.done()
        assert future.exception() == error


def test_block__commmit_retry_error():
    batch = create_batch()
    futures = (
        batch.publish({"data": b"blah blah blah"}),
        batch.publish({"data": b"blah blah blah blah"}),
    )

    # Make the API throw an error when publishing.
    error = google.api_core.exceptions.RetryError("uh oh", None)
    patch = mock.patch.object(type(batch.client.api), "publish", side_effect=error)

    with patch:
        batch._commit()

    for future in futures:
        assert future.done()
        assert future.exception() == error


def test_monitor():
    batch = create_batch(max_latency=5.0)
    with mock.patch.object(time, "sleep") as sleep:
        with mock.patch.object(type(batch), "_commit") as _commit:
            batch.monitor()

    # The monitor should have waited the given latency.
    sleep.assert_called_once_with(5.0)

    # Since `monitor` runs in its own thread, it should call
    # the blocking commit implementation.
    _commit.assert_called_once_with()


def test_monitor_already_committed():
    batch = create_batch(max_latency=5.0)
    status = "something else"
    batch._status = status
    with mock.patch.object(time, "sleep") as sleep:
        batch.monitor()

    # The monitor should have waited the given latency.
    sleep.assert_called_once_with(5.0)

    # The status should not have changed.
    assert batch._status == status


def test_publish_updating_batch_size():
    batch = create_batch(topic="topic_foo")
    messages = (
        types.PubsubMessage(data=b"foobarbaz"),
        types.PubsubMessage(data=b"spameggs"),
        types.PubsubMessage(data=b"1335020400"),
    )

    # Publish each of the messages, which should save them to the batch.
    futures = [batch.publish(message) for message in messages]

    # There should be three messages on the batch, and three futures.
    assert len(batch.messages) == 3
    assert batch._futures == futures

    # The size should have been incremented by the sum of the size
    # contributions of each message to the PublishRequest.
    base_request_size = types.PublishRequest(topic="topic_foo").ByteSize()
    expected_request_size = base_request_size + sum(
        types.PublishRequest(messages=[msg]).ByteSize() for msg in messages
    )

    assert batch.size == expected_request_size
    assert batch.size > 0  # I do not always trust protobuf.


def test_publish_not_will_accept():
    batch = create_batch(topic="topic_foo", max_messages=0)
    base_request_size = types.PublishRequest(topic="topic_foo").ByteSize()

    # Publish the message.
    message = types.PubsubMessage(data=b"foobarbaz")
    future = batch.publish(message)

    assert future is None
    assert batch.size == base_request_size
    assert batch.messages == []
    assert batch._futures == []


def test_publish_exceed_max_messages():
    max_messages = 4
    batch = create_batch(max_messages=max_messages)
    messages = (
        types.PubsubMessage(data=b"foobarbaz"),
        types.PubsubMessage(data=b"spameggs"),
        types.PubsubMessage(data=b"1335020400"),
    )

    # Publish each of the messages, which should save them to the batch.
    with mock.patch.object(batch, "commit") as commit:
        futures = [batch.publish(message) for message in messages]
        assert batch._futures == futures
        assert len(futures) == max_messages - 1

        # Commit should not yet have been called.
        assert commit.call_count == 0

        # When a fourth message is published, commit should be called.
        # No future will be returned in this case.
        future = batch.publish(types.PubsubMessage(data=b"last one"))
        commit.assert_called_once_with()

        assert future is None
        assert batch._futures == futures


@mock.patch.object(thread, "_SERVER_PUBLISH_MAX_BYTES", 1000)
def test_publish_single_message_size_exceeds_server_size_limit():
    batch = create_batch(
        topic="topic_foo",
        max_messages=1000,
        max_bytes=1000 * 1000,  # way larger than (mocked) server side limit
    )

    big_message = types.PubsubMessage(data=b"x" * 984)

    request_size = types.PublishRequest(
        topic="topic_foo", messages=[big_message]
    ).ByteSize()
    assert request_size == 1001  # sanity check, just above the (mocked) server limit

    with pytest.raises(exceptions.MessageTooLargeError):
        batch.publish(big_message)


@mock.patch.object(thread, "_SERVER_PUBLISH_MAX_BYTES", 1000)
def test_publish_total_messages_size_exceeds_server_size_limit():
    batch = create_batch(topic="topic_foo", max_messages=10, max_bytes=1500)

    messages = (
        types.PubsubMessage(data=b"x" * 500),
        types.PubsubMessage(data=b"x" * 600),
    )

    # Sanity check - request size is still below BatchSettings.max_bytes,
    # but it exceeds the server-side size limit.
    request_size = types.PublishRequest(topic="topic_foo", messages=messages).ByteSize()
    assert 1000 < request_size < 1500

    with mock.patch.object(batch, "commit") as fake_commit:
        batch.publish(messages[0])
        batch.publish(messages[1])

    # The server side limit should kick in and cause a commit.
    fake_commit.assert_called_once()


def test_publish_dict():
    batch = create_batch()
    future = batch.publish({"data": b"foobarbaz", "attributes": {"spam": "eggs"}})

    # There should be one message on the batch.
    expected_message = types.PubsubMessage(
        data=b"foobarbaz", attributes={"spam": "eggs"}
    )
    assert batch.messages == [expected_message]
    assert batch._futures == [future]
