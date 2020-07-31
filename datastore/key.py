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
import copy,six

class Key(object):

	def __init__(self, *path_args, **kwargs):
		'''
			Key("kind", 1234, project = project)
		'''
		self._flat_path = path_args
		self._parent = kwargs.get("parent")
		self._namespace = kwargs.get("namespace")
		project = kwargs.get("project")
		self._project = project
		self._path = self._combine_args()

	def __eq__(self, other):
		"""Compare two keys for equality.

		Incomplete keys never compare equal to any other key.

		Completed keys compare equal if they have the same path, project,
		and namespace.

		:rtype: bool
		:returns: True if the keys compare equal, else False.
		"""
		if not isinstance(other, Key):
			return NotImplemented

		if self.is_partial or other.is_partial:
			return False

		return (
			self.flat_path == other.flat_path
			and self.project == other.project
			and self.namespace == other.namespace
		)

	def __ne__(self, other):
		"""Compare two keys for inequality.

		Incomplete keys never compare equal to any other key.

		Completed keys compare equal if they have the same path, project,
		and namespace.

		:rtype: bool
		:returns: False if the keys compare equal, else True.
		"""
		return not self == other

	def __hash__(self):
		"""Hash a keys for use in a dictionary lookp.

		:rtype: int
		:returns: a hash of the key's state.
		"""
		return hash(self.flat_path) + hash(self.project) + hash(self.namespace)

	@staticmethod
	def _parse_path(path_args):
		'''
		[kind,id_or_name,kind2,id_or_name_2]
		> [{"kind":xx, "id":?,"name":?}]
		'''
		if len(path_args) == 0:
			raise Exception

		import logging


		kind_list = path_args[::2]
		id_or_name_list = list(path_args[1::2])
		partial_ending = object()
		if len(path_args) % 2 == 1:
			id_or_name_list.append(partial_ending)

		result = []

		for kind, id_or_name in zip(kind_list, id_or_name_list):
			curr_key_path = {
				"kind": kind
			}
			#logging.error(id_or_name)
			#logging.error(kind)
			if isinstance(id_or_name, str):
				curr_key_path["name"] = id_or_name
			elif isinstance(id_or_name, int):
				curr_key_path["id"] = id_or_name
			elif id_or_name is not partial_ending:
				raise Exception

			result.append(curr_key_path)

		return result

	def _combine_args(self):
		child_path = self._parse_path(self._flat_path)

		if self._parent:
			if self._parent.is_partial:
				raise Exception

			child_path = self._parent.path + child_path

			self._flat_path = self._parent.flat_path + self._flat_path

			if self._namespace and self._namespace != self._parent.namespace:
				raise Exception

			self._namespace = self._parent.namespace

			if self._project and self._project != self._parent.project:
				raise Exception

			self._project = self._parent.project

		return child_path

	def _clone(self):
		"""Duplicates the Key.
		Most attributes are simple types, so don't require copying. Other
		attributes like ``parent`` are long-lived and so we re-use them.
		:rtype: :class:`google.cloud.datastore.key.Key`
		:returns: A new ``Key`` instance with the same data as the current one.
		"""
		cloned_self = self.__class__(
			*self.flat_path, project=self.project, namespace=self.namespace
		)
		# If the current parent has already been set, we re-use
		# the same instance
		cloned_self._parent = self._parent
		return cloned_self

	def completed_key(self, id_or_name):
		"""Creates new key from existing partial key by adding final ID/name.
		:type id_or_name: str or integer
		:param id_or_name: ID or name to be added to the key.
		:rtype: :class:`google.cloud.datastore.key.Key`
		:returns: A new ``Key`` instance with the same data as the current one
				  and an extra ID or name added.
		:raises: :class:`ValueError` if the current key is not partial or if
				 ``id_or_name`` is not a string or integer.
		"""
		if not self.is_partial:
			raise ValueError("Only a partial key can be completed.")

		if isinstance(id_or_name, six.string_types):
			id_or_name_key = "name"
		elif isinstance(id_or_name, six.integer_types):
			id_or_name_key = "id"
		else:
			raise ValueError(id_or_name, "ID/name was not a string or integer.")

		new_key = self._clone()
		new_key._path[-1][id_or_name_key] = id_or_name
		new_key._flat_path += (id_or_name,)
		return new_key

	@property
	def is_partial(self):
		"""Boolean indicating if the key has an ID (or name).

		:rtype: bool
		:returns: ``True`` if the last element of the key's path does not have
				  an ``id`` or a ``name``.
		"""
		return self.id_or_name is None

	@property
	def namespace(self):
		"""Namespace getter.

		:rtype: str
		:returns: The namespace of the current key.
		"""
		return self._namespace

	@property
	def path(self):
		"""Path getter.

		Returns a copy so that the key remains immutable.

		:rtype: :class:`list` of :class:`dict`
		:returns: The (key) path of the current key.
		"""
		return copy.deepcopy(self._path)

	@property
	def flat_path(self):
		"""Getter for the key path as a tuple.

		:rtype: tuple of string and integer
		:returns: The tuple of elements in the path.
		"""
		return self._flat_path

	@property
	def kind(self):
		"""Kind getter. Based on the last element of path.

		:rtype: str
		:returns: The kind of the current key.
		"""
		return self.path[-1]["kind"]

	@property
	def id(self):
		"""ID getter. Based on the last element of path.

		:rtype: int
		:returns: The (integer) ID of the key.
		"""
		return self.path[-1].get("id")

	@property
	def name(self):
		"""Name getter. Based on the last element of path.

		:rtype: str
		:returns: The (string) name of the key.
		"""
		return self.path[-1].get("name")

	@property
	def id_or_name(self):
		"""Getter. Based on the last element of path.

		:rtype: int (if ``id``) or string (if ``name``)
		:returns: The last element of the key's path if it is either an ``id``
				  or a ``name``.
		"""
		return self.id or self.name

	@property
	def project(self):
		"""Project getter.

		:rtype: str
		:returns: The key's project.
		"""
		return self._project

	def _make_parent(self):
		"""Creates a parent key for the current path.

		Extracts all but the last element in the key path and creates a new
		key, while still matching the namespace and the project.

		:rtype: :class:`google.cloud.datastore.key.Key` or :class:`NoneType`
		:returns: A new ``Key`` instance, whose path consists of all but the
				  last element of current path. If the current key has only
				  one path element, returns ``None``.
		"""
		if self.is_partial:
			parent_args = self.flat_path[:-1]
		else:
			parent_args = self.flat_path[:-2]
		if parent_args:
			return Key(
				*parent_args, project=self.project, namespace=self.namespace
			)

	@property
	def parent(self):
		"""The parent of the current key.

		:rtype: :class:`google.cloud.datastore.key.Key` or :class:`NoneType`
		:returns: A new ``Key`` instance, whose path consists of all but the
				  last element of current path. If the current key has only
				  one path element, returns ``None``.
		"""
		if self._parent is None:
			self._parent = self._make_parent()

		return self._parent

	def __repr__(self):
		return "<Key%s, project=%s>" % (self._flat_path, self.project)
