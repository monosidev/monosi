from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List
from monosi.drivers.column import ColumnDataType

from monosi.drivers.column import Column

from .base import Monitor
from .metrics import MetricBase

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

@dataclass 
class TableMonitor(Monitor):
    table: str = field(default_factory=str)
    timestamp_field: str = field(default_factory=str)
    where: str = field(default_factory=str)
    days_ago: int = -100
    metrics: List[ColumnMetricType] = field(default_factory=lambda: ColumnMetricType.all())
    columns: List[Column] = field(default_factory=list)

    # TODO: BASE_SQL should be delegated to Dialect
    BASE_SQL = """
    SELECT 
        DATE_TRUNC('HOUR', {timestamp_field}) as window_start, 
        DATEADD(hr, 1, DATE_TRUNC('HOUR', {timestamp_field})) as window_end, 

        COUNT(*) as row_count, 

        {select_sql}

    FROM {table}
    WHERE 
        DATE_TRUNC('HOUR', {timestamp_field}) >= DATEADD(day, {days_ago}, CURRENT_TIMESTAMP()) 
    GROUP BY window_start, window_end 
    ORDER BY window_start ASC;
    """

    def base_sql_statement(self, select_sql):
        return TableMonitor.BASE_SQL.format(
            select_sql=select_sql,
            table=self.table,
            timestamp_field=self.timestamp_field,
            days_ago=self.days_ago,
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
            days_ago=days_ago,
        )

    def to_dict(self):
        # Used for output on bootstrap right now.
        return {
            'table': self.table,
            'timestamp_field': self.timestamp_field,
        }

    def retrieve_metrics(self):
        return self._create_metrics()


