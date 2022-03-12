from .base import Destination, DestinationConfiguration

class KafkaDestinationConfiguration(DestinationConfiguration):
	@classmethod
	def validate(cls, configuration):
		raise NotImplementedError

	def connection_string(self):
		raise NotImplementedError

	@property
	def type(self):
		raise "kafka"

class KafkaDestination(Destination):
	def _push(self):
		raise NotImplementedError
