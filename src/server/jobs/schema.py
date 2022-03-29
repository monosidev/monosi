from server.pipeline import monitors_pipeline

from .base import CollectorJob


class SchemaCollectorJob(CollectorJob):
    def pipelines(self):
        return [monitors_pipeline]

    def configuration(self):
        return { 'monitors': [ { 'type': 'schema' } ] }

