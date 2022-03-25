import json
from ingestion.pipeline import Pipeline
from ingestion.transformers import (
    # AnomalyTransformer,
    # MetricTransformer,
    MonitorTransformer,
    # ZScoreTransformer,
)

from .config import db_config as destination_dict

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, List

from ingestion.sources.postgresql import PostgreSQLSourceConfiguration

from ingestion.destinations.base import Destination, Publisher
import server.models as models


def resolve_to_model(data: List[Any]):
    if data is None or len(data) == 0:
        raise Exception("Could not resolve to model. Data is empty.")

    model_dict = data[0]

    try:
        models.Monitor.from_dict(model_dict)
        return models.Monitor
    except:
        raise Exception("Could not resolve to model. Did not match.")


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
            model = resolve_to_model(data)

            def uniq(arr):
                return [dict(s) for s in set(frozenset(d.items()) for d in arr)]

            unique_data = uniq(data)

            Session = sessionmaker(bind=self.engine)
            with Session() as session:
                session.bulk_insert_mappings(model, unique_data)
                session.commit()
                session.close()
        except Exception as e:
            logging.error(e)


    def run(self, data: List[Any]):
        self._initialize()

        return self._execute(data)


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



configuration = MonosiDestinationConfiguration(json.dumps(destination_dict))
msi_db = MonosiDestination(configuration)

msi_pipeline = Pipeline(
    transformers=[
        # AnomalyTransformer,
        # MetricTransformer,
        MonitorTransformer,
        # ZScoreTransformer
    ],
    destinations=[msi_db],
)

