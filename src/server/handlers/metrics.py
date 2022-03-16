import logging
from flask_restful import Resource, abort, request
from sqlalchemy import func

from server.models import Metric
from server.middleware.db import db



# class MetricListResource(Resource):


#     def _validate(self, req):
#         pass
#         # return self.resource.validate(req)

#     def get(self, **kwargs):
#         try:
#             database = kwargs['database']
#             schema = kwargs['schema']
#             table = kwargs['table']
#         except:
#             abort(404)

#         obj = self._retrieve_by_kwargs(table, database, schema)

#         return {self.key: obj}


class MetricListResource(Resource):
    @property
    def key(self):
        return "metrics"

    def _transform(self, objs):
        return [
            {
                'metric': obj[0],
                'column_name': obj[1],
                'count': obj[2],
            }
            for obj in objs
        ]
#
    def _retrieve_by_kwargs(self, table_name, database, schema):
        try:
            obj = db.session.query(
                    Metric.metric,
                    Metric.column_name,
                    func.count(Metric.id),
                    Metric.table_name,
                    Metric.database,
                    Metric.schema,
                    func.max(Metric.created_at)
                ).filter(
                    table_name == Metric.table_name,
                    database == Metric.database,
                    schema == Metric.schema
                ).group_by(
                    Metric.table_name, 
                    Metric.database, 
                    Metric.schema,
                    Metric.column_name,
                    Metric.metric,
                ).all()
        except:
            abort(404)
        return {'table_name': table_name, 'database': database, 'schema': schema, 'type': 'table_health', 'metrics': obj}

    def _retrieve_detailed(self, table_name, database, schema, column_name, metric):
        try:
            # objs = db.session.query(Metric, ZScore).outerjoin(ZScore, ZScore.metric_id == Metric.id).filter(
            objs = db.session.query(Metric).filter(
                Metric.table_name==table_name,
                Metric.database==database,
                Metric.schema==schema,
                Metric.metric == metric,
                Metric.column_name == column_name
            ).all() # TODO: ORDER BY
            # metrics = [(lambda d: (d.update(obj[1].to_dict()) or d) if obj[1] else d)(obj[0].to_dict()) for obj in objs]
            metrics = [m.to_dict() for m in objs]
            print(metrics)
        except Exception as e:
            logging.warn(e)
            abort(404)
        return metrics


    # Entrypoint
    def get(self, database, schema, table_name):
        if 'column_name' in request.args and 'metric' in request.args:
            return self.get_detail(table_name, database, schema, request.args)

        obj_list = self._retrieve_by_kwargs(table_name, database, schema)
        transformed_obj_list = self._transform(obj_list['metrics'])

        return {self.key: transformed_obj_list}

    def get_detail(self, table_name, database, schema, args):
        column_name = args.get('column_name')
        metric = args.get('metric')

        metrics = self._retrieve_detailed(table_name, database, schema, column_name, metric)

        return {'metrics': metrics}

# class MetricResource(Resource):
#     @property
#     def key(self):
#         return "metrics"

#     def _retrieve_by_monitor_and_name(self, monitor, name):
#         try:
#             obj = db.session.query(Metric).filter(
#                 Metric.table_name == ".".join([monitor['database'], monitor['schema'], monitor['table_name']]),
#                 Metric.metric == name,
#             )
#         except Exception as e:
#             logging.warn(e)
#             abort(404)
#         return obj

#     def get(self, **kwargs):
#         obj_id = kwargs['obj_id']
#         metric_name = kwargs['metric_name']

#         monitor_resource = MonitorResource()
#         monitor = monitor_resource.get(obj_id=obj_id)['monitor']

#         obj_list = self._retrieve_by_monitor_and_name(monitor, metric_name)
#         obj_dict_list = [obj.to_dict() for obj in obj_list]

#         return {self.key: obj_dict_list}

