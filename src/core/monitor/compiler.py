from dataclasses import dataclass
from typing import Any, List

from core.common.drivers.column import Table
from core.common.drivers.base import BaseDialect

from core.monitor.models.metrics import MetricBase
from core.monitor.models.table import TableMonitor, ColumnMetric, ColumnMetricType

@dataclass
class Compiler:
    dialect: BaseDialect
    metadata: Any

    @staticmethod
    def _driver(config):
        try:
            from core.common.drivers.factory import load_driver
            driver_cls = load_driver(config)

            return driver_cls(config)
        except:
            raise Exception("Could not initialize connection to database in runner.")

    def __init__(self, driver_config):
        driver = self._driver(driver_config)
        self.metadata = driver.metadata()
        self.dialect = driver.dialect

    def compile_metric(self, metric: MetricBase):
        return metric.compile(self.dialect)

    def compile_select(self, metrics: List[MetricBase]):
        select_body = []
        for metric in metrics:
            metric_sql = self.compile_metric(metric)
            select_body.append(metric_sql)

        return ",\n\t".join(select_body)

    def _add_cols(self, monitor: TableMonitor):
        tables = Table.from_metadata(self.metadata)
        for table in tables:
            if table.name.lower() in monitor.table.lower():
                monitor.columns = table.columns

    def compile(self, monitor):
        if isinstance(monitor, TableMonitor):
            self._add_cols(monitor)

        select_sql = self.compile_select(monitor.retrieve_metrics())
        sql = monitor.base_sql_statement(select_sql, self.dialect)
        
        return sql

