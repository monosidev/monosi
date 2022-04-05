import logging
from flask_restful import Resource, abort, request
from sqlalchemy import func

from server.models import Metric, ZScore
from server.middleware.db import db


from .monitors import MonitorResource


# TODO: Do not format directly
METRIC_SQL_TS_DATA = """
SELECT * FROM (
    SELECT 
        value_partition, 
        hours as time_window_start, 
        hours + '1 HOUR'::INTERVAL as time_window_end, 
        first_value(value) over (partition by value_partition order by hours DESC) value,
        first_value(zscore) over (partition by value_partition order by hours DESC) zscore,
        first_value(expected_range_start) over (partition by value_partition order by hours DESC) expected_range_start,
        first_value(expected_range_end) over (partition by value_partition order by hours DESC) expected_range_end,
        first_value(error) over (partition by value_partition order by hours DESC) error
    FROM (
        SELECT
          MSI_METRICS.*,
          MSI_ZSCORES.*,
          hours,
            sum(case when value is null then 0 else 1 end) over (order by hours DESC) as value_partition
          FROM GENERATE_SERIES((
            SELECT DATE_TRUNC('HOUR', MIN(created_at - '1 DAY'::INTERVAL)) FROM MSI_MONITORS WHERE
                MSI_MONITORS.table_name ilike '{table_name}' AND
                MSI_MONITORS.database ilike '{database}' AND
                MSI_MONITORS.schema ilike '{schema}')
          , CURRENT_DATE, '1 HOUR'::INTERVAL) hours
          LEFT JOIN MSI_METRICS ON DATE_TRUNC('HOUR', MSI_METRICS.time_window_start) = hours
          AND
            MSI_METRICS.table_name ilike '{table_name}' AND
            MSI_METRICS.database ilike '{database}' AND
            MSI_METRICS.schema ilike '{schema}' AND
            MSI_METRICS.column_name ilike '{column_name}' AND
            MSI_METRICS.metric ilike '{metric}'
          LEFT JOIN MSI_ZSCORES ON MSI_ZSCORES.METRIC_ID = MSI_METRICS.ID
          ORDER BY hours DESC
    ) as metrics
) as final WHERE value is not null;
"""


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
            query = METRIC_SQL_TS_DATA.format(
                table_name=table_name,
                database=database,
                schema=schema,
                column_name=column_name,
                metric=metric
            )
            print(query)
            objs = db.session.execute(query)
            metrics = [
                {
                    'time_window_start': str(obj[1]),
                    'time_window_end': str(obj[2]),
                    'value': obj[3],
                    'zscore': obj[4],
                    'expected_range_start': obj[5],
                    'expected_range_end': obj[6],
                    'error': obj[7]
                }
            for obj in objs]
        except Exception as e:
            logging.warn(e)
            abort(404)
        return metrics

    # Entrypoint
    def get(self, monitor_id):
        monitor_resource = MonitorResource()
        monitor = monitor_resource.get(obj_id=monitor_id)['monitor']

        if 'column_name' in request.args and 'metric' in request.args:
            return self.get_detail(monitor['table_name'], monitor['database'], monitor['schema'], request.args)

        obj_list = self._retrieve_by_kwargs(monitor['table_name'], monitor['database'], monitor['schema'])
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

