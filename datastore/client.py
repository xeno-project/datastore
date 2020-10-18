# Copyright 2014 Google LLC
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
#
# Modifications copyright 2020 Andreas H. Kelch
#  - removed google dependency
#

from .key import Key
from .entity import Entity
from .transaction import Transaction
from .batch import Batch
from .query import Query

class LIFO(object):
	def __init__(self):
		self._stack = []

	def __iter__(self):
		return iter(reversed(self._stack))

	def push(self, resource):
		self._stack.append(resource)

	def pop(self):
		return self._stack.pop()

	@property
	def top(self):
		if self._stack:
			return self._stack[-1]


class Client(object):
	def __init__(
		self,
		project=None,
		namespace=None,
		credentials=None,
		client_info=None,
		client_options=None,
		_http=None,
		_use_grpc=None,
	):
		self.project = project
		self.namespace = namespace
		self.credentials = credentials

		self._batch_stack = LIFO()

		from viur.xeno.databases import dbinterface
		dbinterface.connect()

	def _push_batch(self, batch):
		"""Push a batch/transaction onto our stack.

		"Protected", intended for use by batch / transaction context mgrs.

		:type batch: :class:`google.cloud.datastore.batch.Batch`, or an object
					 implementing its API.
		:param batch: newly-active batch/transaction.
		"""
		self._batch_stack.push(batch)

	def _pop_batch(self):
		"""Pop a batch/transaction from our stack.

		"Protected", intended for use by batch / transaction context mgrs.

		:raises: IndexError if the stack is empty.
		:rtype: :class:`google.cloud.datastore.batch.Batch`, or an object
				 implementing its API.
		:returns: the top-most batch/transaction, after removing it.
		"""
		return self._batch_stack.pop()

	@property
	def current_batch(self):
		"""Currently-active batch.

		:rtype: :class:`google.cloud.datastore.batch.Batch`, or an object
				implementing its API, or ``NoneType`` (if no batch is active).
		:returns: The batch/transaction at the top of the batch stack.
		"""
		return self._batch_stack.top

	@property
	def current_transaction(self):
		"""Currently-active transaction.

		:rtype: :class:`google.cloud.datastore.transaction.Transaction`, or an
				object implementing its API, or ``NoneType`` (if no transaction
				is active).
		:returns: The transaction at the top of the batch stack.
		"""
		if isinstance(self.current_batch, Transaction):
			return self.current_batch
		return None

	def get(self, key, missing=None, deferred=None, transaction=None, eventual=False):
		"""Retrieve an entity from a single key (if it exists).

		.. note::

		   This is just a thin wrapper over :meth:`get_multi`.
		   The backend API does not make a distinction between a single key or
		   multiple keys in a lookup request.

		:type key: :class:`google.cloud.datastore.key.Key`
		:param key: The key to be retrieved from the datastore.

		:type missing: list
		:param missing: (Optional) If a list is passed, the key-only entities
						returned by the backend as "missing" will be copied
						into it.

		:type deferred: list
		:param deferred: (Optional) If a list is passed, the keys returned
						 by the backend as "deferred" will be copied into it.

		:type transaction:
			:class:`~google.cloud.datastore.transaction.Transaction`
		:param transaction: (Optional) Transaction to use for read consistency.
							If not passed, uses current transaction, if set.

		:type eventual: bool
		:param eventual: (Optional) Defaults to strongly consistent (False).
						 Setting True will use eventual consistency, but cannot
						 be used inside a transaction or will raise ValueError.

		:rtype: :class:`google.cloud.datastore.entity.Entity` or ``NoneType``
		:returns: The requested entity if it exists.

		:raises: :class:`ValueError` if eventual is True and in a transaction.
		"""
		entities = self.get_multi(
			keys=[key],
			missing=missing,
			deferred=deferred,
			transaction=transaction,
			eventual=eventual,
		)
		if entities:
			return entities[0]

	def get_multi(
		self, keys, missing=None, deferred=None, transaction=None, eventual=False
	):
		"""Retrieve entities, along with their attributes.

		:type keys: list of :class:`google.cloud.datastore.key.Key`
		:param keys: The keys to be retrieved from the datastore.

		:type missing: list
		:param missing: (Optional) If a list is passed, the key-only entities
						returned by the backend as "missing" will be copied
						into it. If the list is not empty, an error will occur.

		:type deferred: list
		:param deferred: (Optional) If a list is passed, the keys returned
						 by the backend as "deferred" will be copied into it.
						 If the list is not empty, an error will occur.

		:type transaction:
			:class:`~google.cloud.datastore.transaction.Transaction`
		:param transaction: (Optional) Transaction to use for read consistency.
							If not passed, uses current transaction, if set.

		:type eventual: bool
		:param eventual: (Optional) Defaults to strongly consistent (False).
						 Setting True will use eventual consistency, but cannot
						 be used inside a transaction or will raise ValueError.

		:rtype: list of :class:`google.cloud.datastore.entity.Entity`
		:returns: The requested entities.
		:raises: :class:`ValueError` if one or more of ``keys`` has a project
				 which does not match our project.
		:raises: :class:`ValueError` if eventual is True and in a transaction.
		"""
		if not keys:
			return []

		keys = [ Key(*key) if isinstance(key,tuple) else key for key in keys]

		ids = set(key.project for key in keys)
		for current_id in ids:
			if current_id != self.project:
				raise ValueError("Keys do not match project")

		if transaction is None:
			transaction = self.current_transaction

		from viur.xeno.databases import dbinterface
		entities = dbinterface.get_multi(keys)

		if missing is not None:
			pass #Fixme

		if deferred is not None:
			pass#Fixme

		return entities

	def put(self, entity):
		"""Save an entity in the Cloud Datastore.

		.. note::

		   This is just a thin wrapper over :meth:`put_multi`.
		   The backend API does not make a distinction between a single
		   entity or multiple entities in a commit request.

		:type entity: :class:`google.cloud.datastore.entity.Entity`
		:param entity: The entity to be saved to the datastore.
		"""
		self.put_multi(entities=[entity])

	def put_multi(self, entities):
		"""Save entities in the Cloud Datastore.

		:type entities: list of :class:`google.cloud.datastore.entity.Entity`
		:param entities: The entities to be saved to the datastore.

		:raises: :class:`ValueError` if ``entities`` is a single entity.
		"""
		if isinstance(entities, Entity):
			raise ValueError("Pass a sequence of entities")

		if not entities:
			return

		current = self.current_batch
		in_batch = current is not None

		if not in_batch:
			current = self.batch()
			current.begin()

		for entity in entities:
			current.put(entity)

		if not in_batch:
			current.commit()

	def delete(self, key):
		"""Delete the key in the Cloud Datastore.

		.. note::

		   This is just a thin wrapper over :meth:`delete_multi`.
		   The backend API does not make a distinction between a single key or
		   multiple keys in a commit request.

		:type key: :class:`google.cloud.datastore.key.Key`
		:param key: The key to be deleted from the datastore.
		"""
		self.delete_multi(keys=[key])

	def delete_multi(self, keys):
		"""Delete keys from the Cloud Datastore.

		:type keys: list of :class:`google.cloud.datastore.key.Key`
		:param keys: The keys to be deleted from the Datastore.
		"""
		if not keys:
			return

		# We allow partial keys to attempt a delete, the backend will fail.
		current = self.current_batch
		in_batch = current is not None

		if not in_batch:
			current = self.batch()
			current.begin()

		for key in keys:
			current.delete(key)

		if not in_batch:
			current.commit()

	def allocate_ids(self, incomplete_key, num_ids):
		"""Allocate a list of IDs from a partial key.

		:type incomplete_key: :class:`google.cloud.datastore.key.Key`
		:param incomplete_key: Partial key to use as base for allocated IDs.

		:type num_ids: int
		:param num_ids: The number of IDs to allocate.

		:rtype: list of :class:`google.cloud.datastore.key.Key`
		:returns: The (complete) keys allocated with ``incomplete_key`` as
				  root.
		:raises: :class:`ValueError` if ``incomplete_key`` is not a
				 partial key.
		"""
		if not incomplete_key.is_partial:
			raise ValueError(('Key is not partial.', incomplete_key))

		if num_ids>1:
			raise ValueError("Actually you can only request one Key")

		from random import random
		from time import time



		try:
			from viur.xeno.databases import dbinterface
			newId = str(dbinterface.generateID())
		except :
			newId = int(time()*1000)^int(random()*10000000000000) #we need something better

		return [incomplete_key.completed_key(newId)]

		incomplete_key_pb = incomplete_key.to_protobuf()
		incomplete_key_pbs = [incomplete_key_pb] * num_ids

		conn = self.connection
		allocated_key_pbs = conn.allocate_ids(incomplete_key.project,
											  incomplete_key_pbs)
		allocated_ids = [allocated_key_pb.path[-1].id
						 for allocated_key_pb in allocated_key_pbs]
		return [incomplete_key.completed_key(allocated_id)
				for allocated_id in allocated_ids]

	def key(self, *path_args, **kwargs):
		"""Proxy to :class:`google.cloud.datastore.key.Key`.

		Passes our ``project``.
		"""
		if "project" in kwargs:
			raise Exception
		kwargs["project"] = self.project
		if "namespace" not in kwargs:
			kwargs["namespace"] = self.namespace
		return Key(*path_args, **kwargs)

	def batch(self):
		"""Proxy to :class:`google.cloud.datastore.batch.Batch`."""
		return Batch(self)

	def transaction(self, **kwargs):
		"""Proxy to :class:`google.cloud.datastore.transaction.Transaction`.

		:param kwargs: Keyword arguments to be passed in.
		"""
		return Transaction(self, **kwargs)

	def query(self, **kwargs):
		"""Proxy to :class:`google.cloud.datastore.query.Query`.

		Passes our ``project``.

		Using query to search a datastore:

		.. testsetup:: query

			import os
			import uuid

			from google.cloud import datastore

			unique = os.getenv('CIRCLE_BUILD_NUM', str(uuid.uuid4())[0:8])
			client = datastore.Client(namespace='ns{}'.format(unique))
			query = client.query(kind='_Doctest')

			def do_something(entity):
				pass

		.. doctest:: query

			>>> query = client.query(kind='MyKind')
			>>> query.add_filter('property', '=', 'val')

		Using the query iterator

		.. doctest:: query

			>>> query_iter = query.fetch()
			>>> for entity in query_iter:
			...     do_something(entity)

		or manually page through results

		.. testsetup:: query-page

			import os
			import uuid

			from google.cloud import datastore
			from tests.system.test_system import Config  # system tests

			unique = os.getenv('CIRCLE_BUILD_NUM', str(uuid.uuid4())[0:8])
			client = datastore.Client(namespace='ns{}'.format(unique))

			key = client.key('_Doctest')
			entity1 = datastore.Entity(key=key)
			entity1['foo'] = 1337
			entity2 = datastore.Entity(key=key)
			entity2['foo'] = 42
			Config.TO_DELETE.extend([entity1, entity2])
			client.put_multi([entity1, entity2])

			query = client.query(kind='_Doctest')
			cursor = None

		.. doctest:: query-page

			>>> query_iter = query.fetch(start_cursor=cursor)
			>>> pages = query_iter.pages
			>>>
			>>> first_page = next(pages)
			>>> first_page_entities = list(first_page)
			>>> query_iter.next_page_token is None
			True

		:param kwargs: Parameters for initializing and instance of
					   :class:`~google.cloud.datastore.query.Query`.

		:rtype: :class:`~google.cloud.datastore.query.Query`
		:returns: A query object.
		"""
		if "client" in kwargs:
			raise TypeError("Cannot pass client")
		if "project" in kwargs:
			raise TypeError("Cannot pass project")
		kwargs["project"] = self.project
		if "namespace" not in kwargs:
			kwargs["namespace"] = self.namespace
		return Query(self, **kwargs)
