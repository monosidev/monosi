from dataclasses import dataclass
from enum import Enum
import logging
from posixpath import lexists
from sqlalchemy import create_engine
from typing import Any, Dict, List, Optional
import abc
import json

from ingestion.task import MultiTaskUnit, TaskUnit


@dataclass
class SourceConfiguration:
    name: Optional[str]
    configuration: str
    enabled: bool = True

    @classmethod
    def validate(cls, configuration: str):
        raise NotImplementedError

    def connection_string(self):
        raise NotImplementedError

    @abc.abstractproperty
    def type(self):
        raise NotImplementedError

    @abc.abstractmethod
    def database(self):
        raise NotImplementedError

    @abc.abstractmethod
    def schema(self):
        raise NotImplementedError

    def to_dict(self):
        return {
            "name": self.name,
            "configuration": json.loads(self.configuration),
            "enabled": self.enabled,
            "type": self.type,
        }

@dataclass
class Source:
    configuration: SourceConfiguration

    def __init__(self, configuration: SourceConfiguration):
        self.configuration = configuration

    def _before_pull(self):
        pass

    def _after_pull(self):
        pass

    @abc.abstractmethod
    def _pull(self):
        raise NotImplementedError

    @abc.abstractmethod
    def extractor(self):
        raise NotImplementedError

    @abc.abstractmethod
    def task_units(self):
        raise NotImplementedError

    def pull(self):
        self._before_pull()
        results = self._pull()
        self._after_pull()

        return results

class Extractor(object):
    def run(self, request):
        raise NotImplementedError


# Base SQL

class SQLAlchemyExtractor(Extractor):
    def __init__(self, configuration):
        self.configuration = configuration
        self.engine = None
        self.connection = None
        self.discovered = None

    def _create_engine(self):
        try:
            return create_engine(self.configuration.connection_string())
        except Exception as e:
            raise e

    def _retrieve_results(self, cs):
        columns = [d.name for d in cs.cursor.description]
        rows = [dict(zip(columns, row)) for row in cs.fetchall()]

        return {
            "columns": columns, 
            "rows": rows,
        }

    def discovery_query(self):
        raise NotImplementedError

    def _initialize(self):
        if self.engine and self.connection and self.discovered:
            return

        self.engine = self._create_engine()
        self.connection = self.engine.connect()
        self.discovered = self._execute(self.discovery_query())

    def _execute(self, sql: str):
        if not self.connection:
            raise Exception("Connection has already been closed. Could not execute.")

        cs = self.connection.execute(sql)
        results = self._retrieve_results(cs)

        return results

    def run(self, unit: TaskUnit):
        self._initialize()

        sql = unit.request(self.discovered)
        results = self._execute(sql)

        return results

    def run_multiple(self, unit: TaskUnit):
        self._initialize()

        multiple_sql = unit.request(self.discovered)

        results = []
        for sql in multiple_sql:
            try:
                result = self._execute(sql)
                results.append(result)
            except Exception as e:
                logging.error(e)

        return results

class ColumnMetricType(Enum):
    APPROX_DISTINCTNESS = '_approx_distinctness'
    COMPLETENESS = '_completeness'
    ZERO_RATE = '_zero_rate'
    NEGATIVE_RATE = '_negative_rate'
    NUMERIC_MEAN = '_numeric_mean'
    NUMERIC_MIN = '_numeric_min'
    NUMERIC_MAX = '_numeric_max'
    NUMERIC_STD = '_numeric_std'
    APPROX_DISTINCT_COUNT = '_approx_distinct_count'
    MEAN_LENGTH = '_mean_length'
    MAX_LENGTH = '_max_length'
    MIN_LENGTH = '_min_length'
    STD_LENGTH = '_std_length'
    TEXT_INT_RATE = '_text_int_rate'
    TEXT_NUMBER_RATE = '_text_number_rate'
    TEXT_UUID_RATE = '_text_uuid_rate'
    TEXT_ALL_SPACES_RATE = '_text_all_spaces_rate'
    TEXT_NULL_KEYWORD_RATE = '_text_null_keyword_rate'

    @classmethod
    def default(cls):
        return []

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
    def default_for(cls, data_type): 
        data_type = data_type.lower()
        if data_type == 'number':
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
        elif data_type == 'text':
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

