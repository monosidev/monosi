from dataclasses import dataclass
from datetime import datetime
from dateutil import parser
from enum import Enum
from typing import Any

from core.drivers.column import ColumnDataType, Table
from core.drivers.base import BaseDialect, BaseDriverConfiguration


class ColumnMetricType(Enum):
    APPROX_DISTINCTNESS = 'approx_distinctness'
    COMPLETENESS = 'completeness'
    ZERO_RATE = 'zero_rate'
    NEGATIVE_RATE = 'negative_rate'
    NUMERIC_MEAN = 'numeric_mean'
    NUMERIC_MIN = 'numeric_min'
    NUMERIC_MAX = 'numeric_max'
    NUMERIC_STD = 'numeric_std'
    APPROX_DISTINCT_COUNT = 'approx_distinct_count'
    MEAN_LENGTH = 'mean_length'
    MAX_LENGTH = 'max_length'
    MIN_LENGTH = 'min_length'
    STD_LENGTH = 'std_length'
    TEXT_INT_RATE = 'text_int_rate'
    TEXT_NUMBER_RATE = 'text_number_rate'
    TEXT_UUID_RATE = 'text_uuid_rate'
    TEXT_ALL_SPACES_RATE = 'text_all_spaces_rate'
    TEXT_NULL_KEYWORD_RATE = 'text_null_keyword_rate'

    @classmethod
    def default(cls):
        return [cls.APPROX_DISTINCTNESS, cls.COMPLETENESS]

    @classmethod
    def all(cls):
        return [
            cls.APPROX_DISTINCTNESS, 
            cls.COMPLETENESS,
            cls.ZERO_RATE,
            cls.NEGATIVE_RATE,
            cls.NUMERIC_MEAN,
            cls.NUMERIC_MIN,
            cls.NUMERIC_MAX,
            # cls.NUMERIC_STD,
            cls.APPROX_DISTINCT_COUNT,
            cls.MEAN_LENGTH,
            cls.MAX_LENGTH,
            cls.MIN_LENGTH,
            # cls.STD_LENGTH,
            cls.TEXT_INT_RATE,
            cls.TEXT_NUMBER_RATE,
            cls.TEXT_UUID_RATE,
            cls.TEXT_ALL_SPACES_RATE,
            cls.TEXT_NULL_KEYWORD_RATE,
        ]

    @classmethod
    def default_for(cls, data_type: ColumnDataType): 
        if data_type == ColumnDataType.FLOAT or data_type == ColumnDataType.INTEGER:
            return [
                cls.ZERO_RATE,
                cls.NEGATIVE_RATE,
                cls.NUMERIC_MEAN,
                cls.NUMERIC_MIN,
                cls.NUMERIC_MAX,
                # cls.NUMERIC_STD,
                cls.COMPLETENESS,
                cls.APPROX_DISTINCTNESS,
            ]
        elif data_type == ColumnDataType.STRING:
            return [
                cls.APPROX_DISTINCT_COUNT,
                cls.MEAN_LENGTH,
                cls.MAX_LENGTH,
                cls.MIN_LENGTH,
                # cls.STD_LENGTH,
                cls.TEXT_INT_RATE,
                cls.TEXT_NUMBER_RATE,
                cls.TEXT_UUID_RATE,
                cls.TEXT_ALL_SPACES_RATE,
                cls.TEXT_NULL_KEYWORD_RATE,
                cls.COMPLETENESS,
                cls.APPROX_DISTINCTNESS,
            ]
            

        return cls.default()

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
    driver_config: BaseDriverConfiguration

    def _minutes_ago(self, default, monitor_id):
        try:
            driver = self._driver(self.destination_config)
            sql = "SELECT * FROM msi_executions WHERE monitor_id = {} AND state = 5 ORDER BY created_at DESC LIMIT 1;".format(monitor_id)
            results = driver.execute(sql)
        except:
            return default

        if len(results['rows']) == 0:
            return default

        window_start = results['rows'][0].get('CREATED_AT') or results['rows'][0].get('created_at')

        return int((datetime.now() - window_start.replace(tzinfo=None)).seconds / 60)

    def __init__(self, driver_config, destination):
        driver = self._driver(driver_config)

        self.driver_config = driver_config
        self.destination_config = destination
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
        alias = "{}__{}".format(column.name, metric._value_)

        attr = getattr(self.dialect, metric._value_)
        if not attr:
            raise Exception("Unreachable: Metric type is defined that does not resolve to a definition.")

        select_unformatted = attr()
        select_no_alias = select_unformatted.format(column.name)
        select = "{} AS {}".format(select_no_alias, alias)

        return select

    def compile_select_body(self, columns):
        select_body = []
        for column in columns:
            for metric in ColumnMetricType.default_for(column.data_type):
                select_body.append(self.compile_select(column, metric))

        return ",\n\t".join(select_body)

    def compile_from(self, select_sql, monitor):
        return self.dialect.table_query().format(
            select_sql=select_sql,
            table=monitor.table_name,
            timestamp_field=monitor.timestamp_field,
            minutes_ago=-self._minutes_ago(10000, monitor.id),
            # minutes_ago=monitor.minutes_ago,
        )

    def compile(self, monitor):
        columns = self._retrieve_columns(monitor.fqtn())

        if columns is None:
            raise Exception("Table could not be found in current source's db and schema: ".format(monitor.fqtn()))

        select_sql = self.compile_select_body(columns)
        sql = self.compile_from(select_sql, monitor)
        
        return sql


# Takes object and converts to db Results
class Extractor:
    def __init__(self, source, destinations):
        self.compiler = MetricsCompiler(source, destinations[0])
        self.runner = Runner(source)

    def run(self, monitor):
        compiled_sql = self.compiler.compile(monitor)
        results = self.runner.run(compiled_sql)

        return results
