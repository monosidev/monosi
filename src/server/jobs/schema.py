# from ingestion.collector import Collector
# from ingestion.job import Pipe

# from scheduler import job
# from telemetry.events import track_event

# from server.models import DataSource
# from server.middleware.db import db
# from server.pipeline import msi_pipeline




# class SchemaJob(CollectorJob):

#     def _create_collector(self, source):
#         collector = Collector.from_configuration(
#             source_dict=source,
#             filters=self._create_filters(),
#         )
#         collector.pipelines = [msi_pipeline]
#         return collector

