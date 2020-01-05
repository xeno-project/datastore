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
import six, base64,logging
from .key import Key
from .entity import Entity


KEY_PROPERTY = "__key__"

_NOT_FINISHED = "NOT FINISHED"
_NO_MORE_RESULTS = "NO MORE RESULTS"

_FINISHED = (
	_NO_MORE_RESULTS,
	"MORE RESULTS AFTER LIMIT",
	"MORE RESULTS AFTER CURSOR",
)


class Query(object):

	OPERATORS = {
		"<=": "<=",
		">=": ">=",
		"<": "<",
		">": ">",
		"=": "=",
	}
	"""Mapping of operator strings and their protobuf equivalents."""

	def __init__(
		self,
		client,
		kind=None,
		project=None,
		namespace=None,
		ancestor=None,
		filters=(),
		projection=(),
		order=(),
		distinct_on=(),
	):

		self._client = client
		self._kind = kind
		self._project = project or client.project
		self._namespace = namespace or client.namespace
		self._ancestor = ancestor
		self._filters = []
		# Verify filters passed in.
		for property_name, operator, value in filters:
			self.add_filter(property_name, operator, value)
		self._projection = list(projection)
		self._order = list(("order", order))
		self._distinct_on = list(("distinct_on", distinct_on))

	@property
	def project(self):
		"""Get the project for this Query.

		:rtype: str
		:returns: The project for the query.
		"""
		return self._project or self._client.project

	@property
	def namespace(self):
		"""This query's namespace

		:rtype: str or None
		:returns: the namespace assigned to this query
		"""
		return self._namespace or self._client.namespace

	@namespace.setter
	def namespace(self, value):
		"""Update the query's namespace.

		:type value: str
		"""
		if not isinstance(value, str):
			raise ValueError("Namespace must be a string")
		self._namespace = value

	@property
	def kind(self):
		"""Get the Kind of the Query.

		:rtype: str
		:returns: The kind for the query.
		"""
		return self._kind

	@kind.setter
	def kind(self, value):
		"""Update the Kind of the Query.

		:type value: str
		:param value: updated kind for the query.

		.. note::

		   The protobuf specification allows for ``kind`` to be repeated,
		   but the current implementation returns an error if more than
		   one value is passed.  If the back-end changes in the future to
		   allow multiple values, this method will be updated to allow passing
		   either a string or a sequence of strings.
		"""
		if not isinstance(value, str):
			raise TypeError("Kind must be a string")
		self._kind = value

	@property
	def ancestor(self):
		"""The ancestor key for the query.

		:rtype: :class:`~google.cloud.datastore.key.Key` or None
		:returns: The ancestor for the query.
		"""
		return self._ancestor

	@ancestor.setter
	def ancestor(self, value):
		"""Set the ancestor for the query

		:type value: :class:`~google.cloud.datastore.key.Key`
		:param value: the new ancestor key
		"""
		if not isinstance(value, Key):
			raise TypeError("Ancestor must be a Key")
		self._ancestor = value

	@ancestor.deleter
	def ancestor(self):
		"""Remove the ancestor for the query."""
		self._ancestor = None

	@property
	def filters(self):
		"""Filters set on the query.

		:rtype: tuple[str, str, str]
		:returns: The filters set on the query. The sequence is
			``(property_name, operator, value)``.
		"""
		return self._filters[:]

	def add_filter(self, property_name, operator, value):

		if self.OPERATORS.get(operator) is None:
			error_message = 'Invalid expression: "%s"' % (operator,)
			choices_message = "Please use one of: =, <, <=, >, >=."
			raise ValueError(error_message, choices_message)

		if property_name == KEY_PROPERTY and not isinstance(value, Key):
			raise ValueError('Invalid key: "%s"' % value)

		self._filters.append((property_name, operator, value))

	@property
	def projection(self):
		"""Fields names returned by the query.

		:rtype: sequence of string
		:returns: Names of fields in query results.
		"""
		return self._projection[:]

	@projection.setter
	def projection(self, projection):
		"""Set the fields returned the query.

		:type projection: str or sequence of strings
		:param projection: Each value is a string giving the name of a
						   property to be included in the projection query.
		"""
		if isinstance(projection, str):
			projection = [projection]
		self._projection[:] = projection

	def keys_only(self):
		"""Set the projection to include only keys."""
		self._projection[:] = [KEY_PROPERTY]

	def key_filter(self, key, operator="="):
		"""Filter on a key.

		:type key: :class:`google.cloud.datastore.key.Key`
		:param key: The key to filter on.

		:type operator: str
		:param operator: (Optional) One of ``=``, ``<``, ``<=``, ``>``, ``>=``.
						 Defaults to ``=``.
		"""
		self.add_filter(KEY_PROPERTY, operator, key)

	@property
	def order(self):
		"""Names of fields used to sort query results.

		:rtype: sequence of string
		:returns: The order(s) set on the query.
		"""
		return self._order[:]

	@order.setter
	def order(self, value):
		"""Set the fields used to sort query results.

		Sort fields will be applied in the order specified.

		:type value: str or sequence of strings
		:param value: Each value is a string giving the name of the
					  property on which to sort, optionally preceded by a
					  hyphen (-) to specify descending order.
					  Omitting the hyphen implies ascending order.
		"""
		if isinstance(value, str):
			value = [value]
		self._order[:] = value

	@property
	def distinct_on(self):
		"""Names of fields used to group query results.

		:rtype: sequence of string
		:returns: The "distinct on" fields set on the query.
		"""
		return self._distinct_on[:]

	@distinct_on.setter
	def distinct_on(self, value):
		"""Set fields used to group query results.

		:type value: str or sequence of strings
		:param value: Each value is a string giving the name of a
					  property to use to group results together.
		"""
		if isinstance(value, str):
			value = [value]
		self._distinct_on[:] = value

	def fetch(
		self,
		limit=None,
		offset=0,
		start_cursor=None,
		end_cursor=None,
		client=None,
		eventual=False,
	):
		if client is None:
			client = self._client

		return Iterator(
			self,
			client,
			limit=limit,
			offset=offset,
			start_cursor=start_cursor,
			end_cursor=end_cursor,
			eventual=eventual,
		)


