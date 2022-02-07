import logging
from dataclasses import dataclass, field
from mashumaro import DataClassDictMixin
from typing import Any, List, Dict

from core.monitor.models.schema import SchemaMetric, SchemaMetricType

from .data import Anomaly, Data, Test, TestResult


@dataclass
class SchemaDataPoint(DataClassDictMixin):
    value: Any
    expected: Any
    col: str
    error: bool

@dataclass
class SchemaTestResult:
    metric: SchemaMetric
    status: bool = True # false is err
    data: List[SchemaDataPoint] = field(default_factory=list)

    def to_dict(self):
        return {
            'data': [pt.to_dict() for pt in self.data],
            'status': self.status,
            'message': self.err_message(),
        }

    def err_message(self):
        err_pts = list(filter(lambda x: x.error, self.data))

        if len(err_pts) == 0:
            return "No failures."

        msg = ""
        for pt in err_pts:
            msg += "\n\tColumn: {}, Metric: {}".format(pt.col, self.metric.type._value_)
            for pt in err_pts:
                msg += "\n\t\tValue: {}, Expected: {}\n".format(pt.value, pt.expected)

        return msg

@dataclass
class SchemaComparisonTest(Test):
    expected: Dict[str, Any]
    data: Dict[str, Any]
    result: SchemaTestResult
    _anomalies: List[Anomaly] = field(default_factory=list)

    @classmethod
    def from_metric(cls, metric: SchemaMetric, schema: Data):
        actual_col_to_metric = {}
        for col in schema.columns:
            actual_col_to_metric[col.name] = getattr(col, metric.type._value_)

        return cls(
            expected=metric.col_to_metric,
            data=actual_col_to_metric,
            result=SchemaTestResult(metric=metric),
        )

    def anomalies(self):
        return self._anomalies

    def run(self):
        expected_cols = self.expected.keys()
        actual_cols = self.data.keys()

        pts = []
        status = True
        for col in expected_cols:
            try:
                pt = SchemaDataPoint(
                    expected=self.expected[col],
                    value=self.data[col],
                    error=(self.expected[col] != self.data[col]),
                    col=col,
                )
                if pt.error:
                    status = False
                pts.append(pt)
            except Exception as e:
                pt = SchemaDataPoint(
                    expected=self.expected[col],
                    value=None,
                    error=True,
                    col=col,
                )
                if pt.error:
                    status = False
                pts.append(pt)

        self.result.data = pts
        self.result.status = status

        return self.result

