import pytest

import ingestion.transformers.monosi.monitors as monitors


@pytest.fixture
def schema():
    return {
        'columns': ['NAME', 'COL_NAME', 'COL_TYPE', 'COL_DESCRIPTION', 'COL_SORT_ORDER', 'DATABASE', 'SCHEMA', 'DESCRIPTION', 'IS_VIEW'],
        'rows': [
            {
                'NAME': 'name_of_table',
                'COL_NAME': 'name_of_col',
                'COL_TYPE': 'timestamp_tz',
                'COL_DESCRIPTION': None,
                'COL_SORT_ORDER': '3',
                'DATABASE': 'database',
                'SCHEMA': 'schema',
                'DESCRIPTION': None,
                'IS_VIEW': 'false'
            },
            {
                'NAME': 'name_of_table',
                'COL_NAME': 'name_of_col_2',
                'COL_TYPE': 'text',
                'COL_DESCRIPTION': None,
                'COL_SORT_ORDER': '3',
                'DATABASE': 'database',
                'SCHEMA': 'schema',
                'DESCRIPTION': None,
                'IS_VIEW': 'false'
            },
            {
                'NAME': 'name_of_table_2',
                'COL_NAME': 'name_of_col_3',
                'COL_TYPE': 'int',
                'COL_DESCRIPTION': None,
                'COL_SORT_ORDER': '3',
                'DATABASE': 'database',
                'SCHEMA': 'schema',
                'DESCRIPTION': None,
                'IS_VIEW': 'false'
            },
        ]
    }

def test__transform_empty():
    input_arr = {'rows': []}
    output_arr = monitors.MonitorTransformer._transform(input_arr)

    assert len(output_arr) == 0

def test__transform(schema):
    output_arr = monitors.MonitorTransformer._transform(schema)
    expected_num_monitors = 2

    assert len(output_arr) == expected_num_monitors


@pytest.fixture
def monitor():
    return {}

@pytest.fixture
def normalized_schema():
    return monitors.MonitorTransformer._normalized_schema()

def test__normalized_schema_correct(normalized_schema, monitor):
    input_arr = [monitor]
    is_correct = monitors.MonitorTransformer.match(input_arr, normalized_schema)

    assert is_correct == True

def test__normalized_schema_correct_multiple(normalized_schema, monitor):
    input_arr = [monitor, monitor]
    is_correct = monitors.MonitorTransformer.match(input_arr, normalized_schema)

    assert is_correct == True

def test__normalized_schema_incorrect_to_have_none(normalized_schema):
    input_arr = []
    is_correct = monitors.MonitorTransformer.match(input_arr, normalized_schema)

    assert is_correct == False

def test__normalized_schema_incorrect(normalized_schema):
    input_arr = [{"anything": "goeshere"}]
    is_correct = monitors.MonitorTransformer.match(input_arr, normalized_schema)

    assert is_correct == False

def test__normalized_schema_incorrect_multiple(normalized_schema):
    input_arr = [{}, {"anything": "goeshere"}]
    is_correct = monitors.MonitorTransformer.match(input_arr, normalized_schema)

    assert is_correct == False


@pytest.fixture
def original_schema():
    return monitors.MonitorTransformer._original_schema()

def test__original_schema_correct(original_schema, schema):
    is_correct = monitors.MonitorTransformer.match(schema, original_schema)

    assert is_correct == True

def test__original_schema_incorrect_to_have_none(original_schema):
    is_correct = monitors.MonitorTransformer.match({}, original_schema)

    assert is_correct == False

def test__original_schema_incorrect(original_schema):
    input_arr = {'anything': 'goeshere'}
    is_correct = monitors.MonitorTransformer.match(input_arr, original_schema)

    assert is_correct == False

