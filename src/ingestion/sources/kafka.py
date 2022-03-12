import json

from .base import Source, SourceConfiguration

class KafkaSourceConfiguration(SourceConfiguration):
	@classmethod
	def validate(cls, configuration):
        raise NotImplementedError

    def connection_string(self) -> str:
        raise NotImplementedError

    @property
	def type(self):
		return "kafka"


class KafkaSource(Source):
    pass
