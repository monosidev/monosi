import json
import logging
from sqlalchemy import create_engine
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
        print(self.configuration)
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


class SQLAlchemyPublisher(Publisher):
    def __init__(self, configuration):
        self.configuration = configuration
        self.engine = None
        self.connection = None

    def _create_engine(self):
        try:
            return create_engine(self.configuration.connection_string())
        except Exception as e:
            raise e

    def _initialize(self):
        if self.engine and self.connection:
            return

        self.engine = self._create_engine()
        self.connection = self.engine.connect()

    def _execute(self, sqlalchemy_objs: List[Any]):
        if self.engine is None:
            raise Exception("Initialize publisher before execution.")

        if len(sqlalchemy_objs) > 0 and 'metric' in sqlalchemy_objs[0]:
            try: 
                Session = sessionmaker(bind=self.engine)
                with Session() as session:
                    from server.models import Metric
                    session.bulk_insert_mappings(Metric, sqlalchemy_objs)
                    session.commit()
                    session.close()
            except Exception as e:
                logging.warn(e)
        else:
            try: 
                Session = sessionmaker(bind=self.engine)
                with Session() as session:
                    from server.models import ZScore
                    session.bulk_insert_mappings(ZScore, sqlalchemy_objs)
                    session.commit()
                    session.close()
            except Exception as e:
                logging.warn(e)


    def run(self, sqlalchemy_objs: List[Any]):
        self._initialize()

        return self._execute(sqlalchemy_objs)

class SQLAlchemyDestination(Destination):
    def push(self, sqlalchemy_objs: List[Any]):
        publisher = SQLAlchemyPublisher(self.configuration)
        publisher.run(sqlalchemy_objs)

class MsiInternalDestinationConfiguration(SQLAlchemyDestinationConfiguration):
    @property
    def type(self):
        return "msi_internal"

class MsiInternalPublisher(SQLAlchemyPublisher):
    pass

class MsiInternalDestination(SQLAlchemyDestination):
    pass

