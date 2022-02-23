import pytest

from cli.parsers import definitions
from core.drivers.base import BaseDriver, BaseDriverConfiguration
from core.drivers.postgres import DriverConfiguration

from core.models import datasource, integration, monitor, project, workspace, zscore

## DataSource Model ##

@pytest.fixture
def model_db_config():
    return DriverConfiguration(
        user="test_user",
        password="test_password",
        host="test_host",
        database="test_database",
        schema="test_schema",
        port=5432,
    )

@pytest.fixture
def model_datasource(model_db_config):
    return datasource.DataSource(
        name="Example Datasource",
        type="postgres",
        config=model_db_config.to_dict(),
    )

def test_datasource_create(model_datasource):
    assert isinstance(model_datasource, datasource.DataSource)

def test_datasource_db_config(model_datasource):
    db_config = model_datasource.db_config()
    assert isinstance(db_config, BaseDriverConfiguration)

def test_datasource_db_driver(model_datasource):
    db_driver = model_datasource.db_driver()
    assert isinstance(db_driver, BaseDriver)


## Integration Model ##

@pytest.fixture
def model_integration():
    return integration.Integration(
        name="Test Integration",
        type="slack",
        config="{}", # NO URL to send to 
    )

def test_integration_create(model_integration):
    assert isinstance(model_integration, integration.Integration)

# def test_integration_send_success(model_integration):
#     message = "The message to send."
#     try:
#         model_integration.send(message)
#     except Exception as e:
#         pass

def test_integration_send_failure(model_integration):
    message = "The message to send."
    with pytest.raises(Exception):
        model_integration.send(message)

## Monitor Model ##

@pytest.fixture
def model_monitor():
    return monitor.MsiMonitor(
        table_name="test_table",
        schema="test_schema",
        database="test_database",
        timestamp_field="Test Timestamp Field",
        workspace="Test Workspace",
        source="Test Source",
        type="table_health",
    )

def test_monitor_create(model_monitor):
    assert model_monitor

def test_monitor_fqtn(model_monitor):
    fqtn = model_monitor.fqtn()
    assert fqtn == "test_database.test_schema.test_table"


##  Project Model ##
@pytest.fixture
def source_name():
    return "test_source"

@pytest.fixture
def model_workspace(source_name, model_db_config):
    return workspace.Workspace(
       name="Test Workspace",
       integrations={
         source_name: model_db_config
       },
    )

@pytest.fixture
def model_project(model_workspace, source_name):
    return project.Project(
        name="Example Project",
        workspace=model_workspace,
        source_name=source_name,
    )

@pytest.fixture
def model_monitor_definition():
    return definitions.MonitorDefinition(
        type=definitions.MonitorDefinitionType.TABLE_HEALTH,
        table="test_table",
        timestamp_field="timestamp_field",
    )

def test_project_create(model_project):
    assert model_project

def test_project_add_monitor(model_project, model_monitor_definition):
    monitor_count_original = len(model_project.monitors)
    
    model_project.add_monitor(model_monitor_definition)
    monitor_count_plus_one = len(model_project.monitors)

    assert monitor_count_original + 1 == monitor_count_plus_one

    def source(self):
        return self.workspace.integrations[self.source_name]

def test_project_source(model_project):
    source = model_project.source()
    assert isinstance(source, BaseDriverConfiguration)

def test_project_destinations(model_project):
    destinations = model_project.destinations()

    assert len(destinations) > 0
    for destination in destinations:
        assert isinstance(destination, BaseDriverConfiguration)




# class ModelDatasourceTestSuite(unittest.TestCase):
#     """ Datasource test cases."""

#     def test_create(self):
#         self.assertEqual(op.fn(), py_operator.eq)

