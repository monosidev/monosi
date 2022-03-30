from abc import abstractmethod
from ingestion.collector import Collector

from scheduler import job
from telemetry.events import track_event

from server.models import DataSource
from server.middleware.db import db


class CollectorJob(job.JobBase):
    MAX_RETRIES = 3
    TIMEOUT = 10
    
    def _retrieve_source_configuration(self, source_id):
        source = db.session.query(DataSource).filter(DataSource.id == source_id).one()
        source_configuration = source.config

        source_configuration['type'] = source.type
        source_configuration['start_date'] = str(self.last_run) if self.last_run else None

        return source_configuration

    def _create_collector(self, source, pipelines, configuration):
        collector = Collector.from_configuration(
            source_dict=source,
            pipelines=pipelines,
            configuration=configuration,
        )
        return collector

    @classmethod
    def meta_info(cls):
        return {
            'job_class_string': '%s.%s' % (cls.__module__, cls.__name__),
            'notes': ('This ingests metadata from the source specified.'),
            'arguments': [
                {'type': 'integer', 'description': 'The ID of the datasource from which to ingest metadata.'},
            ],
        }

    @abstractmethod
    def pipelines(self):
        raise NotImplementedError

    @abstractmethod
    def configuration(self):
        raise NotImplementedError

    def run(self, datasource_id, *args, **kwargs):
        track_event(action="metadata_ingestion_start", label="server")

        source = self._retrieve_source_configuration(datasource_id)

        collector_pipeline = self._create_collector(source, self.pipelines(), self.configuration())
        collector_pipeline.run()





