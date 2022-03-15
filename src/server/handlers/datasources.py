import logging
from telemetry.events import track_event

from server.models import DataSource

from .base import CrudResource, ListResource

class DataSourceResource(CrudResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasource"

class DataSourceListResource(ListResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasources"

    def _after_create(self, sqlalc_obj):
        track_event(action="connection_created", label=sqlalc_obj.type)

    def _after_create(self, sqlalc_obj):
        try:
            from server.middleware.scheduler import manager
            manager.add_job(
                job_class_string='server.jobs.metadata.MetadataJob',
                job_id=str(sqlalc_obj.id),
                name='DataSource Ingestion: {}'.format(sqlalc_obj.name),
                args=[sqlalc_obj.id]
            )
        except Exception as e:
            logging.error("Failed to schedule monitor")
            logging.error(e)

class DataSourceTestResource(CrudResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasource"

    def _test(self, obj):
        driver = obj.db_driver()
        return driver.test()

    def get(self, **kwargs):
        obj_id = kwargs['obj_id']
        obj = self._retrieve_by_id(obj_id)

        result = self._test(obj)
        return {self.key: {"connection": result}}
