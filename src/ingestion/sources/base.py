from dataclasses import dataclass
from sqlalchemy import create_engine
from typing import Any, Dict, List, Optional
import abc
import json

from ingestion.task import Task, TaskUnit


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
    def run(self, request: str):
        raise NotImplementedError


# Base SQL

class SQLAlchemyExtractor(Extractor):
    def __init__(self, configuration):
        self.configuration = configuration
        self.engine = None
        self.connection = None

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

    def _initialize(self):
        if self.engine and self.connection:
            return

        self.engine = self._create_engine()
        self.connection = self.engine.connect()

    def _execute(self, sql: str):
        if not self.connection:
            raise Exception("Connection has already been closed. Could not execute.")

        return self.connection.execute(sql)

    def run(self, unit: TaskUnit):
        self._initialize()

        cs = self._execute(unit.request)
        results = self._retrieve_results(cs)

        return results

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
        return cls._numeric_mean().format("LENGTH({})")

    @classmethod
    def _max_length(cls):
        return cls._numeric_max().format("LENGTH({})")

    @classmethod
    def _min_length(cls):
        return cls._numeric_min().format("LENGTH({})")

    @classmethod
    def _std_length(cls):
        return cls._numeric_std().format("LENGTH({})")

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
    def schema_query(cls):
        return """
            SELECT
                lower(c.table_name) AS name,
                lower(c.column_name) AS col_name,
                lower(c.data_type) AS col_type,
                c.comment AS col_description,
                lower(c.ordinal_position) AS col_sort_order,
                lower(c.table_catalog) AS database,
                lower(c.table_schema) AS schema,
                t.comment AS description,
                decode(lower(t.table_type), 'view', 'true', 'false') AS is_view
            FROM
                {database_name}.INFORMATION_SCHEMA.COLUMNS AS c
            LEFT JOIN
                {database_name}.INFORMATION_SCHEMA.TABLES t
                    ON c.TABLE_NAME = t.TABLE_NAME
                    AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
            WHERE LOWER( name ) = '{table_name}'
              AND LOWER( schema ) = '{schema_name}'
        """

    @classmethod
    def table_metrics_query(cls):
        raise NotImplementedError

    @classmethod
    def query_access_logs_query(cls):
        raise NotImplementedError
        
    @classmethod
    def query_copy_logs_query(cls):
        raise NotImplementedError


@dataclass
class SQLAlchemySource(Source):
    dialect: SQLAlchemySourceDialect

    def _schema(self) -> TaskUnit:
        schema_query = self.dialect.schema_query().format(
            database_name=self.configuration.database(),
            schema_name=self.configuration.schema(),
            table_name='orders'
        )
        return TaskUnit(request=schema_query)

    def _metrics(self) -> List[TaskUnit]:
        tables = [] # TODO: Get for all tables
        return [TaskUnit(request=self.dialect.table_metrics_query()) for table in tables]

    def _query_access_logs(self) -> TaskUnit:
        return TaskUnit(request=self.dialect.query_access_logs_query())

    def _query_copy_logs(self) -> TaskUnit:
        return TaskUnit(request=self.dialect.query_copy_logs_query())

    def extractor(self):
        raise NotImplementedError

    def task_units(self) -> List[TaskUnit]:
        units = [
            self._schema(),
            # self._query_access_logs(),
            # self._query_copy_logs()
        ]
        [units.append(unit) for unit in self._metrics()]

        return units

