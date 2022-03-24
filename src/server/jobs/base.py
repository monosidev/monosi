from ingestion.job import Pipe

from scheduler import job
from telemetry.events import track_event

from server.models import DataSource
from server.middleware.db import db
from server.pipeline import msi_pipeline


class SchemaJob(job.JobBase):
    MAX_RETRIES = 3
    TIMEOUT = 10
    
    def _retrieve_source_configuration(self, source_id):
        source = db.session.query(DataSource).filter(DataSource.id == source_id).one()
        source_configuration = source.config

        source_configuration['type'] = source.type
        source_configuration['start_date'] = str(self.last_run)

        return source_configuration

    def _create_pipeline(self, source):
        pipeline = Pipe.from_configuration(
            sources=[source],
        )
        pipeline.destinations = [msi_pipeline]
        return pipeline

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

        source = self._retrieve_source_configuration(datasource_id)
        source['only'] = 'schema'

        collector_pipeline = self._create_pipeline(source)
        collector_pipeline.run()

