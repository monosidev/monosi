import abc

from dataclasses import dataclass
import logging
from sqlalchemy import create_engine
from typing import List, Type

from .column import Column


class BaseDialect:
    @classmethod
    def approx_distinct_count(cls):
        return "COUNT(DISTINCT {})"
    
    @classmethod
    def approx_distinctness(cls):
        return "{} / CAST(COUNT(*) AS NUMERIC)".format(cls.approx_distinct_count())

    @classmethod
    def numeric_mean(cls):
        return "AVG({})"

    @classmethod
    def numeric_min(cls):
        return "MIN({})"

    @classmethod
    def numeric_max(cls):
        return "MAX({})"

    @classmethod
    def numeric_std(cls):
        return "STDDEV(CAST({} as double))"

    @classmethod
    def mean_length(cls):
        return cls.numeric_mean().format("LENGTH({})")

    @classmethod
    def max_length(cls):
        return cls.numeric_max().format("LENGTH({})")

    @classmethod
    def min_length(cls):
        return cls.numeric_min().format("LENGTH({})")

    @classmethod
    def std_length(cls):
        return cls.numeric_std().format("LENGTH({})")

@dataclass
class BaseDriverConfiguration:
    database: str
    schema: str

    def fqtn(self, table):
        table_parts = table.split('.')

        table_name = table_parts.pop()
        schema = table_parts.pop() if len(table_parts) > 0 else self.schema
        database = table_parts.pop() if len(table_parts) > 0 else self.database

        return database, schema, table_name

    @abc.abstractmethod
    def driver_name(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def configuration_schema(cls):
        raise NotImplementedError

    @abc.abstractmethod
    def connection_string(self) -> str:
        raise NotImplementedError

    @abc.abstractclassmethod
    def validate(cls, config_dict):
        raise NotImplementedError

    @classmethod
    def from_dict(cls, config_dict):
        raise NotImplementedError

    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError

@dataclass
class BaseDriver:
    configuration: BaseDriverConfiguration
    dialect: Type[BaseDialect]

    def _retrieve_type(self, type_code, scale):
        raise NotImplementedError

    def _create_columns(self, columns_and_types) -> List[Column]:
        column_names = []
        column_count = {}

        columns = []

        for column_and_type in columns_and_types:
            name = column_and_type[0]
            column_type = column_and_type[1]

            try:
                curr_count = column_count[name] + 1
            except:
                curr_count = 0
            column_count[name] = curr_count

            column_name = "{}{}".format(name, (column_count[name] if curr_count else ''))
            column_names.append(column_name)

            columns.append(Column(column_name.upper(), column_type))

        return columns

    def _retrieve_results(self, cs):
        column_and_types = [(d.name, self._retrieve_type(d.type_code, d.scale)) for d in cs.cursor.description]
        columns = self._create_columns(column_and_types)
        rows = [dict(zip([col.name for col in columns], row)) for row in cs.fetchall()]

        return {
            "columns": columns, 
            "rows": rows,
        }

    def _before_execute(self):
        pass

    @abc.abstractmethod
    def _execute(self, sql):
        raise NotImplementedError

    def execute(self, sql):
        self._before_execute()

        cs = self._execute(sql)
        results = self._retrieve_results(cs)

        return results

class BaseSqlAlchemyDriver(BaseDriver):
    def __init__(self, configuration: BaseDriverConfiguration):
        self.configuration = configuration
        self.engine = None
        self.connection = None

    def _create_engine(self):
        try:
            return create_engine(self.configuration.connection_string())
        except Exception as e:
            raise e

    def _before_execute(self):
        if self.engine and self.connection:
            return

        self.engine = self._create_engine()
        self.connection = self.engine.connect()

    def _execute(self, sql):
        if not self.connection:
            raise Exception("Connection has already been closed. Could not execute.")

        return self.connection.execute(sql)

    def close(self):
        if self.connection:
            self.connection.close()
        self.connection = None

    def test(self):
        try:
            result = self.execute("SELECT 1")
            rows = result["rows"]
            columns = result["columns"]
            return len(rows) ==1 and rows[0][columns[0].name]==1
        except Exception as e:
            logging.error(e)
            return False

    @classmethod
    def validate(cls, config_dict):
        pass
