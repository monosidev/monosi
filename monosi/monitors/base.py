import abc
from dataclasses import dataclass, field
from enum import Enum
from mashumaro import DataClassDictMixin
from typing import List, Optional, Dict
from monosi.config.configuration import Configuration

from monosi.anomalies import AnomalyDetectorTest

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

    @abc.abstractmethod
    def info(self):
        raise NotImplementedError

    @abc.abstractclassmethod
    def validate(cls, monitor_dict):
        raise NotImplementedError

    @abc.abstractclassmethod
    def execute(cls, config):
        raise NotImplementedError
    
    @abc.abstractclassmethod
    def from_dict(cls, value: Dict[str, int]) -> 'Monitor':
        raise NotImplementedError

    def run(self, config: Configuration):
        reporter = config.reporter

        reporter.monitor_started(self)
        try:
            metrics = self.execute(config)
            tests = [AnomalyDetectorTest.from_metric(metric) for metric in metrics]
            [test.run(reporter) for test in tests]
        finally:
            reporter.monitor_finished(self)
            reporter.finish()

    @abc.abstractmethod
    def compile(self):
        raise NotImplementedError

