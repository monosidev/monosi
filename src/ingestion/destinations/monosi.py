import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, List

from ingestion.sources.postgresql import PostgreSQLSourceConfiguration

from .base import Destination, Publisher


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

    def _execute(self, data: List[Any]):
        if self.engine is None:
            raise Exception("Initialize publisher before execution.")

        try: 
            from server.models import Monitor
            model = Monitor # TODO

            Session = sessionmaker(bind=self.engine)
            with Session() as session:
                session.bulk_insert_mappings(model, data)
                session.commit()
                session.close()
        except Exception as e:
            logging.error(e)
    
    def _terminate(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
        
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None


    def run(self, data: List[Any]):
        self._initialize()
        result = self._execute(data)
        self._terminate()

        return result


class MonosiDestinationConfiguration(PostgreSQLSourceConfiguration):
    @property
    def type(self):
        return "monosi"

class MonosiPublisher(SQLAlchemyPublisher):
    pass

class MonosiDestination(Destination):
    def _push(self, data):
        publisher = MonosiPublisher(self.configuration)
        publisher.run(data)


