from kafka import KafkaProducer, KafkaAdminClient, NewTopic
import json

from .base import Destination, DestinationConfiguration


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


class Publisher(object):
    def run(self, item):
        raise NotImplementedError

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







class Extractor(object):
    def run(self, request: str):
        raise NotImplementedError

class SQLAlchemyExtractor(Extractor):
    def __init__(self, configuration):
        self.configuration = configuration
        self.driver = None

    def _initialize(self):
        try:
            from core.drivers.factory import load_driver
            driver_cls = load_driver(self.configuration)

            self.driver = driver_cls(self.configuration)
        except Exception as e:
            print(e)
            raise Exception("Could not initialize connection to database in Runner.")

    def _execute(self, sql: str):
        if self.driver is None:
            raise Exception("Initialize runner before execution.")

        results = self.driver.execute(sql)
        return results

    def run(self, unit: TaskUnit):
        self._initialize()
        sql = unit.request

        return self._execute(sql)