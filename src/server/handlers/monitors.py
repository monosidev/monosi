from flask_restful import abort
from sqlalchemy import func

from server.models import Metric, Monitor
from server.middleware.db import db

from .base import CrudResource, ListResource

class MonitorListResource(ListResource):
    @property
    def resource(self):
        raise NotImplemented

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
            'created_at': obj[8].strftime("%b %d, %Y %H:%M:%S"),
        }

    def _all(self):
        try:
            objs = db.session.query(
                    func.count(func.concat(Metric.metric, Metric.column_name).distinct()),
                    Monitor.id,
                    Monitor.table_name,
                    Monitor.database,
                    Monitor.schema,
                    Monitor.type,
                    Monitor.source,
                    Monitor.workspace,
                    Monitor.created_at
                ).outerjoin(
                    Metric,
                    (Monitor.table_name==Metric.table_name) &
                    (Monitor.database==Metric.database) &
                    (Monitor.schema==Metric.schema)
                ).group_by(
                    Monitor.id,
                    Monitor.table_name,
                    Monitor.database,
                    Monitor.schema,
                    Monitor.type,
                    Monitor.source,
                    Monitor.workspace,
                    Monitor.created_at
                ).all()
        except:
            abort(500)
        return [self._transform(obj) for obj in objs]

    def post(self): # Disable creation
        abort(500)


class MonitorResource(CrudResource):
    @property
    def resource(self):
        return Monitor

    @property
    def key(self):
        return "monitor"
