from dataclasses import dataclass, field
from enum import Enum

from typing import Any, List, Dict
import json
import operator as py_operator

from core.common.drivers.base import BaseDialect

from . import MonitorConfiguration, MonitorDefinition
from .base import Monitor
from .metrics import MetricBase, MetricType
from .schedule import Schedule

# class Operator(Enum):
#     EQ = 'eq'
#     NE = 'ne'
#     GT = 'gt'
#     GE = 'ge'
#     LT = 'lt'
#     LE = 'le'
#     ABS_INC = 'abs_inc'
#     ABS_dec = 'abs_dec'
#     REL_INC = 'rel_inc'
#     REL_dec = 'rel_dec'

# class ThresholdDefinition:
# 	operator: Operator
# 	value: float

@dataclass
class CustomMonitorConfiguration:
    sql: str
    thresholds: str
# 	thresholds: List[ThresholdDefinition]

@dataclass
class CustomMonitorDefinition(MonitorConfiguration, MonitorDefinition, CustomMonitorConfiguration):
    def to_monitor(self, workspace):
        return CustomMonitor.from_definition(self, workspace)


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

    def to_dict(self):
    	return {
    		'operator': self.operator._value_,
    		'value': self.value,
    	}

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

    def to_dict(self):
    	return {
    		'sql': self.sql,
    		'thresholds': [threshold.to_dict() for threshold in self.thresholds],
    	}

    def compile(self, dialect: BaseDialect):
        return self.sql

def extract_or_default(obj, key, default):
    return obj[key] if key in obj else default

@dataclass
class CustomMonitor(Monitor):
    metric: CustomMetric

    def retrieve_metrics(self):
        return [self.metric]

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

    def to_dict(self):
        metric_dict = self.metric.to_dict()
        output = {
            'sql': metric_dict['sql'],
            'thresholds': metric_dict['thresholds'],
            'type': 'custom',
        }
        if self.name:
            output['name'] = self.name
        if self.description:
            output['description'] = self.description

        return output

    def base_sql_statement(self, select_sql, dialect):
        return "WITH t1 (c1) AS ({select_sql}) SELECT c1 AS custom FROM t1".format(select_sql=select_sql)

    @classmethod
    def from_definition(cls, definition: CustomMonitorDefinition, workspace):
        # monitor_base = super().from_definition(definition, workspace)
        driver_config = workspace.get_driver_config(definition.datasource)
        metric = CustomMetric.from_dict({'sql': definition.sql, 'thresholds': definition.thresholds})

        return cls(
            # name=monitor_base.name,
            # description=monitor_base.description,
            # enabled=monitor_base.enabled,
            # driver_config=monitor_base.driver_config,
            name=definition.name,
            description=definition.description,
            schedule=Schedule(definition.schedule_minutes),
            enabled=definition.enabled or True,
            driver_config=driver_config,
            metric=metric,
        )
