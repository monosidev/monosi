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

def temp_transform_to_tests(metric_stats) -> List[AnomalyDetectorTest]:
    tests = []

    for column in metric_stats.keys():
        for metric in metric_stats[column].keys():
            values = metric_stats[column][metric]

            values: List[float] = list(filter(lambda x: x == None, values))
            test = AnomalyDetectorTest(column, metric, values)
            tests.append(test)
    
    return tests

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
            metric_stats = self.execute(config)
            metric_tests = temp_transform_to_tests(metric_stats)
            [metric_test.run(reporter) for metric_test in metric_tests]
        finally:
            reporter.monitor_finished(self)
            reporter.finish()

    @abc.abstractmethod
    def compile(self):
        raise NotImplementedError

