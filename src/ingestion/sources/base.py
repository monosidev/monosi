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
    def schema_tables_query(cls, database_name, schema_name):
        raise NotImplementedError

    @classmethod
    def schema_columns_query(cls, database_name, schema_name):
        raise NotImplementedError

    @classmethod
    def table_metrics_query(cls):
        raise NotImplementedError

    @classmethod
    def access_logs_query(cls):
        raise NotImplementedError
        
    @classmethod
    def copy_and_load_logs_query(cls):
        raise NotImplementedError


@dataclass
class SQLAlchemySource(Source):
    dialect: SQLAlchemySourceDialect

    def _columns_schema(self, _) -> TaskUnit:
        return self.dialect.schema_columns_query(
            database_name=self.configuration.database(),
            schema_name=self.configuration.schema(),
        )

    def _tables_schema(self, _) -> TaskUnit:
        return self.dialect.schema_tables_query(
            database_name=self.configuration.database(),
            schema_name=self.configuration.schema(),
        )

    def _metrics(self, discovery_data) -> List[TaskUnit]:
        # tables = [row.get('TABLE_NAME') for row in discovery_data['rows']]
        # Filter nulls

        print(discovery_data)
        return "SELECT 1"
        # return [MultiTaskUnit(request=self.dialect.table_metrics_query()) for table in tables]

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
            TaskUnit(request=self._metrics),
            # TaskUnit(request=self._access_logs),
            # TaskUnit(request=self._copy_and_load_logs),
        ]

        return units

