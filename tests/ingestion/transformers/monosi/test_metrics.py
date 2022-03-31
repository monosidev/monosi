from datetime import datetime
from uuid import uuid4
import pytest

import ingestion.transformers.monosi.metrics as metrics


@pytest.fixture
def metric():
    return {
        "id": str(uuid4().hex),
        "table_name": "table",
        "schema": "schema",
        "database": "database",
        "column_name": "col_name",
        "metric": "metric-name",
        "value": "84848.9",
        "time_window_start": str(datetime.now()),
        "time_window_end": str(datetime.now()),
        "created_at": str(datetime.now())
    }

@pytest.fixture
def metric_diff_col_and_type():
    return {
        "id": str(uuid4().hex),
        "table_name": "table",
        "schema": "schema",
        "database": "database",
        "column_name": "another_col",
        "metric": "metric-name-2",
        "value": "84848.9",
        "time_window_start": str(datetime.now()),
        "time_window_end": str(datetime.now()),
        "created_at": str(datetime.now())
    }

@pytest.fixture
def metrics_input():
    return {
        'columns': ['TIME_WINDOW_START', 'TIME_WINDOW_END'],
        'rows': [
        ]
    }

@pytest.fixture
def metrics_input_one():
    return {
        'columns': ['TIME_WINDOW_START', 'TIME_WINDOW_END'],
        'rows': [
            {
                'WINDOW_START': '123',
                'WINDOW_END': '123',
                'TABLE_NAME': 'table',
                'SCHEMA_NAME': 'schema',
                'DATABASE_NAME': 'database',
                'anything___else': 'value'
            }
        ]
    }

@pytest.fixture
def metrics_input_multiple():
    return {
        'columns': ['TIME_WINDOW_START', 'TIME_WINDOW_END'],
        'rows': [
            {
                'WINDOW_START': '123',
                'WINDOW_END': '123',
                'TABLE_NAME': 'table',
                'SCHEMA_NAME': 'schema',
                'DATABASE_NAME': 'database',
                'anything___else': 'value',
                'one___more': 'value'
            }
        ]
    }

def test__transform_empty_metrics(metrics_input):
    output_arr = metrics.MetricTransformer._transform(metrics_input)

    assert len(output_arr) == 0

def test__transform_one_metric(metrics_input_one):
    output_arr = metrics.MetricTransformer._transform(metrics_input_one)

    assert len(output_arr) == 1

def test__transform_multiple_metrics(metrics_input_multiple):
    output_arr = metrics.MetricTransformer._transform(metrics_input_multiple)

    assert len(output_arr) == 2


@pytest.fixture
def normalized_schema():
    return metrics.MetricTransformer._normalized_schema()

def test__normalized_schema_correct(normalized_schema, metric):
    input_arr = [metric]
    is_correct = metrics.MetricTransformer.match(input_arr, normalized_schema)

    assert is_correct == True

def test__normalized_schema_correct_multiple(normalized_schema, metric, metric_diff_col_and_type):
    input_arr = [metric, metric_diff_col_and_type]
    is_correct = metrics.MetricTransformer.match(input_arr, normalized_schema)

    assert is_correct == True

def test__normalized_schema_incorrect_to_have_none(normalized_schema):
    input_arr = []
    is_correct = metrics.MetricTransformer.match(input_arr, normalized_schema)

    assert is_correct == False

def test__normalized_schema_incorrect(normalized_schema, metric):
    input_arr = [{'anything': 'atall'}]
    is_correct = metrics.MetricTransformer.match(input_arr, normalized_schema)

    assert is_correct == False

def test__normalized_schema_incorrect_multiple(normalized_schema, metric):
    input_arr = [metric, {'anything': 'else'}]
    is_correct = metrics.MetricTransformer.match(input_arr, normalized_schema)

    assert is_correct == False


# TODO OOOOOOOOOOOOOOOP
@pytest.fixture
def original_schema():
    return metrics.MetricTransformer._original_schema()

def test__original_schema_correct(original_schema, metrics_input_one):
    is_correct = metrics.MetricTransformer.match(metrics_input_one, original_schema)

    assert is_correct == True

def test__original_schema_correct_multiple(original_schema, metrics_input_multiple):
    is_correct = metrics.MetricTransformer.match(metrics_input_multiple, original_schema)

    assert is_correct == True

def test__original_schema_incorrect_to_have_none(original_schema, metrics_input):
    is_correct = metrics.MetricTransformer.match(metrics_input, original_schema)

    assert is_correct == False

def test__original_schema_incorrect(original_schema):
    input_arr = [{'anything': 'goeshere'}]
    is_correct = metrics.MetricTransformer.match(input_arr, original_schema)

    assert is_correct == False

