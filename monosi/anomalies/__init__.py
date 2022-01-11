from dataclasses import dataclass
from typing import List, Optional

from .zscore import ZScoreAlgorithm

@dataclass
class AnomalyDetectorTest:
    column: str
    metric: str
    data: List['MetricDataPoint']
    anomalies: Optional[List['Anomaly']] = None

    def run(self, reporter):
        reporter.test_started(self)
        try:
            self.anomalies = ZScoreAlgorithm.anomalies(self.data)
            result = len(self.anomalies) == 0
            if result:
                reporter.test_passed(self)
            else:
                reporter.test_failed(self)
        finally:
            reporter.test_finished(self)

    @classmethod
    def from_metric(cls, metric):
        # TODO: Deal with null values
        return cls(
            column=metric.column_name,
            metric=metric.metric_type._value_,
            data=metric.nonnull_values())
