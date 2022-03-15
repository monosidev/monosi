from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import json

from .base import Destination, DestinationConfiguration, Publisher


class KafkaDestinationConfiguration(DestinationConfiguration):
	@classmethod
	def validate(cls, configuration):
		raise NotImplementedError

	@classmethod
	def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "host": { "type": "string" },
                "port": { "type": "string" },
            },
            "secret": [  ],
        }


	def connection_string(self):
        configuration = json.loads(self.configuration)

		return "{host}:{port}".format(
			host=configuration.get('host'),
			port=configuration.get('port'),
		)

	@property
	def type(self):
		return "kafka"

class KafkaDestinationPublisher(Publisher):
	def __init__(self, configuration: KafkaDestinationConfiguration):
		self.configuration = configuration
		self.connection = None

	def _initialize(self):
		connection_string = self.configuration.connection_string()
		
		admin = KafkaAdminClient(bootstrap_servers=connection_string)
		topic = NewTopic(name="msi_kafka", num_partitions=1, replication_factor=1)
		admin.create_topics(new_topics=[topic], validate_only=False)

		self.connection = KafkaProducer(bootstrap_servers=connection_string,
										value_serializer=lambda x: json.dumps(x).encode("utf-8"))

	def run(self, item):
		self.connection.send("msi_kafka", item)



class KafkaDestination(Destination):
	def _push(self):
		raise NotImplementedError
