from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from core.common.drivers.base import BaseDialect
from core.common.drivers.column import Column

from . import MonitorConfiguration, MonitorDefinition
from .base import Monitor
from .metrics import MetricBase
from .schedule import Schedule


@dataclass
class SchemaMonitorConfigurationDefaults:
	columns: List[Dict[str, str]] = field(default_factory=list)

@dataclass
class SchemaMonitorConfiguration:
    table: str

@dataclass
class SchemaMonitorDefinition(MonitorConfiguration, SchemaMonitorConfigurationDefaults, MonitorDefinition, SchemaMonitorConfiguration):
    def to_monitor(self, workspace):
        return SchemaMonitor.from_definition(self, workspace)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": "schema",
            "table": self.table,
            "columns": self.columns,
            # "schedule_minutes": self.schedule_minutes,
            # "schedule_type": self.schedule_type,
            # "schedule": Schedule(self.schedule_minutes).to_dict(),
        }

def extract_or_default(obj, key, default):
    return obj[key] if key in obj else default

class SchemaMetricType(Enum):
    COLUMN_NAMES = 'name'
    COLUMN_TYPES = 'data_type'
    COLUMN_ORDERS = 'order'

    @classmethod
    def all(cls):
        return [
            cls.COLUMN_NAMES,
            cls.COLUMN_TYPES,
            cls.COLUMN_ORDERS,
        ]

@dataclass
class SchemaMetric(MetricBase):
    type: SchemaMetricType
    col_to_metric: Dict[str, Any]

    @classmethod
    def from_columns(cls, metric_type: SchemaMetricType, columns: List[Column]):
        col_to_metric_map = {}
        for col in columns:
            col_to_metric_map[col.name] = getattr(col, metric_type._value_)

        return cls(
            type=metric_type,
            col_to_metric=col_to_metric_map,
        )

    def compile(self, dialect: BaseDialect):
        return ""

@dataclass
class SchemaMonitor(SchemaMonitorConfigurationDefaults, Monitor, SchemaMonitorConfiguration):
    columns: List[Column] = field(default_factory=list)
    metrics: List[SchemaMetric] = field(default_factory=list)

    def retrieve_metrics(self):
        return self.metrics

    def info(self):
        info_str = "Schema Monitor: {}".format(self.table)
        if self.description:
            info_str += ": {}".format(self.description)
        return info_str

    @classmethod
    def validate(cls, monitor_dict):
        if 'table' not in monitor_dict:
            raise Exception("Table key was missing in the schema monitor definition.")
        if 'columns' not in monitor_dict:
            raise Exception("Columns key was missing in the schema monitor definition.")

        if len(monitor_dict['table'].split('.')) < 3:
            raise Exception("Database and schema not found.")

    @classmethod
    def _create_metrics(cls, columns: List[Column]):
        metrics = []
        for metric_type in SchemaMetricType.all():
            metric = SchemaMetric.from_columns(metric_type, columns)
            metrics.append(metric)

        return metrics

    
    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'SchemaMonitor':
        table = value['table'] # Required
        columns = [Column.from_dict(col) for col in value['columns']]
        metrics = cls._create_metrics(columns)

        description = extract_or_default(value, 'description', None)
        schedule = Schedule.from_dict(extract_or_default(value, 'schedule', {}))

        return cls(
            table=table,
            columns=columns,
            metrics=metrics,
            description=description,
            schedule=schedule,
        )

    def to_dict(self):
        return {
            'type': 'schema',
            'table': self.table,
            'columns': [col.to_dict() for col in self.columns],
        }

    def database_name(self):
        table_parts = self.table.split('.')
        if len(table_parts) < 3:
            raise Exception("Table name not fully qualified with database")

        return table_parts[0].lower()

    def schema_name(self):
        table_parts = self.table.split('.')
        if len(table_parts) < 3:
            raise Exception("Schema name not fully qualified with database")

        return table_parts[1].lower()

    def table_name(self):
        table_parts = self.table.split('.')
        if len(table_parts) < 3:
            raise Exception("Table name not fully qualified with database")

        return table_parts[2].lower()

    def base_sql_statement(self, select_sql, dialect):
        return dialect.metadata_query().format(
                database_name=self.database_name(),
                schema_name = self.schema_name(),
                table_name=self.table_name())


    @classmethod
    def from_definition(cls, definition: SchemaMonitorDefinition, workspace):
        # monitor_base = super().from_definition(definition, workspace)
        driver_config = workspace.get_driver_config(definition.datasource)

        columns = [Column.from_dict(col) for col in definition.columns]
        metrics = cls._create_metrics(columns)
        enabled = definition.enabled or True
        
        return cls(
            # name=monitor_base.name,
            # description=monitor_base.description,
            # enabled=monitor_base.enabled,
            # driver_config=monitor_base.driver_config,
            name=definition.name,
            description=definition.description,
            schedule=Schedule(definition.schedule_minutes),
            enabled=enabled,
            driver_config=driver_config,
            table=definition.table,
            columns=columns,
            metrics=metrics,
        )
