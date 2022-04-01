import logging

from apscheduler.events import EVENT_JOB_EXECUTED
from server.middleware.db import db
from telemetry.events import track_event

from server.models import DataSource, Metric, Monitor

from .base import CrudResource, ListResource

class DataSourceResource(CrudResource):
    @property
    def resource(self):
        return DataSource

    @property
    def key(self):
        return "datasource"

    def _delete_associated(self, obj_id, model):
        ds = self._retrieve_by_id(obj_id)
        database = ds.config['database'] # TODO: If more than one source shares these, they will all be deleted.
        schema = ds.config['schema']

        objs = db.session.query(model).filter(
            model.database.ilike(f'%{database}%'),
            model.schema.ilike(f'%{schema}%'),
        ).delete(synchronize_session=False)
    
    def delete(self, obj_id):
        self._delete_associated(obj_id, Monitor)
        self._delete_associated(obj_id, Metric)
        super().delete(obj_id)

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

