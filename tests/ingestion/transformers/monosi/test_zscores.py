import pytest

import ingestion.transformers.monosi.zscores as zscores


@pytest.fixture
def zscore():
    return {
        'metric_id': "1",
        'expected_range_start': 0.0,
        'expected_range_end': 1.0,
        'error': False,
        'zscore': 0.5,
    }

@pytest.fixture
def zscore_error():
    return {
        'metric_id': "3",
        'expected_range_start': 1.5,
        'expected_range_end': 9.0,
        'error': True,
        'zscore': 0.2,
    }

@pytest.fixture
def metric():
    return {
        'table_name': 'msi_monitors', 
        'schema': 'public',
        'database': 'postgres',
        'column_name': 'id', 
        'metric': 'completeness',
        'value': '1.00000000000000000000',
        'time_window_start': '2022-03-31T12:00:00-07:00',
        'time_window_end': '2022-03-31T13:00:00-07:00',
        'interval_length_sec': None,
        'id': '9e8c2f029fbd4db8a52fe72c62fe8a8c',
        'created_at': '2022-03-31T12:07:37.686462-07:00'
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


def test__transform_empty_metrics():
    input_arr = []
    output_arr = zscores.ZScoreTransformer._transform(input_arr)

    assert len(output_arr) == 0

def test__transform_one_metric(metric):
    input_arr = [metric]
    output_arr = zscores.ZScoreTransformer._transform(input_arr)

    assert len(output_arr) == 1

def test__transform_multiple_metrics(metric, metric_diff_col_and_type):
    input_arr = [metric, metric_diff_col_and_type]
    output_arr = zscores.ZScoreTransformer._transform(input_arr)

    assert len(output_arr) == 2

def test__transform_multiple_metrics_same(metric):
    input_arr = [metric, metric]
    output_arr = zscores.ZScoreTransformer._transform(input_arr)

    assert len(output_arr) == 2



@pytest.fixture
def normalized_schema():
    return zscores.ZScoreTransformer._normalized_schema()

def test__normalized_schema_correct(normalized_schema, zscore):
    input_arr = [zscore]
    is_correct = zscores.ZScoreTransformer.match(input_arr, normalized_schema)

    assert is_correct == True

def test__normalized_schema_correct_multiple(zscore, zscore_error):
    input_arr = [zscore, zscore_error]
    is_correct = zscores.ZScoreTransformer.match(input_arr, normalized_schema)

    assert is_correct == True

def test__normalized_schema_incorrect_to_have_none(normalized_schema):
    input_arr = []
    is_correct = zscores.ZScoreTransformer.match(input_arr, normalized_schema)

    assert is_correct == False

def test__normalized_schema_incorrect(normalized_schema, zscore):
    input_arr = [{'anything': 'else'}]
    is_correct = zscores.ZScoreTransformer.match(input_arr, normalized_schema)

    assert is_correct == False

def test__normalized_schema_incorrect_multiple(normalized_schema, metric, zscore):
    input_arr = [metric, {'anything': 'else'}, zscore]
    is_correct = zscores.ZScoreTransformer.match(input_arr, normalized_schema)

    assert is_correct == False


@pytest.fixture
def original_schema():
    return zscores.ZScoreTransformer._original_schema()

def test__original_schema_correct(original_schema, metric):
    input_arr = [metric]
    is_correct = zscores.ZScoreTransformer.match(input_arr, original_schema)

    assert is_correct == True

def test__original_schema_correct_multiple(original_schema, metric, metric_diff_col_and_type):
    input_arr = [metric, metric_diff_col_and_type]
    is_correct = zscores.ZScoreTransformer.match(input_arr, original_schema)

    assert is_correct == True

def test__original_schema_incorrect_to_have_none(original_schema):
    input_arr = []
    is_correct = zscores.ZScoreTransformer.match(input_arr, original_schema)

    assert is_correct == False

def test__original_schema_incorrect(original_schema):
    input_arr = [{'anything': 'goeshere'}]
    is_correct = zscores.ZScoreTransformer.match(input_arr, original_schema)

    assert is_correct == False

