from dataclasses import dataclass
from typing import Dict, List

from monosi.monitors.metrics import MetricBase

@dataclass
class DataPoint:
    value: float
    error: bool = False

    def to_dict(self):
        return {
            'value': self.value,
            'error': self.error,
        }

class TableDataPoint(DataPoint):
    window_start: str
    window_end: str

@dataclass
class TestResult:
    data: List[DataPoint]

    def anomalies(self):
        return list(filter(lambda x: x.error == True, self.data))

@dataclass
class Data:
    points: Dict[str, List[DataPoint]]

    def for_metric(self, metric: MetricBase) :
        alias = metric.alias()
        return self.points[alias.lower()]

    @classmethod
    def anomalies(cls, points: List[DataPoint]):
        raise NotImplementedError

    @classmethod
    def from_results(cls, results):
        cols = [column.name.lower() for column in results['columns']]
        points = {}
        for col in cols:
            points[col] = []

        for row in results['rows']:
            for col in row.keys():
                if row[col]:
                    point = DataPoint(value=float(row[col]))
                    points[col.lower()].append(point)
        
        return cls(points)

@dataclass
class TableData(Data):
    points: Dict[str, List[TableDataPoint]]

    @classmethod
    def from_results(cls, results):
        return super().from_results(results)

    @classmethod
    def anomalies(cls, points: List[DataPoint]):
        pass

class CustomData(Data):
    @classmethod
    def anomalies(cls, points: List[DataPoint]):
        pass

@dataclass
class Test:
    data: List[DataPoint]

