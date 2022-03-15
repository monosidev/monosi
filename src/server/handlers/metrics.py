import logging
from flask_restful import Resource, abort, request
from sqlalchemy import func

from server.models import Metric, ZScore

from server.middleware.db import db
from .monitors import MonitorResource, MonitorListResource


class MetricListResource(Resource):
    def _retrieve_by_monitor(self, monitor):
        try:
            objs = db.session.query(Metric.metric, Metric.column_name, func.count(Metric.id)).filter(
                Metric.table_name==monitor['table_name'],
                Metric.database==monitor['database'],
                Metric.schema==monitor['schema'],
            ).group_by(Metric.metric, Metric.column_name).all()
            objs = [{'metric': obj[0], 'column_name': obj[1], 'count': obj[2]} for obj in objs]
        except Exception as e:
            logging.warn(e)
            abort(404)
        return objs

    @property
    def key(self):
        return "metrics"

    def get(self, obj_id):
        monitor_resource = MonitorResource()
        monitor = monitor_resource.get(obj_id=obj_id)['monitor']

        if request.args.get('column_name') and request.args.get('metric'):
            return self.get_individ(monitor, request.args)

        obj_list = self._retrieve_by_monitor(monitor)
        return {self.key: obj_list}

    def _retrieve_by_monitor_and_name(self, monitor, column_name, metric):
        try:
            objs = db.session.query(Metric, ZScore).outerjoin(ZScore, ZScore.metric_id == Metric.id).filter(
                Metric.table_name==monitor['table_name'],
                Metric.database==monitor['database'],
                Metric.schema==monitor['schema'],
                Metric.metric == metric,
                Metric.column_name == column_name
            ).all() # TODO: ORDER BY
            metrics = [(lambda d: (d.update(obj[1].to_dict()) or d) if obj[1] else d)(obj[0].to_dict()) for obj in objs]
        except Exception as e:
            logging.warn(e)
            abort(404)
        return metrics

    def get_individ(self, monitor, args):
        column_name = args.get('column_name')
        metric = args.get('metric')

        metrics = self._retrieve_by_monitor_and_name(monitor, column_name, metric)
        return {'metrics': metrics}

class MetricResource(Resource):
    @property
    def key(self):
        return "metrics"

    def _retrieve_by_monitor_and_name(self, monitor, name):
        try:
            obj = db.session.query(Metric).filter(
                Metric.table_name == ".".join([monitor['database'], monitor['schema'], monitor['table_name']]),
                Metric.metric == name,
            )
        except Exception as e:
            logging.warn(e)
            abort(404)
        return obj

    def get(self, **kwargs):
        obj_id = kwargs['obj_id']
        metric_name = kwargs['metric_name']

        monitor_resource = MonitorResource()
        monitor = monitor_resource.get(obj_id=obj_id)['monitor']

        obj_list = self._retrieve_by_monitor_and_name(monitor, metric_name)
        obj_dict_list = [obj.to_dict() for obj in obj_list]

        return {self.key: obj_dict_list}

