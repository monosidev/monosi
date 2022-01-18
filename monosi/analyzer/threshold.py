from dataclasses import dataclass, field
from typing import List
from monosi.analyzer.data import DataPoint

from monosi.monitors.custom import CustomMetric, Threshold

from .data import Data, Test, TestResult

@dataclass
class ThresholdTest(Test):
    thresholds: List[Threshold]
    anomalies: List[DataPoint] = field(default_factory=list)

    def run(self):
        for point in self.data:
            for threshold in self.thresholds:
                point.error = threshold.evaluate(point.value)

        result = TestResult(self.data)
        self.anomalies = result.anomalies()

        return result

    @classmethod
    def from_metric(cls, metric: CustomMetric, data: Data):
        return cls(
            data=data.for_metric(metric),
            thresholds=metric.thresholds,
            column=metric.alias(),
            metric=metric.type.value,
        )

