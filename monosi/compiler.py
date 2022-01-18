from dataclasses import dataclass
from typing import Any, List
from monosi.drivers.column import Column
from monosi.profiler import DatabaseTable
from monosi.monitors.table import TableMonitor

from monosi.drivers.dialect import Dialect
from monosi.monitors.base import Monitor
from monosi.monitors.metrics import MetricBase
from monosi.monitors.custom import CustomMetric
from monosi.monitors.table import ColumnMetric, ColumnMetricType

@dataclass
class Compiler:
    dialect: Dialect
    metadata: Any

    def _retrieve_unformatted_sql(self, metric_type: ColumnMetricType) -> str:
        attr = getattr(self.dialect, metric_type._value_)
        if not attr:
            raise Exception("Unreachable: Metric type is defined that does not resolve to a definition.")

        return attr()

    def _compile_column_metric(self, metric: ColumnMetric):
        alias = metric.alias()
        column = metric.column

        unformatted_metric_sql = self._retrieve_unformatted_sql(metric.type)
        formatted_metric_sql = unformatted_metric_sql.format(column)

        metric_sql = "{} AS {}".format(formatted_metric_sql, alias)
        return metric_sql

    def _compile_custom_metric(self, metric: CustomMetric):
        return metric.sql

    def compile_metric(self, metric: MetricBase):
        if isinstance(metric, ColumnMetric):
            return self._compile_column_metric(metric)
        elif isinstance(metric, CustomMetric):
            return self._compile_custom_metric(metric)
        else:
            raise Exception("Metric could not be compiled")

    def compile_select(self, metrics: List[MetricBase]):
        select_body = []
        for metric in metrics:
            metric_sql = self.compile_metric(metric)
            select_body.append(metric_sql)

        return ",\n\t".join(select_body)

    def _add_cols(self, monitor: TableMonitor):
        tables = DatabaseTable.from_metadata(self.metadata)
        for table in tables:
            if table.name.lower() in monitor.table:
                monitor.columns = table.columns

    def compile(self, monitor: Monitor):
        if isinstance(monitor, TableMonitor):
            self._add_cols(monitor)

        select_sql = self.compile_select(monitor.retrieve_metrics())
        sql = monitor.base_sql_statement(select_sql)
        
        return sql

