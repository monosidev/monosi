import pytest

from ingestion.sources.base import ColumnMetricType, MetricsQueryBuilder
from ingestion.sources.bigquery import BigQuerySourceDialect


@pytest.mark.parametrize('column_type', [
    'ARRAY<TIMESTAMP>',
    'ARRAY<STRUCT<start TIMESTAMP, end TIMESTAMP>>',
    'STRUCT<created_at TIMESTAMP>',
    'STRUCT<count INT64, created_at TIMESTAMP>',
    'STRUCT<label STRING, created_at TIMESTAMP>',
    'ARRAY<DATE>',
])
def test_nested_temporal_columns_do_not_generate_scalar_metrics(column_type):
    assert ColumnMetricType.default_for(column_type) == [ColumnMetricType.COMPLETENESS]
    builder = MetricsQueryBuilder(BigQuerySourceDialect, {}, {}, 0)
    result = builder._select_sql([
        {'NAME': 'events', 'COL_NAME': 'windows', 'COL_TYPE': column_type},
        {'NAME': 'events', 'COL_NAME': 'created_at', 'COL_TYPE': 'timestamp'},
    ])['events']
    assert result['timestamp_fields'] == ['created_at']
    assert 'CAST(windows AS TIMESTAMP)' not in result['sql']
    assert 'windows___freshness' not in result['sql']
    assert 'COUNT(windows)' in result['sql']
    assert 'created_at___freshness' in result['sql']


@pytest.mark.parametrize('column_type', ['date', 'timestamp', 'timestamp with time zone', 'timestamp_ntz'])
def test_scalar_temporal_columns_keep_freshness(column_type):
    assert ColumnMetricType.default_for(column_type) == [ColumnMetricType.FRESHNESS]
    builder = MetricsQueryBuilder(BigQuerySourceDialect, {}, {}, 0)
    result = builder._select_sql([
        {'NAME': 'events', 'COL_NAME': 'created_at', 'COL_TYPE': column_type},
    ])['events']
    assert result['timestamp_fields'] == ['created_at']
    assert 'created_at___freshness' in result['sql']


def test_table_with_only_nested_temporal_columns_has_no_timestamp_field():
    builder = MetricsQueryBuilder(BigQuerySourceDialect, {}, {}, 0)
    result = builder._select_sql([
        {'NAME': 'events', 'COL_NAME': 'windows', 'COL_TYPE': 'array<timestamp>'},
    ])['events']
    assert result['timestamp_fields'] == []
    assert builder._timestamp_field(result) is None
    assert 'TIMESTAMP_DIFF' not in result['sql']


def test_bigquery_nested_timestamp_does_not_generate_invalid_cast():
    builder = MetricsQueryBuilder(BigQuerySourceDialect, {}, {}, 0)
    result = builder._select_sql([
        {'NAME': 'events', 'COL_NAME': 'windows', 'COL_TYPE': 'array<struct<start timestamp, end timestamp>>'},
    ])['events']
    assert 'CAST(windows AS TIMESTAMP)' not in result['sql']
    assert result['timestamp_fields'] == []
