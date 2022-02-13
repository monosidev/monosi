from dataclasses import dataclass
from typing import Any

from core.drivers.column import Table
from core.drivers.base import BaseDialect


class Runner:
    def __init__(self, config):
        self.config = config
        self.driver = None

    def _initialize(self):
        try:
            from core.drivers.factory import load_driver
            driver_cls = load_driver(self.config)

            self.driver = driver_cls(self.config)
        except Exception as e:
            print(e)
            raise Exception("Could not initialize connection to database in Runner.")

    def _execute(self, sql: str):
        if self.driver is None:
            raise Exception("Initialize runner before execution.")

        results = self.driver.execute(sql)
        return results

    def run(self, sql: str):
        self._initialize()

        return self._execute(sql)

@dataclass
class MetricsCompiler:
    metadata: Any
    dialect: BaseDialect

    def __init__(self, driver_config):
        driver = self._driver(driver_config)

        self.metadata = driver.metadata()
        self.dialect = driver.dialect

    @staticmethod
    def _driver(config):
        try:
            from core.drivers.factory import load_driver
            driver_cls = load_driver(config)

            return driver_cls(config)
        except:
            raise Exception("Could not initialize connection to database in runner.")


    def _retrieve_columns(self, table_name: str):
        tables = Table.from_metadata(self.metadata)
        for table in tables:
            if table.name.lower() in table_name.lower():
                return table.columns

    def compile_select(self, column, metric):
        alias = "{}__{}".format(column, metric.type.value)

        attr = getattr(self.dialect, metric.type._value_)
        if not attr:
            raise Exception("Unreachable: Metric type is defined that does not resolve to a definition.")

        select_unformatted = attr()
        select_no_alias = select_unformatted.format(column)
        select = "{} AS {}".format(select_no_alias, alias)

        return select

    def compile_select_body(self, columns, metrics):
        select_body = [self.compile_select(column, metric) for column, metric in zip(columns, metrics)]

        return ",\n\t".join(select_body)

    def compile_from(self, select_sql, monitor):
        return self.dialect.table_query().format(
            select_sql=select_sql,
            table=monitor.table_name,
            timestamp_field=monitor.timestamp_field,
            minutes_ago=1000,
            # minutes_ago=monitor.minutes_ago,
        )

    def compile(self, monitor):
        columns = self._retrieve_columns(monitor.table_name)
        metrics = [] # TODO get from monitor type???

        select_sql = self.compile_select(columns, metrics)
        sql = self.compile_from(select_sql, monitor)
        
        return sql


# Takes object and converts to db Results
class Extractor:
    def __init__(self, source):
        self.compiler = MetricsCompiler(source)
        self.runner = Runner(source)

    def run(self, monitor):
        compiled_sql = self.compiler.compile(monitor)
        results = self.runner.run(compiled_sql)

        return results
