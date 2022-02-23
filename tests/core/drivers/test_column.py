import pytest

import core.drivers.column as column

def test_extract_or_default_exists():
    key = 'key'
    value = 'value'
    default = 'default'
    obj = {key: value}

    extracted_val = column.extract_or_default(obj, key, default)
    assert extracted_val == value

def test_extract_or_default_doesnt_exist():
    key = 'key'
    value = 'value'
    default = 'default'
    obj = {key: value}

    extracted_val = column.extract_or_default(obj, 'alt_key', default)
    assert extracted_val == default

def test_assign_if_exists_when_exists():
    pass

def test_assign_if_exists_doesnt_exist():
    pass


@pytest.fixture
def column_obj():
    return column.Column(
        name="column_name",
        data_type=column.ColumnDataType.STRING,
    )

def test_column_create(column_obj):
    assert isinstance(column_obj, column.Column)

# use multiple args here
def test_resolve_to_type_from_str_():
    pass


@pytest.fixture
def table():
    return column.Table(
        name="table_name",
        columns=[]
    )

def test_table_timestamp_cols(table):
    pass

def test_table_timestamp(table):
    pass

def test_table__insert_in_table(table):
    pass

def test_table__fqtn():
    pass

def test_table_from_metadata():
    pass

