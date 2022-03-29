import logging

from apscheduler.events import EVENT_JOB_EXECUTED
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

    def _after_destroy(self, sqlalc_obj): # Stop ingestion job
        track_event(action="connection_destroyed", label=sqlalc_obj.type)
        from server.middleware.scheduler import manager
        manager.remove_job(str(sqlalc_obj.id))
        

class DataSourceListResource(ListResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasources"

    # TODO: Move logic
    def _after_create(self, sqlalc_obj):
        track_event(action="connection_created", label=sqlalc_obj.type)
        try:
            from server.middleware.scheduler import manager
            manager.add_job(
                job_class_string='server.jobs.schema.SchemaCollectorJob',
                job_id=str(sqlalc_obj.id) + '_schema',
                name="Data Source Schema: {}".format(sqlalc_obj.name),
                args=[sqlalc_obj.id],
                trigger='date',
            )
            def start_monitoring(_): # should only fire once
                manager.add_job(
                    job_class_string='server.jobs.table_health.TableHealthCollectorJob',
                    job_id=str(sqlalc_obj.id),
                    name='Data Source Table Health: {}'.format(sqlalc_obj.name),
                    args=[sqlalc_obj.id]
                )
                manager.remove_listener(start_monitoring)

            manager.add_listener(start_monitoring, EVENT_JOB_EXECUTED) 
        except Exception as e:
            logging.error("Failed to schedule monitor")
            logging.error(e)

class DataSourceTestResource(DataSourceResource):
    def _test(self, obj):
        from ingestion.sources import SourceFactory

        source = obj.to_dict()
        configuration = source['config']
        configuration['type'] = source['type']

        source = SourceFactory.create(configuration)
        return source.test()

    def get(self, **kwargs):
        obj_id = kwargs['obj_id']
        obj = self._retrieve_by_id(obj_id)

        result = self._test(obj)
        return {self.key: {"connection": result}}

    def put(self, obj_id): # TODO: Change Error Type
        raise NotImplementedError