class MetricsQueryBuilder:
    def __init__(self, dialect, database, schema, ddata):
        self.dialect = dialect
        self.database = database
        self.schema = schema
        self.ddata = ddata

    def _base_query(self, select_sql, table, timestamp_field, minutes_ago=-int(0.25*24*60)):
        return """
            SELECT 
                DATE_TRUNC('HOUR', {timestamp_field}) as window_start, 
                DATEADD(hr, 1, DATE_TRUNC('HOUR', {timestamp_field})) as window_end, 
                COUNT(*) as row_count, 
                '{table}' as TABLE_NAME,
                '{database}' as DATABASE_NAME,
                '{schema}' as SCHEMA_NAME,

                {select_sql}
            FROM {table} as c
            WHERE 
                DATE_TRUNC('HOUR', {timestamp_field}) >= DATEADD(minute, {minutes_ago}, CURRENT_TIMESTAMP()) 
            GROUP BY window_start, window_end 
            ORDER BY window_start ASC;
        """.format(
            select_sql=select_sql,
            table=table,
            timestamp_field=timestamp_field,
            minutes_ago=minutes_ago,
            database=self.database,
            schema=self.schema,
        )

    def _extract_col_info(self, column):
        return column['COL_NAME'], column['COL_TYPE']

    def _transform_col_info_metric(self, col_name, metric, table_name):
        alias =  "{}__{}".format(col_name, metric._value_)
        attr = getattr(self.dialect, metric._value_)

        if not attr:
            raise Exception("Unreachable: Metric type is defined that does not resolve to a definition.")

        select_unformatted = attr()
        select_no_alias = select_unformatted.format('"{}"'.format(col_name.upper()))
        select = "{} AS {}".format(select_no_alias, alias)

        return select

    def _transform_col_info(self, col_name, col_type, table_name):
        col_sql = [self._transform_col_info_metric(col_name, metric, table_name) for metric in ColumnMetricType.default_for(col_type)]
        if len(col_sql) == 0:
            return None

        return ",\n\t".join(col_sql)

    def _col_sql(self, item, select_body):
        table_name = item['NAME']

        col_name, col_type = self._extract_col_info(item)
        col_sql = self._transform_col_info(col_name, col_type, table_name)

        if table_name not in select_body:
            select_body[table_name] = {'sql': [], 'timestamp_fields': []}

        if col_sql is not None:
            select_body[table_name]['sql'].append(col_sql)
        if col_type == 'date' or col_type == 'timestamp_tz':
            select_body[table_name]['timestamp_fields'].append(col_name)

    def _select_sql(self, ddata):
        select_body = {}

        [self._col_sql(item, select_body) for item in ddata]
        for table_name, cols in select_body.items():
            select_body[table_name] = {
                'sql': ',\n'.join(cols['sql']),
                'timestamp_fields': cols['timestamp_fields']
            }

        return select_body

    def _timestamp_field(self, cols): # TODO: Improve
        if len(cols['timestamp_fields']) == 0:
            return None

        return cols['timestamp_fields'][0]

    def compile(self) -> List[str]:
        metrics_queries = []

        select_sql = self._select_sql(self.ddata['rows'])
        for table_name, cols in select_sql.items():
            cols_sql = cols['sql']
            timestamp_field = self._timestamp_field(cols)

            if timestamp_field is not None:
                metrics_queries.append(self._base_query(
                    cols_sql,
                    table_name,
                    timestamp_field,
                ))

        return metrics_queries


class SQLAlchemySourceDialect:
    @classmethod
    def _approx_distinct_count(cls):
        return "COUNT(DISTINCT {})"
    
    @classmethod
    def _approx_distinctness(cls):
        return "{} / CAST(COUNT(*) AS NUMERIC)".format(cls._approx_distinct_count())

    @classmethod
    def _numeric_mean(cls):
        return "AVG({})"

    @classmethod
    def _numeric_min(cls):
        return "MIN({})"

    @classmethod
    def _numeric_max(cls):
        return "MAX({})"

    @classmethod
    def _numeric_std(cls):
        return "STDDEV(CAST({} as double))"

    @classmethod
    def _mean_length(cls):
        return "AVG(LENGTH({}))"

    @classmethod
    def _max_length(cls):
        return "MAX(LENGTH({}))"

    @classmethod
    def _min_length(cls):
        return "MIN(LENGTH({}))"

    @classmethod
    def _std_length(cls):
        return "STDDEV(CAST(LENGTH({}) as double))"

    @classmethod
    def _text_int_rate(cls):
        raise NotImplementedError

    @classmethod
    def _text_number_rate(cls):
        raise NotImplementedError

    @classmethod
    def _text_uuid_rate(cls):
        raise NotImplementedError

    @classmethod
    def text_all_spaces_rate(cls):
        raise NotImplementedError

    @classmethod
    def _text_null_keyword_rate(cls):
        raise NotImplementedError

    @classmethod
    def _zero_rate(cls):
        raise NotImplementedError

    @classmethod
    def _negative_rate(cls):
        raise NotImplementedError

    @classmethod
    def _completeness(cls):
        raise NotImplementedError

    @classmethod
    def schema_tables_query(cls, database_name, schema_name):
        raise NotImplementedError

    @classmethod
    def schema_columns_query(cls, database_name, schema_name):
        raise NotImplementedError

    @classmethod
    def table_metrics_query(cls, configuration, discovery_data):
        builder = MetricsQueryBuilder(cls, configuration.database(), configuration.schema(), discovery_data)
        queries = builder.compile()
        return queries

    @classmethod
    def access_logs_query(cls):
        raise NotImplementedError
        
    @classmethod
    def copy_and_load_logs_query(cls):
        raise NotImplementedError


@dataclass
class SQLAlchemySource(Source):
    dialect: SQLAlchemySourceDialect

    def _columns_schema(self, _) -> str:
        return self.dialect.schema_columns_query(
            database_name=self.configuration.database(),
            schema_name=self.configuration.schema(),
        )

    def _tables_schema(self, _) -> str:
        return self.dialect.schema_tables_query(
            database_name=self.configuration.database(),
            schema_name=self.configuration.schema(),
        )

    def _metrics(self, discovery_data) -> List[str]:
        return self.dialect.table_metrics_query(self.configuration, discovery_data)
        # return [TaskUnit(request=self.dialect.table_metrics_query()) for table in tables]

    def _access_logs(self, _) -> TaskUnit:
        return self.dialect.access_logs_query()

    def _copy_and_load_logs(self, _) -> TaskUnit:
        return self.dialect.copy_and_load_logs_query()

    def extractor(self):
        raise NotImplementedError

    def task_units(self) -> List[TaskUnit]:
        units = [
            # TaskUnit(request=self._columns_schema),
            # TaskUnit(request=self._tables_schema),
            MultiTaskUnit(request=self._metrics),
            # TaskUnit(request=self._access_logs),
            # TaskUnit(request=self._copy_and_load_logs),
        ]

        return units

