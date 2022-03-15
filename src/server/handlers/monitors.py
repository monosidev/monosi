import logging
import uuid
from flask_restful import Resource, abort
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from server.models import Monitor, Metric
from server.middleware.db import db

from .base import CrudResource, ListResource

class MonitorListResource(ListResource):
    @property
    def resource(self):
        return Monitor

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
            objs = db.session.query(func.count(func.concat(Metric.metric, Metric.column_name).distinct()), Monitor.id, Monitor.table_name, Monitor.database, Monitor.schema, Monitor.type, Monitor.source, Monitor.workspace).outerjoin(Metric,
                (Monitor.table_name==Metric.table_name) &
                (Monitor.database==Metric.database) &
                (Monitor.schema==Metric.schema)
            ).group_by(Monitor.id, Monitor.table_name, Monitor.database, Monitor.schema, Monitor.type, Monitor.source, Monitor.workspace).all()
        except:
            abort(500)
        return [self._transform(obj) for obj in objs]

    def _validate(self, req):
        try:
            Monitor.from_dict(req)
        except:
            return False
        return True

class MonitorResource(CrudResource):
    @property
    def resource(self):
        return Monitor

    @property
    def key(self):
        return "monitor"

    def _delete_associated_metrics(self, sqlalc_obj):
        try:
            db.session.query(Metric).filter(
                Metric.table_name==sqlalc_obj.table_name,
                Metric.database==sqlalc_obj.database,
                Metric.schema==sqlalc_obj.schema,
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
