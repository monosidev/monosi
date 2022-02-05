from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ColumnDataType(Enum):
    STRING = 'string'
    DATE = 'date'
    DATETIME = 'datetime'
    INTEGER = 'integer'
    FLOAT = 'float'
    BOOLEAN = 'boolean'

def extract_or_default(obj, key, default):
    return obj[key] if key in obj else default

def assign_if_exists(obj, key, value):
    if value:
        obj[key] = value

@dataclass
class Column:
    name: str
    data_type: ColumnDataType
    order: Optional[int] = None
    nullable: Optional[bool] = None
    primary: Optional[bool] = None
    unique: Optional[bool] = None

    @classmethod
    def from_dict(cls, col_dict):
        return cls(
            name=col_dict['name'],
            data_type=ColumnDataType(col_dict['type']),
            order=extract_or_default(col_dict, 'order', None),
            nullable=extract_or_default(col_dict, 'nullable', None),
            primary=extract_or_default(col_dict, 'primary', None),
            unique=extract_or_default(col_dict, 'unique', None),
        )

    def to_dict(self):
        col_dict = {
            'name': self.name,
            'type': self.data_type._value_,
        }
        # TODO: Check if mutable
        assign_if_exists(col_dict, 'order', self.order)
        assign_if_exists(col_dict, 'nullable', self.nullable)
        assign_if_exists(col_dict, 'primary', self.primary)
        assign_if_exists(col_dict, 'unique', self.unique)

        return col_dict

def resolve_to_type_from_str(type_str):
    type_str = type_str.lower()
    if 'varchar' in type_str:
        return ColumnDataType.STRING
    elif 'number' in type_str or 'int' in type_str:
        return ColumnDataType.INTEGER
    elif 'date' in type_str or 'timestamp' in type_str:
        return ColumnDataType.DATE
    elif 'bool' in type_str:
        return ColumnDataType.BOOLEAN

    # TODO: Check all other types should actually resolve into strings
    return ColumnDataType.STRING

@dataclass
class Table:
    name: str
    columns: List[Column]

    def timestamp_cols(self):
        t_col_types = [ColumnDataType.DATE, ColumnDataType.DATETIME]
        cols = list(filter(lambda x: x.data_type in t_col_types, self.columns))

        return cols

    def timestamp(self):
        return self.timestamp_cols()[0]

    @classmethod
    def _insert_in_table(cls, tables, name, column):
        if name not in tables:
            table = cls(
                name=name,
                columns=[]
            )
        else:
            table = tables[name]

        table.columns.append(column)
        tables[name] = table

        return tables

    @classmethod
    def _fqtn(cls, row, name):
        return '.'.join([row['DATABASE'], row['SCHEMA'], name])

    @classmethod
    def from_metadata(cls, metadata) -> List['Table']:
        tables = {}
        for row in metadata['rows']:
            column = Column(
                name = row['COL_NAME'],
                data_type=resolve_to_type_from_str(row['COL_TYPE']),
                order=int(row['COL_SORT_ORDER'])
            )
            tables = cls._insert_in_table(tables, cls._fqtn(row, row['NAME']), column)

        return list(tables.values()) # TODO: Test me.
