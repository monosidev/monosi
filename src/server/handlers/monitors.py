import logging
import uuid
from core.models.monitor import MsiMonitor
from flask_restful import Resource, abort
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from core.models.monitor import MsiMonitor
from core.models.metadata.metric import MsiMetric

from server.middleware.db import db
from .base import CrudResource, ListResource

class MonitorListResource(ListResource):
    @property
    def resource(self):
        return MsiMonitor

    @property
    def key(self):
        return "monitors"

    @staticmethod
    def _transform(obj):
        return {
            'metrics': obj[0],
            'id': obj[1],
            'table_name': obj[2],
            'database': obj[3],
            'schema': obj[4],
            'type': obj[5],
            'source': obj[6],
            'workspace': obj[7],
        }

    def _all(self):
        try:
            objs = db.session.query(func.count(func.concat(MsiMetric.metric, MsiMetric.column_name).distinct()), MsiMonitor.id, MsiMonitor.table_name, MsiMonitor.database, MsiMonitor.schema, MsiMonitor.type, MsiMonitor.source, MsiMonitor.workspace).outerjoin(MsiMetric,
                (MsiMonitor.table_name==MsiMetric.table_name) &
                (MsiMonitor.database==MsiMetric.database) &
                (MsiMonitor.schema==MsiMetric.schema)
            ).group_by(MsiMonitor.id, MsiMonitor.table_name, MsiMonitor.database, MsiMonitor.schema, MsiMonitor.type, MsiMonitor.source, MsiMonitor.workspace).all()
        except:
            abort(500)
        return [self._transform(obj) for obj in objs]

    def _after_create(self, sqlalc_obj):
        try:
            logging.info("Scheduling monitor to run: {}", sqlalc_obj.to_dict())

            from server.middleware.scheduler import manager
            manager.add_job(
                job_class_string='server.jobs.monitor.MonitorJob',
                job_id=str(sqlalc_obj.id),
                name='Table Health Monitor',
                args=[sqlalc_obj.id])
        except Exception as e:
            logging.error("Failed to schedule monitor")
            logging.error(e)

class MonitorResource(CrudResource):
    @property
    def resource(self):
        return MsiMonitor

    @property
    def key(self):
        return "monitor"

    def _delete_associated_metrics(self, sqlalc_obj):
        try:
            db.session.query(MsiMetric).filter(
                MsiMetric.table_name==sqlalc_obj.table_name,
                MsiMetric.database==sqlalc_obj.database,
                MsiMetric.schema==sqlalc_obj.schema,
            ).delete(synchronize_session=False)
            db.session.commit()
        except Exception as e:
            logging.error("Failed to delete associated metrics with monitor:{}".format(sqlalc_obj.to_dict()))
            logging.error(e)

    def _delete_associated_executions(self, sqlalc_obj):
        pass

    def _after_destroy(self, sqlalc_obj):
        from server.middleware.scheduler import manager
        manager.remove_job(str(sqlalc_obj.id))
        self._delete_associated_metrics(sqlalc_obj)
        self._delete_associated_executions(sqlalc_obj)


class RunMonitorResource(Resource):
    def get(self, obj_id):
        from server.jobs.monitor import MonitorJob
        MonitorJob.run_job(obj_id, uuid.uuid4().hex, monitor_id=obj_id)

