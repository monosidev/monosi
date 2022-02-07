import abc
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from core.common.drivers.column import Table

from core.monitor.models.metrics import MetricBase

@dataclass
class DataPoint:
    value: Any
    error: bool = False

    def to_dict(self):
        return {
            'value': self.value,
            'error': self.error,
        }

@dataclass
class Data(Table):
    points: Dict[str, List[DataPoint]]

    def for_metric(self, metric: MetricBase) :
        alias = metric.alias().lower()
        return self.points[alias]

    @classmethod
    def from_results(cls, results):
        cols = [column.name.lower() for column in results['columns']]
        points = {}
        for col in cols:
            points[col] = []

        for row in results['rows']:
            for col in row.keys():
                if row[col]:
                    try:
                        point = DataPoint(value=row[col])
                        points[col.lower()].append(point)
                    except TypeError:
                        pass
                        # logging.info("Can't convert other rows, including window_start for example.")

        try:
            tables = Table.from_metadata(results)
            if len(tables) != 1:
                raise Exception("Schema parsing failed, more than 1 or no tables.")
            columns = tables[0].columns
        except:
            columns = results['columns']
            # this is special casing for schema 
        
        return cls(
            name="intermediate-data",
            columns=columns,
            points=points
        )

@dataclass
class Anomaly:
    points: List[DataPoint] = field(default_factory=list)

@dataclass
class TestResult:
    anomalies: List[Anomaly]
    status: bool

    def to_dict(self):
        return {}

    def err_message(self):
        return ''

@dataclass
class Test:
    data: List[DataPoint]

    def anomalies(self):
        anomaly_pts = list(filter(lambda x: x.error == False, self.data))
        anomaly_objs = [Anomaly(points=[pt]) for pt in anomaly_pts]
        return anomaly_objs

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError

    @classmethod
    def from_metric(cls, metric: MetricBase, data: Data):
        raise NotImplementedError

