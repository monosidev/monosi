import logging

from pipeline import ingestion_task
from pipeline.base import analysis_task
from scheduler import job
from telemetry.events import track_event

from server.models import DataSource
from server.config import db_config as destination
from server.middleware.db import db


logger = logging.getLogger(__name__)

class MetadataJob(job.JobBase):
    MAX_RETRIES = 3
    TIMEOUT = 10

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': ('This ingests metadata from the source specified.'),
            'arguments': [
                {'type': 'integer', 'description': 'The ID of the datasource from which to ingest metadata.'},
            ],
        }

    def run(self, datasource_id, *args, **kwargs):
        track_event(action="metadata_ingestion_start", label="server")

        source = db.session.query(DataSource).filter(DataSource.id == datasource_id).one()
        source_configuration = source.to_dict()
        source_configuration['config']['type'] = source_configuration['type']

        # Metrics Pipeline
        try:
            mpipe_metrics = ingestion_task(source_configuration['config'], destination)
            mpipe_metrics.run()
        except Exception as e:
            logging.error(e)

        # Reprocessing - ZScores Pipelines
        try:
            mpipe_zscores = analysis_task(destination, destination)
            mpipe_zscores.run()
        except Exception as e:
            logging.error(e)

        track_event(action="metadata_ingestion_stop", label="server")

