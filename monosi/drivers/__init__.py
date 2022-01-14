import abc
from dataclasses import dataclass
from typing import List, Optional, Type

from .column import Column
from .dialect import Dialect

@dataclass
class DriverConfig:
    schema: Optional[str] = None
    database: Optional[str] = None

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'retrieve_data') and 
                callable(subclass.retrieve_data) and 
                hasattr(subclass, 'validate') and 
                callable(subclass.validate) or 
                hasattr(subclass, 'from_dict') and 
                callable(subclass.from_dict) or 
                NotImplemented)

    @abc.abstractmethod
    def driver_name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_data(self, source_dict):
        raise NotImplementedError

    @abc.abstractmethod
    def validate(self, config_dict):
        raise NotImplementedError

    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError

    @abc.abstractmethod
    def from_dict(self, config_dict):
        raise NotImplementedError

class BaseDriver:
    dialect: Type[Dialect]

    @abc.abstractmethod
    def test_connection(self):
        raise NotImplementedError

    @abc.abstractmethod
    def describe_table(self, table):
        raise NotImplementedError

    @abc.abstractmethod
    def execute_sql(self, sql):
        raise NotImplementedError

    @abc.abstractclassmethod
    def get_compiler(cls):
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

            columns.append(Column(column_name, column_type))

        return columns

