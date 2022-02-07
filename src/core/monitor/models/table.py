from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from core.common.drivers.column import Column, ColumnDataType
from core.common.drivers.base import BaseDialect

from . import MonitorDefinition, MonitorConfiguration
from .base import Monitor
from .metrics import MetricBase
from .schedule import Schedule

@dataclass
class TableMonitorConfigurationDefaults:
    where: str = ''
    days_ago: int = -100

@dataclass
class TableMonitorConfiguration:
    table: str
    timestamp_field: str

@dataclass
class TableMonitorDefinition(MonitorConfiguration, TableMonitorConfigurationDefaults, MonitorDefinition, TableMonitorConfiguration):
    def to_monitor(self, workspace):
        return TableMonitor.from_definition(self, workspace)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": "table",
            "table": self.table,
            # "schedule_minutes": self.schedule_minutes,
            # "schedule_type": self.schedule_type,
            # "schedule": Schedule(self.schedule_minutes).to_dict(),
            "timestamp_field": self.timestamp_field,
        }

def extract_or_default(obj, key, default):
    return obj[key] if key in obj else default

class ColumnMetricType(Enum):
    APPROX_DISTINCTNESS = 'approx_distinctness'
    COMPLETENESS = 'completeness'
    ZERO_RATE = 'zero_rate'
    NEGATIVE_RATE = 'negative_rate'
    NUMERIC_MEAN = 'numeric_mean'
    NUMERIC_MIN = 'numeric_min'
    NUMERIC_MAX = 'numeric_max'
    NUMERIC_STD = 'numeric_std'
    APPROX_DISTINCT_COUNT = 'approx_distinct_count'
    MEAN_LENGTH = 'mean_length'
    MAX_LENGTH = 'max_length'
    MIN_LENGTH = 'min_length'
    STD_LENGTH = 'std_length'
    TEXT_INT_RATE = 'text_int_rate'
    TEXT_NUMBER_RATE = 'text_number_rate'
    TEXT_UUID_RATE = 'text_uuid_rate'
    TEXT_ALL_SPACES_RATE = 'text_all_spaces_rate'
    TEXT_NULL_KEYWORD_RATE = 'text_null_keyword_rate'

    @classmethod
    def default(cls):
        return [cls.APPROX_DISTINCTNESS, cls.COMPLETENESS]

    @classmethod
    def all(cls):
        return [
            cls.APPROX_DISTINCTNESS, 
            cls.COMPLETENESS,
            cls.ZERO_RATE,
            cls.NEGATIVE_RATE,
            cls.NUMERIC_MEAN,
            cls.NUMERIC_MIN,
            cls.NUMERIC_MAX,
            cls.NUMERIC_STD,
            cls.APPROX_DISTINCT_COUNT,
            cls.MEAN_LENGTH,
            cls.MAX_LENGTH,
            cls.MIN_LENGTH,
            cls.STD_LENGTH,
            cls.TEXT_INT_RATE,
            cls.TEXT_NUMBER_RATE,
            cls.TEXT_UUID_RATE,
            cls.TEXT_ALL_SPACES_RATE,
            cls.TEXT_NULL_KEYWORD_RATE,
        ]

    @classmethod
    def default_for(cls, data_type: ColumnDataType): 
        if data_type == ColumnDataType.FLOAT or data_type == ColumnDataType.INTEGER:
            return [
                cls.ZERO_RATE,
                cls.NEGATIVE_RATE,
                cls.NUMERIC_MEAN,
                cls.NUMERIC_MIN,
                cls.NUMERIC_MAX,
                cls.NUMERIC_STD,
            ]
        elif data_type == ColumnDataType.STRING:
            return [
                cls.APPROX_DISTINCT_COUNT,
                cls.MEAN_LENGTH,
                cls.MAX_LENGTH,
                cls.MIN_LENGTH,
                cls.STD_LENGTH,
                cls.TEXT_INT_RATE,
                cls.TEXT_NUMBER_RATE,
                cls.TEXT_UUID_RATE,
                cls.TEXT_ALL_SPACES_RATE,
                cls.TEXT_NULL_KEYWORD_RATE,
            ]
            

        return cls.default()


@dataclass
class ColumnMetric(MetricBase):
    type: ColumnMetricType
    column: str

    def alias(self):
        return "{}__{}".format(self.column, self.type.value)

    def compile(self, dialect: BaseDialect):
        alias = self.alias()
        column = self.column

        attr = getattr(dialect, self.type._value_)
        if not attr:
            raise Exception("Unreachable: Metric type is defined that does not resolve to a definition.")
        unformatted_metric_sql = attr()
        formatted_metric_sql = unformatted_metric_sql.format(column)

        metric_sql = "{} AS {}".format(formatted_metric_sql, alias)
        return metric_sql


@dataclass
class TableMonitor(TableMonitorConfigurationDefaults, Monitor, TableMonitorConfiguration):
    metrics: List[ColumnMetricType] = field(default_factory=lambda: ColumnMetricType.all())
    columns: List[Column] = field(default_factory=list)
    minutes_ago: int = -100 * 24 * 60

    def base_sql_statement(self, select_sql, dialect):
        return dialect.table_query().format(
            select_sql=select_sql,
            table=self.table,
            timestamp_field=self.timestamp_field,
            minutes_ago=self.minutes_ago,
        )

    def info(self):
        info_str = "Table Health Monitor: {}".format(self.table)
        if self.description:
            info_str += "\n{}".format(self.description)
        return info_str

    @classmethod
    def validate(cls, monitor_dict):
        pass

    def _create_metrics(self):
        metrics = []
        for column in self.columns:
            for metric_type in ColumnMetricType.default_for(column.data_type):
                if metric_type in self.metrics:
                    metric = ColumnMetric(
                        column=column.name,
                        type=ColumnMetricType(metric_type),
                    )
                    metrics.append(metric)

        return metrics
    
    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'Monitor':
        table = value['table']
        timestamp_field = value['timestamp_field']
        description = extract_or_default(value, 'description', None)
        where = extract_or_default(value, 'where', '')
        days_ago = extract_or_default(value, 'days_ago', -100)
        
        return cls(
            table=table,
            description=description,
            timestamp_field=timestamp_field,
            where=where,
            minutes_ago=(days_ago * 60 * 24),
        )

    def to_dict(self):
        # Used for output on bootstrap right now.
        output = {
            'table': self.table,
            'timestamp_field': self.timestamp_field,
            'type': 'table',
        }
        if self.name:
            output['name'] = self.name
        if self.description:
            output['description'] = self.description

        return output

    def retrieve_metrics(self):
        return self._create_metrics()

    @classmethod
    def from_definition(cls, definition: TableMonitorDefinition, workspace):
        # monitor_base = super().from_definition(definition, workspace)
        driver_config = workspace.get_driver_config(definition.datasource)

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
            table=definition.table,
            timestamp_field=definition.timestamp_field,
            where=definition.where,
            minutes_ago=(definition.days_ago * 60 * 24),
        )

