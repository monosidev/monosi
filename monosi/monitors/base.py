import abc
from dataclasses import dataclass
from enum import Enum
from mashumaro import DataClassDictMixin
from typing import Optional, Dict

class MonitorType(Enum):
    TableMetrics = 'table_metrics'

@dataclass
class Monitor(DataClassDictMixin):
    description: Optional[str] = None

    @abc.abstractclassmethod
    def validate(cls, monitor_dict):
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def from_dict(cls, value: Dict[str, int]) -> 'Monitor':
        raise NotImplementedError

    @abc.abstractmethod
    def compile(self):
        raise NotImplementedError

