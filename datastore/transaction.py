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
from .batch import Batch


class Transaction(Batch):
	_status = None

	def __init__(self, client, read_only=False):
		super(Transaction, self).__init__(client)
		self._id = None

		self._options = {"read_only": False}

	@property
	def id(self):
		"""Getter for the transaction ID.

		:rtype: str
		:returns: The ID of the current transaction.
		"""
		return self._id

	def current(self):
		"""Return the topmost transaction.

		.. note::

			If the topmost element on the stack is not a transaction,
			returns None.

		:rtype: :class:`google.cloud.datastore.transaction.Transaction` or None
		:returns: The current transaction (if any are active).
		"""
		top = super(Transaction, self).current()
		if isinstance(top, Transaction):
			return top

	def begin(self):
		"""Begins a transaction.

		This method is called automatically when entering a with
		statement, however it can be called explicitly if you don't want
		to use a context manager.

		:raises: :class:`~exceptions.ValueError` if the transaction has
				 already begun.
		"""
		super(Transaction, self).begin()
		# FIXME
		try:
			response_pb = self._client._datastore_api.begin_transaction(self.project)
			self._id = response_pb.transaction
		except:  # noqa: E722 do not use bare except, specify exception instead
			pass #self._status = self._ABORTED
			#raise

	def rollback(self):
		"""Rolls back the current transaction.

		This method has necessary side-effects:

		- Sets the current transaction's ID to None.
		"""
		try:
			# No need to use the response it contains nothing.
			self._client._datastore_api.rollback(self.project, self._id)
		finally:
			super(Transaction, self).rollback()
			# Clear our own ID in case this gets accidentally reused.
			self._id = None

	def commit(self):
		"""Commits the transaction.

		This is called automatically upon exiting a with statement,
		however it can be called explicitly if you don't want to use a
		context manager.

		This method has necessary side-effects:

		- Sets the current transaction's ID to None.
		"""
		try:
			super(Transaction, self).commit()
		finally:
			# Clear our own ID in case this gets accidentally reused.
			self._id = None

	def put(self, entity):
		"""Adds an entity to be committed.

		Ensures the transaction is not marked readonly.
		Please see documentation at
		:meth:`~google.cloud.datastore.batch.Batch.put`

		:type entity: :class:`~google.cloud.datastore.entity.Entity`
		:param entity: the entity to be saved.

		:raises: :class:`RuntimeError` if the transaction
				 is marked ReadOnly
		"""
		if self._options["read_only"]:
			raise RuntimeError("Transaction is read only")
		else:
			super(Transaction, self).put(entity)