class Iterator(object):

	next_page_token = None

	def __init__(
		self,
		query,
		client,
		limit=None,
		offset=None,
		start_cursor=None,
		end_cursor=None,
		eventual=False,
	):
		self._started = False
		self.client = client
		self.item_to_value = Entity
		self.max_results = limit
		self.page_number = 0
		self.next_page_token = start_cursor
		self.num_results = 0
		self._query = query
		self._offset = offset
		self._end_cursor = end_cursor
		self._eventual = eventual
		self._more_results = True
		self._skipped_results = 0

	@property
	def pages(self):
		if self._started:
			raise ValueError("Iterator has already started", self)
		self._started = True
		return self._page_iter(increment=True)

	def _items_iter(self):
		for page in self._page_iter(increment=False):
			for item in page:
				self.num_results += 1
				yield item

	def __iter__(self):
		if self._started:
			raise ValueError("Iterator has already started", self)
		self._started = True
		return self._items_iter()

	def _page_iter(self, increment):
		page = self._next_page()
		while page is not None:
			self.page_number += 1
			if increment:
				self.num_results += page.num_items
			yield page
			page = self._next_page()

	def _next_page(self):
		if not self._more_results:
			return None

		transaction = self.client.current_transaction
		if transaction is None:
			transaction_id = None
		else:
			transaction_id = transaction.id #FIXME

		from viur.xeno.databases import dbinterface
		entities = dbinterface.query(self._query)

		return Page(self, entities, self.item_to_value)

class Page(object):
	def __init__(self, parent, items, item_to_value, raw_page=None):
		self._parent = parent
		self._num_items = len(items)
		self._remaining = self._num_items
		self._item_iter = iter(items)
		self._item_to_value = item_to_value
		self._raw_page = raw_page

	@property
	def raw_page(self):
		return self._raw_page

	@property
	def num_items(self):
		return self._num_items

	@property
	def remaining(self):
		return self._remaining

	def __iter__(self):
		return self

	def next(self):
		item = six.next(self._item_iter)
		#logging.error(item)
		#result = self._item_to_value(self._parent, item)
		#logging.error(result)
		self._remaining -= 1
		return item

	__next__ = next
