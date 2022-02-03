import logging
from dataclasses import dataclass, field
from typing import Any, List, Dict

from core.monitor.models.schema import SchemaMetric, SchemaMetricType

from .data import Anomaly, Data, Test, TestResult

@dataclass
class SchemaComparisonTest(Test):
    expected: Dict[str, Any]
    data: Dict[str, Any]
    _anomalies: List[Anomaly] = field(default_factory=list)

    @classmethod
    def from_metric(cls, metric: SchemaMetric, schema: Data):
        actual_col_to_metric = {}
        for col in schema.columns:
            actual_col_to_metric[col.name] = getattr(col, metric.type._value_)

        return cls(
            expected=metric.col_to_metric,
            data=actual_col_to_metric,
        )

    def anomalies(self):
        return self._anomalies

    def run(self):
        expected_cols = self.expected.keys()
        actual_cols = self.data.keys()

        for col in expected_cols:
            try:
                if self.expected[col] != self.data[col]:
                    anomaly = Anomaly()
                    self._anomalies.append(anomaly)
            except Exception as e:
                self._anomalies.append(Anomaly())
                logging.warn("Likely a column missing, should be considered an anomaly")

        return TestResult(self._anomalies)

