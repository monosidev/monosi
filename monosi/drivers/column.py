from dataclasses import dataclass
from enum import Enum

class ColumnDataType(Enum):
    STRING = 'string'
    DATE = 'date'
    DATETIME = 'datetime'
    INTEGER = 'integer'
    FLOAT = 'float'
    BOOLEAN = 'boolean'

@dataclass
class Column:
    name: str
    data_type: ColumnDataType
