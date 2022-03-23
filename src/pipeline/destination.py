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

class MsiIntegrationDestination(Destination):
    def __init__(self, integration):
        self.integration = integration

    def _push(self, zscores):
        [self.integration.send(zscore['metric_id'], self.integration.config) for zscore in zscores]


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
                logging.error(e)
        elif len(sqlalchemy_objs) > 0 and 'table_name' in sqlalchemy_objs[0]:
            try: 
                Session = sessionmaker(bind=self.engine)
                with Session() as session:
                    from server.models import Monitor

                    entries_to_update = []
                    entries_to_put = []
                    # Find all customers that needs to be updated and build mappings
                    def uniq(monitors):
                        return [dict(s) for s in set(frozenset(d.items()) for d in monitors)]

                    monitors = uniq(sqlalchemy_objs)

                    for monitor in monitors:
                        monitors_objs = session.query(Monitor.id).filter(
                                Monitor.table_name == monitor['table_name'],
                                Monitor.database == monitor['database'],
                                Monitor.schema == monitor['schema'],
                        ).all()
                        if len(monitors_objs) > 0:
                            entries_to_update.append(monitor)
                        else:
                            entries_to_put.append(monitor)

                    session.bulk_insert_mappings(Monitor, entries_to_put)
                    session.bulk_update_mappings(Monitor, entries_to_update)
                    session.commit()

                    session.close()
            except Exception as e:
                logging.error(e)
        else:
            try: 
                Session = sessionmaker(bind=self.engine)
                with Session() as session:
                    from server.models import ZScore
                    session.bulk_insert_mappings(ZScore, sqlalchemy_objs)
                    session.commit()
                    session.close()
            except Exception as e:
                logging.error(e)


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

