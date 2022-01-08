import abc
from dataclasses import dataclass, field
from enum import Enum
from mashumaro import DataClassDictMixin
from typing import Optional, Dict

class MonitorType(Enum):
    TableMetrics = 'table_metrics'

class ScheduleType(Enum):
    INTERVAL = 'interval'

@dataclass
class Schedule(DataClassDictMixin):
    minutes: int = 720
    type: ScheduleType = ScheduleType.INTERVAL

@dataclass
class Monitor(DataClassDictMixin):
    description: Optional[str] = None
    schedule: Schedule = field(default_factory=Schedule)

    @abc.abstractclassmethod
    def validate(cls, monitor_dict):
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def from_dict(cls, value: Dict[str, int]) -> 'Monitor':
        raise NotImplementedError

    @abc.abstractmethod
    def compile(self):
        raise NotImplementedError

