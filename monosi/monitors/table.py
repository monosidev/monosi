from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List

from .base import Monitor
from .metrics import MetricBase

def extract_or_default(obj, key, default):
    return obj[key] if key in obj else default
    
class StringColumnMetricTypeDefaults:
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

class NumericColumnMetricTypeDefaults:
    ZERO_RATE = 'zero_rate'
    NEGATIVE_RATE = 'negative_rate'
    NUMERIC_MEAN = 'numeric_mean'
    NUMERIC_MIN = 'numeric_min'
    NUMERIC_MAX = 'numeric_max'
    NUMERIC_STD = 'numeric_std'

class ColumnMetricType(StringColumnMetricTypeDefaults, NumericColumnMetricTypeDefaults, Enum):
    APPROX_DISTINCTNESS = 'approx_distinctness'
    COMPLETENESS = 'completeness'

    @classmethod
    def default(cls):
        return [cls.APPROX_DISTINCTNESS, cls.COMPLETENESS]

    @classmethod
    def all(cls):
        return cls.__members__.values()

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

    metrics: List[ColumnMetric] = field(default_factory=list)

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

    @classmethod
    def validate(cls, monitor_dict):
        pass

    @classmethod
    def _create_metrics(cls, columns, allowed_metrics):
        metrics = []
        for column in columns:
            for metric_type in ColumnMetricType.default():
                if metric_type in allowed_metrics:
                    metric = ColumnMetric(
                        column=column,
                        type=metric_type,
                    )
                    metrics.append(metric)

        return metrics
    
    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> 'Monitor':
        table = value['table']
        timestamp_field = value['timestamp_field']
        where = extract_or_default(value, 'where', '')
        days_ago = extract_or_default(value, 'days_ago', -100)

        # TODO: columns
        user_columns = extract_or_default(value, 'columns', [])
        user_metrics = extract_or_default(value, 'metrics', ColumnMetricType.default())
        metrics = cls._create_metrics(user_columns, user_metrics)

        return cls(
            table=table,
            metrics=metrics,
            timestamp_field=timestamp_field,
            where=where,
            days_ago=days_ago,
        )

