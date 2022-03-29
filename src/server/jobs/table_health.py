import logging
from server.models import Monitor
from server.pipeline import metrics_pipeline
from server.middleware.db import db

from .base import CollectorJob


class TableHealthCollectorJob(CollectorJob):
    def pipelines(self):
        return [metrics_pipeline]

    def configuration(self):
        try:
            monitors = db.session.query(Monitor).all()
            monitors = [{'type': 'table_health', 'info': monitor.to_dict()} for monitor in monitors]
        except Exception as e:
            logging.warn("Could not load the monitors.")
            monitors = []

        return { 'monitors': monitors }

