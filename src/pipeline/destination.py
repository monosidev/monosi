import json
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, List

from ingestion.destinations import Destination, DestinationConfiguration, Publisher


class MsiWireDestination(Destination):
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def _push(self, data):
        self.pipeline.process(data)


class SQLAlchemyDestinationConfiguration(DestinationConfiguration):
    @classmethod
    def validate(cls, configuration):
        raise NotImplementedError

    @classmethod
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "type": { "type": "string" },
                "user": { "type": "string" },
                "password": { "type": "string" },
                "host": { "type": "string" },
                "port": { "type": "string" },
                "database": { "type": "string" },
                "schema": { "type": "string" },
            },
            "secret": [ "password" ],
        }

    def connection_string(self) -> str:
        configuration = json.loads(self.configuration)

        return '{type}://{user}:{password}@{host}:{port}/{database}'.format(
            type=configuration.get('type'),
            user=configuration.get('user'),
            password=configuration.get('password'),
            host=configuration.get('host'),
            port=configuration.get('port'),
            database=configuration.get('database'),
            schema=configuration.get('schema'),
        )

    @property
    def type(self):
        raise NotImplementedError


class SQLAlchemyDestination(Destination):
    def push(self, sqlalchemy_objs: List[Any]):
        driver = None

        if driver == None:
            return

        Session = sessionmaker(bind=driver.engine)
        with Session() as session:
            from core.models.metadata.metric import MsiMetric
            session.bulk_insert_mappings(MsiMetric, [metric.to_dict() for metric in metrics])
            session.commit()
            session.close()

class SQLAlchemyPublisher(Publisher):
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

        Session = sessionmaker(bind=self.driver.engine)
        with Session() as session:
            from core.models.metadata.metric import MsiMetric
            session.bulk_insert_mappings(MsiMetric, [metric.to_dict() for metric in metrics])
            session.commit()
            session.close()

    def run(self, sqlalchemy_objs: List[Any]):
        self._initialize()

        return self._execute(sqlalchemy_objs)


class MsiInternalDestinationConfiguration(SQLAlchemyDestinationConfiguration):
    @property
    def type(self):
        return "msi_internal"

class MsiInternalPublisher(SQLAlchemyPublisher):
    pass

class MsiInternalDestination(SQLAlchemyDestination):
    pass

