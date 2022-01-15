from dataclasses import dataclass
from typing import List

from monosi.monitors.custom import CustomMetric, Threshold

from .data import Data, Test, TestResult

@dataclass
class ThresholdTest(Test):
    thresholds: List[Threshold]

    def run(self):
        for point in self.data:
            for threshold in self.thresholds:
                point.error = threshold.evaluate(point.value)

        return TestResult(self.data)

    @classmethod
    def from_metric(cls, metric: CustomMetric, data: Data):
        return cls(
            data=data.for_metric(metric),
            thresholds=metric.thresholds,
        )

