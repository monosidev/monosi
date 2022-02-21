from dataclasses import dataclass
from enum import Enum
from typing import Optional
from mashumaro import DataClassDictMixin


def extract_or_default(obj, key, default):
    return obj[key] if key in obj else default

class MonitorDefinitionType(Enum):
    TABLE_HEALTH = 'table_health'
    SCHEMA = 'schema'
    VOLUME = 'volume'
    FRESHNESS = 'freshness'
    DISTRIBUTION = 'distribution'

    @classmethod
    def all(cls):
        return list(map(lambda c: c.value, cls))

@dataclass
class MonitorDefinition(DataClassDictMixin):
    type: MonitorDefinitionType
    table: str
    timestamp_field: Optional[str]

    @classmethod
    def validate(cls, def_dict):
        if 'type' not in def_dict:
            raise Exception('MonitorDefinitionError: type required.')
        elif 'table' not in def_dict:
            raise Exception('MonitorDefinitionError: table required.')

        if def_dict['type'] not in MonitorDefinitionType.all():
            raise Exception('MonitorDefinitionError: Could not find type: {}'.format(def_dict['type']))

        if def_dict['type'] == 'table_health' and 'timestamp_field' not in def_dict:
            raise Exception('MonitorDefinitionError: timestamp_field required.')

        return True

    @classmethod
    def from_dict(cls, def_dict):
        cls.validate(def_dict)
        
        return cls(
            type=MonitorDefinitionType(def_dict['type']),
            table=def_dict['table'],
            timestamp_field=extract_or_default(def_dict, 'timestamp_field', None)
        )
