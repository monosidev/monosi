from flask_restful import abort
from sqlalchemy import func

from server.models import Metric
from server.middleware.db import db

from .base import ListResource

class MonitorListResource(ListResource):
    @property
    def resource(self):
        raise NotImplemented

    @property
    def key(self):
        return "monitors"

    @staticmethod
    def _transform(obj):
        metrics_count = obj[0]
        table_name = obj[1]
        database_name = obj[2]
        schema_name = obj[3]
        created_at = obj[4]
        metrics_id = "{}/{}/{}".format(database_name, schema_name, table_name)

        return {
            'id': metrics_id,
            'metrics': metrics_count,
            'table_name': table_name,
            'database': database_name,
            'schema': schema_name,
            'type': 'table_health',
            'created_at': str(created_at),
        }

    def _all(self):
        try:
            objs = db.session.query(
                    func.count(func.concat(Metric.metric, Metric.column_name).distinct()),
                    Metric.table_name,
                    Metric.database,
                    Metric.schema,
                    func.max(Metric.created_at)
                ).group_by(
                    Metric.table_name, 
                    Metric.database, 
                    Metric.schema
                ).all()
        except:
            abort(500)
        return [self._transform(obj) for obj in objs]

    def post(self): # Disable creation
        abort(500)

