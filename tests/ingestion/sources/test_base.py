import datetime
import json
import pytest

import ingestion.sources.base as base


@pytest.fixture
def configuration_dict():
    return {
        'type': 'test_type',
        'database': 'test_db_key',
        'schema': 'test_schema_key',
        'start_date': None,
    }

@pytest.fixture
def source_configuration(configuration_dict):
    return base.SourceConfiguration(
        configuration=json.dumps(configuration_dict)
    )


def test_minutes_ago_no_start_date(source_configuration):
    minutes_ago = source_configuration.minutes_ago()
    assert minutes_ago == -int(1*24*60)

def test_minutes_ago_with_start_date_as_datetime(configuration_dict):
    fifteen_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=15)
    configuration_dict['start_date'] = fifteen_minutes_ago

    source_configuration = base.SourceConfiguration(
        configuration=json.dumps(configuration_dict)
    )
    minutes_ago = source_configuration.minutes_ago()
    assert minutes_ago == -15

def test_minutes_ago_with_start_date_as_string(configuration_dict):
    fifteen_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=15)
    configuration_dict['start_date'] = str(fifteen_minutes_ago)

    source_configuration = base.SourceConfiguration(
        configuration=json.dumps(configuration_dict)
    )
    minutes_ago = source_configuration.minutes_ago()
    assert minutes_ago == -15


## METRIC QUERY BUILDER

@pytest.fixture
def dialect():
    from ingestion.sources.postgresql import PostgreSQLSourceDialect
    return PostgreSQLSourceDialect

@pytest.fixture
def configuration():
    base.SourceConfiguration(configuration=json.dumps({'database': 'postgres', 'schema': 'public', 'start_date': None}))

@pytest.fixture
def ddata():
    return {'columns': ['NAME', 'COL_NAME', 'COL_TYPE', 'COL_SORT_ORDER', 'DATABASE', 'SCHEMA', 'IS_VIEW'], 'rows': [{'NAME': 'msi_executions', 'COL_NAME': 'job_id', 'COL_TYPE': 'text', 'COL_SORT_ORDER': 1, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_executions', 'COL_NAME': 'result', 'COL_TYPE': 'text', 'COL_SORT_ORDER': 3, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_executions', 'COL_NAME': 'id', 'COL_TYPE': 'integer', 'COL_SORT_ORDER': 4, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_executions', 'COL_NAME': 'state', 'COL_TYPE': 'integer', 'COL_SORT_ORDER': 2, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_executions', 'COL_NAME': 'updated_at', 'COL_TYPE': 'timestamp with time zone', 'COL_SORT_ORDER': 7, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_executions', 'COL_NAME': 'created_at', 'COL_TYPE': 'timestamp with time zone', 'COL_SORT_ORDER': 6, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_executions', 'COL_NAME': 'datasource_id', 'COL_TYPE': 'integer', 'COL_SORT_ORDER': 5, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_sources', 'COL_NAME': 'type', 'COL_TYPE': 'character varying', 'COL_SORT_ORDER': 2, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_sources', 'COL_NAME': 'name', 'COL_TYPE': 'character varying', 'COL_SORT_ ORDER': 1, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}, {'NAME': 'msi_sources', 'COL_NAME': 'created_at', 'COL_TYPE': 'timestamp with time zone', 'COL_SORT_ORDER': 5, 'DATABASE': 'postgres', 'SCHEMA': 'public', 'IS_VIEW': 'false'}]}

@pytest.fixture
def query_builder(dialect, configuration, ddata):
    return base.MetricsQueryBuilder(dialect, configuration, ddata)


def test_select_sql(query_builder):
    ddata = query_builder.ddata
    select_sql = query_builder._select_sql(ddata['rows'])

    assert len(select_sql) > 0








