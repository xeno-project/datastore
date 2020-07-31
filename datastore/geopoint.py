# Taken from gcloud
class GeoPoint( object ):
	"""Simple container for a geo point value.
	:type latitude: float
	:param latitude: Latitude of a point.
	:type longitude: float
	:param longitude: Longitude of a point.
	"""

	def __init__( self, latitude, longitude ):
		self.latitude = latitude
		self.longitude = longitude

	def to_protobuf( self ):
		"""Convert the current object to protobuf.
		:rtype: :class:`google.type.latlng_pb2.LatLng`.
		:returns: The current point as a protobuf.
		"""
		# return latlng_pb2.LatLng(latitude=self.latitude, longitude=self.longitude)
		return None

	def __eq__( self, other ):
		"""Compare two geo points for equality.
		:rtype: bool
		:returns: True if the points compare equal, else False.
		"""
		if not isinstance( other, GeoPoint ):
			return NotImplemented

		return self.latitude == other.latitude and self.longitude == other.longitude

	def __ne__( self, other ):
		"""Compare two geo points for inequality.
		:rtype: bool
		:returns: False if the points compare equal, else True.
		"""
		return not self == other
