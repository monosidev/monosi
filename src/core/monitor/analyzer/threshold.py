from dataclasses import dataclass, field
from mashumaro import DataClassDictMixin
from typing import List

from core.monitor.models.custom import CustomMetric, Threshold
from core.monitor.models.metrics import MetricBase

from .data import Anomaly, Data, Test, TestResult


@dataclass
class ThresholdDataPoint(DataClassDictMixin):
    value: float
    operator: str
    expected: float
    error: bool

@dataclass
class ThresholdTestResult:
    metric: CustomMetric
    status: bool = True # false is err
    data: List[ThresholdDataPoint] = field(default_factory=list)

    def to_dict(self):
        return {
            'data': [pt.to_dict() for pt in self.data],
            'status': self.status,
            'message': self.err_message(),
        }

    def err_message(self):
        error_pts = list(filter(lambda x: x.error, self.data))

        if len(error_pts) == 0:
            return "No failures."

        msg = "\nSQL: {}".format(self.metric.sql)
        msg += "\n"
        msg += "The following threshold checks failed:"
        
        threshold_errs = {}
        for pt in error_pts:
            key = pt.operator + "_" + str(pt.expected)
            if key not in threshold_errs:
                threshold_errs[key] = {}
                threshold_errs[key]['operator'] = pt.operator
                threshold_errs[key]['expected'] = pt.expected
                threshold_errs[key]['actual'] = []
            threshold_errs[key]['actual'].append(pt.value)

        for threshold in threshold_errs:
            msg += "\n\n\tThreshold type: {}\n\tExpected value: {}\n\tActual (err) values: {}".format(
                threshold_errs[threshold]['operator'], 
                threshold_errs[threshold]['expected'],
                threshold_errs[threshold]['actual'])

        return msg

@dataclass
class ThresholdTest(Test):
    thresholds: List[Threshold]
    result: ThresholdTestResult

    def run(self):
        data = []
        status = True

        for point in self.data:
            for threshold in self.thresholds:
                point.error = not threshold.evaluate(point.value)

                if point.error:
                    status = False

                threshold_point = ThresholdDataPoint(
                    value=point.value,
                    operator=threshold.operator._value_,
                    expected=threshold.value,
                    error=point.error,
                )
                data.append(threshold_point)


        self.result.data = data
        self.result.status = status

        return self.result

    @classmethod
    def from_metric(cls, metric: CustomMetric, data: Data):
        return cls(
            data=data.for_metric(metric),
            thresholds=metric.thresholds,
            result=ThresholdTestResult(metric=metric)
        )
