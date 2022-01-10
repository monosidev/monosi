from dataclasses import dataclass
from math import sqrt
from typing import List

from .zscore import ZScoreAlgorithm

@dataclass
class AnomalyDetectorTest:
    column: str
    metric: str
    values: List[float]

    def __init__(self, column, metric, values):
        self.column = column
        self.metric = metric
        self.values = values

    def run(self, reporter):
        reporter.test_started(self)
        try:
            anomalies = ZScoreAlgorithm.anomalies(self.values)
            result = len(anomalies) == 0
            if result:
                reporter.test_passed(self)
            else:
                reporter.test_failed(self)
        finally:
            reporter.test_finished(self)
