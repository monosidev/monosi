import abc
from dataclasses import dataclass, field
from enum import Enum
from mashumaro import DataClassDictMixin
from typing import Any, List, Optional, Dict

from .metrics import MetricBase

class MonitorType(Enum):
    TABLE = 'table'
    CUSTOM = 'custom'

class ScheduleType(Enum):
    INTERVAL = 'interval'

@dataclass
class Schedule(DataClassDictMixin):
    minutes: int = 720
    type: ScheduleType = ScheduleType.INTERVAL

@dataclass
class Monitor:
    metrics: List[MetricBase]
    description: Optional[str] = None
    schedule: Schedule = field(default_factory=Schedule)

    def base_sql_statement(self, select_sql):
        raise NotImplementedError

    def retrieve_metrics(self):
        raise NotImplementedError

    @abc.abstractmethod
    def info(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def validate(cls, monitor_dict):
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'Monitor':
        raise NotImplementedError
