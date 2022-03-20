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
    assert minutes_ago == -int(.25*24*60)

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

