from dataclasses import dataclass, field
from enum import Enum
from typing import Any, List, Dict

import operator as py_operator
from monosi.monitors.base import Schedule
# from monosi.monitors.base import Schedule

from monosi.monitors.metrics import MetricType

from .base import Monitor
from .metrics import MetricBase

class ComparativeOperatorDefaults:
    EQ = 'eq'
    NE = 'ne'
    GT = 'gt'
    GE = 'ge'
    LT = 'lt'
    LE = 'le'

class PercentOperatorDefaults:
    ABS_INC = 'abs_inc'
    ABS_dec = 'abs_dec'
    REL_INC = 'rel_inc'
    REL_dec = 'rel_dec'

class Operator(ComparativeOperatorDefaults, PercentOperatorDefaults, Enum):
    EQ = 'eq'
    NE = 'ne'
    GT = 'gt'
    GE = 'ge'
    LT = 'lt'
    LE = 'le'
    ABS_INC = 'abs_inc'
    ABS_dec = 'abs_dec'
    REL_INC = 'rel_inc'
    REL_dec = 'rel_dec'

    def fn(self):
        if self._value_ in ComparativeOperatorDefaults.__dict__.values():
            return getattr(py_operator, self._value_)
        elif self._value_ in PercentOperatorDefaults.__dict__.values():
            return py_operator.iadd # TODO: Update
        
        raise Exception("Operator does not exist.")

@dataclass
class Threshold:
    operator: Operator
    value: float

    def evaluate(self, source_operand: float):
        op_fn = self.operator.fn()
        return op_fn(source_operand, self.value)

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'Threshold':
        return cls(
            operator=Operator(value['operator']),
            value=value['value'],
        )

@dataclass
class CustomMetric(MetricBase):
    sql: str = field(default_factory=str)
    thresholds: List[Threshold] = field(default_factory=list)
    type: MetricType = MetricType.CUSTOM

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'CustomMetric':
        sql = value['sql']
        thresholds: List[Threshold] = []

        for threshold_dict in value['thresholds']:
            threshold = Threshold.from_dict(threshold_dict)
            thresholds.append(threshold)

        return cls(
            sql=sql, 
            thresholds=thresholds,
        )

def extract_or_default(obj, key, default):
    return obj[key] if key in obj else default

@dataclass
class CustomMonitor(Monitor):
    metrics: List[CustomMetric] = field(default_factory=list)

    def retrieve_metrics(self):
        return self.metrics

    def info(self):
        info_str = "Custom Monitor"
        if self.description:
            info_str += ": {}".format(self.description)
        return info_str

    @classmethod
    def validate(cls, monitor_dict):
        pass # only one CustomMetric allowed per monitor
    
    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'CustomMonitor':
        metric = CustomMetric.from_dict(value)
        description = extract_or_default(value, 'description', None)
        schedule = Schedule.from_dict(extract_or_default(value, 'schedule', {}))

        return cls(
            metrics=[metric],
            description=description,
            schedule=schedule,
        )

    def base_sql_statement(self, select_sql):
        return "WITH custom_metric AS ({select_sql}) SELECT 1 AS custom FROM custom_metric".format(select_sql=select_sql)

