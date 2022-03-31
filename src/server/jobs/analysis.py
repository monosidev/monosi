from dataclasses import dataclass, field
import json
import logging
from typing import List
from ingestion.destinations import Destination
from server.models import Metric
from server.middleware.db import db

class ZScoreShim(Destination):
    def _retrieve_metrics_by_attrs(self, database, schema):
        metrics = db.session.query(Metric).filter( # TODO: Optimize
            Metric.database == database,
            Metric.schema == schema,
        ).all()

        metrics_dict = [metric.to_dict() for metric in metrics]
        return json.loads(json.dumps(metrics_dict))

    def push(self, data):
        if len(data) == 0:
            return

        database = data[0]['database']
        schema = data[0]['schema']

        metrics = self._retrieve_metrics_by_attrs(database, schema)
        from server.pipeline import zscores_pipeline
        zscores_pipeline.push(metrics)

activator = ZScoreShim('{}')

