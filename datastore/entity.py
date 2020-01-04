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

class Entity(dict):

	def __init__(self, key=None, exclude_from_indexes=()):
		super(Entity, self).__init__()
		self.key = key
		self.exclude_from_indexes = exclude_from_indexes
		self._meanings = {}

	def __eq__(self, other):
		"""Compare two entities for equality.

		Entities compare equal if their keys compare equal and their
		properties compare equal.

		:rtype: bool
		:returns: True if the entities compare equal, else False.
		"""
		if not isinstance(other, Entity):
			return NotImplemented

		return (
			self.key == other.key
			and self.exclude_from_indexes == other.exclude_from_indexes
			and self._meanings == other._meanings
			and super(Entity, self).__eq__(other)
		)

	def __ne__(self, other):
		"""Compare two entities for inequality.

		Entities compare equal if their keys compare equal and their
		properties compare equal.

		:rtype: bool
		:returns: False if the entities compare equal, else True.
		"""
		return self != other

	@property
	def kind(self):
		"""Get the kind of the current entity.

		.. note::

			This relies entirely on the :class:`google.cloud.datastore.key.Key`
			set on the entity.  That means that we're not storing the kind
			of the entity at all, just the properties and a pointer to a
			Key which knows its Kind.
		"""
		if self.key:
			return self.key.kind
		return None

	@property
	def id(self):
		"""Get the ID of the current entity.

		.. note::

			This relies entirely on the :class:`google.cloud.datastore.key.Key`
			set on the entity.  That means that we're not storing the ID
			of the entity at all, just the properties and a pointer to a
			Key which knows its ID.
		"""
		if self.key is None:
			return None
		else:
			return self.key.id

	def __repr__(self):
		if self.key:
			return "<Entity%s %s>" % (
				self.key._flat_path,
				super(Entity, self).__repr__(),
			)
		else:
			return "<Entity %s>" % (super(Entity, self).__repr__())
