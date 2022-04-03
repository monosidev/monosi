import json
from ingestion.pipeline import Pipeline
from ingestion.transformers import (
    AnomalyTransformer,
    MetricTransformer,
    MonitorTransformer,
    ZScoreTransformer,
)
from server.middleware import db

from .config import db_config as destination_dict

import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Any, List

from ingestion.sources.postgresql import PostgreSQLSourceConfiguration

from ingestion.destinations.base import Destination, Publisher
import server.models as models
from server.jobs.analysis import activator as zscores_activator


def resolve_to_model(data: List[Any]): # TODO: Handle resolution
    if len(data) == 0:
        return

    example_dict = data[0]
    if 'metric' in example_dict.keys():
        return models.Metric
    elif 'timestamp_field' in example_dict.keys():
        return models.Monitor
    elif 'zscore' in example_dict.keys():
        return models.ZScore

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

    def upsert_data(self, og_entries, key="metric_id"):
        model = models.ZScore
        entries = {}
        for entry in og_entries:
            entries[entry[key]] = entry
        entries_to_insert = []
        
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            for each in session.query(model).filter(models.ZScore.metric_id.in_(entries.keys())).all():
                entry = entries.pop(each.metric_id)

        for entry in entries.values():
            entries_to_insert.append(entry)

        session.bulk_insert_mappings(model, entries_to_insert)

        session.commit()

    def _execute(self, data: List[Any]):
        if self.engine is None:
            raise Exception("Initialize publisher before execution.")

        if data is None or len(data) == 0:
            logging.warn("No data to persist")
            return

        try: 
            model = resolve_to_model(data)

            def uniq(arr): # TODO: Transformer should handle uniqueness
                return [dict(s) for s in set(frozenset(d.items()) for d in arr)]

            unique_data = uniq(data)

            if len(unique_data) > 0 and 'metric_id' in unique_data[0].keys():
                self.upsert_data(unique_data)
                return

            # TODO: Handle insert vs. update
            Session = sessionmaker(bind=self.engine)
            with Session() as session:
                session.bulk_insert_mappings(model, unique_data)
                session.commit()
                session.close()
        except Exception as e:
            import traceback
            traceback.print_exc()
            logging.error("Issue persisting information: {}".format(e))
            raise e

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

        
class MsiIntegrationDestination(Destination):
    def __init__(self, integration):
        self.integration = integration

    def _push(self, zscores):
        self.integration.send(zscores, self.integration.config)

class MsiIntegrationShim(Destination):
    def _push(self, anomalies):
        anomalies_destinations = []
        [anomalies_destinations.append(MsiIntegrationDestination(integration)) for integration in db.db.session.query(models.Integration).all()]

        [destination.push(anomalies) for destination in anomalies_destinations]


configuration = MonosiDestinationConfiguration(json.dumps(destination_dict))
msi_db = MonosiDestination(configuration)

integration_shim_destination = MsiIntegrationShim('{}')

anomalies_pipeline = Pipeline(
    transformers=[AnomalyTransformer],
    destinations=[integration_shim_destination]
)

zscores_pipeline = Pipeline(
    transformers=[ZScoreTransformer],
    destinations=[msi_db, anomalies_pipeline]
)

metrics_pipeline = Pipeline(
    transformers=[MetricTransformer],
    destinations=[msi_db, zscores_activator]
)

monitors_pipeline = Pipeline(
    transformers=[MonitorTransformer],
    destinations=[msi_db] # TODO: Table health monitor creator destination?
)

