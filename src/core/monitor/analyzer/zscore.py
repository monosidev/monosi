from dataclasses import dataclass, field
from math import sqrt
from typing import List
from core.monitor.models.table import ColumnMetric

from core.monitor.models.metrics import MetricBase

from .data import Data, DataPoint, Test, TestResult

class ZScoreAlgorithm:
    @classmethod
    def _mean(cls, values: List[float]):
        return round(sum(values) / len(values), 2)

    @classmethod
    def _std_dev(cls, values: List[float]):
        values_mean = cls._mean(values)

        distances = [((value - values_mean) ** 2) for value in values]
        distances_mean = cls._mean(distances)
        std_dev = round(sqrt(distances_mean), 2)

        return std_dev

    @classmethod
    def run(cls, points: List[DataPoint], sensitivity: float):
        nonnull_points = list(filter(lambda x: x.value != None, points))
        values = [point.value for point in nonnull_points]
        try:
            mean = cls._mean(values)
            std_dev = cls._std_dev(values)
        except ZeroDivisionError:
            return []

        if (std_dev == 0): return []

        zscore_points = []
        for point in nonnull_points:
            try:
                z_score = round(((point.value - mean) / std_dev), 2) 
                error = abs(z_score) > sensitivity 
                zscore_point = ZScoreDataPoint(
                    value=point.value,
                    expected_range_start=mean-(sensitivity*abs(std_dev)),
                    expected_range_end=mean+(sensitivity*abs(std_dev)),
                    error=error,
                    z_score=z_score,
                )
                zscore_points.append(zscore_point)

            except Exception as e:
                pass
                # return []

        return zscore_points

class TableDataPoint(DataPoint):
    window_start: str
    window_end: str

@dataclass
class ZScoreDataPointFields:
    expected_range_start: float
    expected_range_end: float
    z_score: float

@dataclass
class ZScoreDataPoint(TableDataPoint, ZScoreDataPointFields):
    error: bool

    def to_dict(self):
        return {
            'value': self.value,
            'range': [self.expected_range_start, self.expected_range_end],
            'error': self.error,
            'z_score': self.z_score,
            # 'window': [self.window_start, self.window_end],
        }

@dataclass
class ZscoreTestResult:
    metric: ColumnMetric
    status: bool = True
    data: List[ZScoreDataPoint] = field(default_factory=list)

    def to_dict(self):
        return {
            'data': [pt.to_dict() for pt in self.data],
            'status': self.status,
            'message': self.err_message(),
        }

    def err_message(self):
        # TODO: Needs window
        err_pts = list(filter(lambda x: x.error, self.data))

        if len(err_pts) == 0:
            return "No failures."

        msg = "\n\tColumn: {}, Metric: {}".format(self.metric.column, self.metric.type._value_)
        msg += "\n\t{} data point(s) were not within the expected range.\n".format(len(err_pts))
        for pt in err_pts:
            msg += "\n\t\tValue: {}, Expected Range: {} - {}".format(pt.value, round(pt.expected_range_start, 2), round(pt.expected_range_end, 2))

        if len(err_pts) > 5:
            msg += "\n\t\t..."

        return msg

@dataclass
class ZScoreTest(Test):
    result: ZscoreTestResult
    sensitivity: float = 3.0
    data: List[DataPoint]

    def run(self):
        self.result.data = ZScoreAlgorithm.run(self.data, self.sensitivity)
        for pt in self.result.data:
            if pt.error:
                self.result.status = False
                break

        return self.result

    @classmethod
    def from_metric(cls, metric, data: Data):
        points = data.for_metric(metric)
        return cls(data=points, result=ZscoreTestResult(metric=metric))

