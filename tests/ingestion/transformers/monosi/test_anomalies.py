import pytest

import ingestion.transformers.monosi.anomalies as anomalies


@pytest.fixture
def zscores():
    return []

@pytest.fixture
def zscore():
    return {
        'metric_id': 1,
        'expected_range_start': 0.0,
        'expected_range_end': 1.0,
        'error': False,
        'zscore': 0.5,
    }

@pytest.fixture
def zscore_error():
    return {
        'metric_id': 3,
        'expected_range_start': 1.5,
        'expected_range_end': 9.0,
        'error': True,
        'zscore': 0.2,
    }

def test__transform_empty_zscores():
    input_arr = []
    output_arr = anomalies.AnomalyTransformer._transform(input_arr)

    assert len(output_arr) == 0

def test__transform_no_anomalous_zscores(zscore):
    input_arr = [zscore]
    output_arr = anomalies.AnomalyTransformer._transform(input_arr)

    assert len(output_arr) == 0

def test__transform_all_anomalous_zscores(zscore_error):
    input_arr = [zscore_error]
    output_arr = anomalies.AnomalyTransformer._transform(input_arr)

    assert len(output_arr) == 1

def test__transform_mixed_anomalous_zscores(zscore, zscore_error):
    input_arr = [zscore, zscore_error]
    output_arr = anomalies.AnomalyTransformer._transform(input_arr)

    assert len(output_arr) == 1



@pytest.fixture
def normalized_schema():
    return anomalies.AnomalyTransformer._normalized_schema()

def test__normalized_schema_correct(normalized_schema, zscore_error):
    input_arr = [zscore_error]
    is_correct = anomalies.AnomalyTransformer.match(input_arr, normalized_schema)

    assert is_correct == True

def test__normalized_schema_correct_multiple(normalized_schema, zscore_error):
    input_arr = [zscore_error, zscore_error]
    is_correct = anomalies.AnomalyTransformer.match(input_arr, normalized_schema)

    assert is_correct == True

def test__normalized_schema_incorrect_to_have_none(normalized_schema):
    input_arr = []
    is_correct = anomalies.AnomalyTransformer.match(input_arr, normalized_schema)

    assert is_correct == False

def test__normalized_schema_incorrect(normalized_schema, zscore):
    input_arr = [zscore]
    is_correct = anomalies.AnomalyTransformer.match(input_arr, normalized_schema)

    assert is_correct == False

def test__normalized_schema_incorrect_multiple(normalized_schema, zscore, zscore_error):
    input_arr = [zscore, zscore_error]
    is_correct = anomalies.AnomalyTransformer.match(input_arr, normalized_schema)

    assert is_correct == False


@pytest.fixture
def original_schema():
    return anomalies.AnomalyTransformer._original_schema()

def test__original_schema_correct(original_schema, zscore):
    input_arr = [zscore]
    is_correct = anomalies.AnomalyTransformer.match(input_arr, original_schema)

    assert is_correct == True

def test__original_schema_correct_multiple(original_schema, zscore, zscore_error):
    input_arr = [zscore, zscore_error]
    is_correct = anomalies.AnomalyTransformer.match(input_arr, original_schema)

    assert is_correct == True

def test__original_schema_incorrect_to_have_none(original_schema):
    input_arr = []
    is_correct = anomalies.AnomalyTransformer.match(input_arr, original_schema)

    assert is_correct == False

def test__original_schema_incorrect(original_schema):
    input_arr = [{'anything': 'goeshere'}]
    is_correct = anomalies.AnomalyTransformer.match(input_arr, original_schema)

    assert is_correct == False
