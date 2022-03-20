import os
import pytest
from sqlalchemy.engine.mock import create_mock_engine

import scheduler.base as base

## JobStore Tests
@pytest.fixture
def connection_string():
    db_config = {
        "type": "postgresql",
        "user": os.getenv('DB_USER'),
        "password": os.getenv('DB_PASSWORD'),
        "host": os.getenv('DB_HOST'),
        "port": os.getenv('DB_PORT'),
        "database": os.getenv('DB_DATABASE'),
        "schema": os.getenv('DB_SCHEMA'),
    }
    from ingestion.sources import SourceFactory
    source = SourceFactory.create(db_config)
    return source.configuration.connection_string()

@pytest.fixture
def datasource_id():
    return 130

@pytest.fixture
def datasource_id_not_executed():
    return 131

@pytest.fixture
def jobstore(connection_string, datasource_id):
    return base.MsiJobStore(url=connection_string)

def test_jobstore_get_no_execution(jobstore, datasource_id_not_executed):
    execution = jobstore.get(datasource_id_not_executed)
    assert execution == {}

def test_jobstore_get_execution_exists(jobstore, datasource_id):
    execution = jobstore.get(datasource_id)
    assert execution != {}

def test_jobstore_get_execution_exists_created_at(jobstore, datasource_id):
    execution = jobstore.get(datasource_id)
    created_at = execution.get('created_at')
    assert created_at is not None
    # assert parse is date

