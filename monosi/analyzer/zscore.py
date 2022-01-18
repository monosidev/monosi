from dataclasses import dataclass, field
from math import sqrt
from typing import List
from monosi.analyzer.data import DataPoint

from monosi.monitors.table import ColumnMetric

from .data import Data, Test, TestResult, TableDataPoint

@dataclass
class ZScoreDataPointFields:
    expected_range_start: float
    expected_range_end: float
    z_score: float

@dataclass
class ZScoreDataPoint(TableDataPoint, ZScoreDataPointFields):
    pass

class ZScoreTestResult(TestResult):
    data: List[ZScoreDataPoint]

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
                    expected_range_start=point.value-sensitivity,
                    expected_range_end=point.value+sensitivity,
                    error=error,
                    z_score=z_score,
                )
                zscore_points.append(zscore_point)

            except Exception as e:
                pass
                # return []

        return zscore_points

@dataclass
class ZScoreTest(Test):
    sensitivity: float = 3.0
    data: List[DataPoint]
    anomalies: List[DataPoint] = field(default_factory=list)

    @classmethod
    def from_metric(cls, metric: ColumnMetric, data: Data):
        metric_data = data.for_metric(metric)
        return cls(data=metric_data, column=metric.column, metric=metric.type.value)

    def run(self):
        z_scores = ZScoreAlgorithm.run(self.data, self.sensitivity)
        result = ZScoreTestResult(z_scores)
        self.anomalies = result.anomalies()

        return result

