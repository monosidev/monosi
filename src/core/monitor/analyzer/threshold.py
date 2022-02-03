from dataclasses import dataclass
from typing import List

from core.monitor.models.custom import CustomMetric, Threshold

from .data import Anomaly, Data, Test, TestResult

@dataclass
class ThresholdTest(Test):
    thresholds: List[Threshold]

    def run(self):
        anomalies = []

        for point in self.data:
            for threshold in self.thresholds:
                point.error = not threshold.evaluate(point.value)

                if not point.error:
                    anomaly = Anomaly(
                        points=[point],
                    )
                    anomalies.append(anomaly)

        return TestResult(anomalies)

    @classmethod
    def from_metric(cls, metric: CustomMetric, data: Data):
        return cls(
            data=data.for_metric(metric),
            thresholds=metric.thresholds,
        )
