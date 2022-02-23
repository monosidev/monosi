import pytest

from core.drivers.base import BaseDialect, BaseDriver, BaseDriverConfiguration, BaseSqlAlchemyDriver


@pytest.fixture
def table_name():
    return "test_table"

@pytest.fixture
def driver_configuration():
    return BaseDriverConfiguration(
        database="test_database",
        schema="test_schema",
    )

def test_driver_configuration_fqtn_just_table(driver_configuration, table_name):
    database_name = driver_configuration.database
    schema_name = driver_configuration.schema

    fully_qualified_table_name = driver_configuration.fqtn(table_name)

    assert len(fully_qualified_table_name) == 3
    assert fully_qualified_table_name[0] == database_name
    assert fully_qualified_table_name[1] == schema_name
    assert fully_qualified_table_name[2] == table_name

def test_driver_configuration_fqtn_with_schema(driver_configuration):
    database_name = driver_configuration.database
    schema_name = "schema_name"
    table_name = "table_name"

    fully_qualified_table_name = driver_configuration.fqtn("{}.{}".format(schema_name, table_name))

    assert len(fully_qualified_table_name) == 3
    assert fully_qualified_table_name[0] == database_name
    assert fully_qualified_table_name[1] == schema_name
    assert fully_qualified_table_name[2] == table_name

def test_driver_configuration_fqtn_with_database(driver_configuration):
    database_name = "database_name"
    schema_name = "schema_name"
    table_name = "table_name"

    fully_qualified_table_name = driver_configuration.fqtn("{}.{}.{}".format(database_name, schema_name, table_name))

    assert len(fully_qualified_table_name) == 3
    assert fully_qualified_table_name[0] == database_name
    assert fully_qualified_table_name[1] == schema_name
    assert fully_qualified_table_name[2] == table_name


@pytest.fixture
def dialect():
    return BaseDialect

@pytest.fixture
def driver(driver_configuration, dialect):
    return BaseDriver(
        configuration=driver_configuration,
        dialect=dialect
    )

def test_driver__create_columns():
    pass

def test_driver__retrieve_results():
    pass

def test_driver__execute():
    pass



@pytest.fixture
def sqlalchemy_driver(driver_configuration):
    return BaseSqlAlchemyDriver(
        configuration=driver_configuration
    )

def test_sqlalchemy_driver__create_engine(sqlalchemy_driver):
    pass

def test_sqlalchemy_driver__before_execute(sqlalchemy_driver):
    pass

def test_sqlalchemy_driver__execute(sqlalchemy_driver):
    pass

def test_sqlalchemy_driver_close(sqlalchemy_driver):
    pass

def test_sqlalchemy_driver_test_succeed(sqlalchemy_driver):
    pass

def test_sqlalchemy_driver_test_fail(sqlalchemy_driver):
    pass

def test_sqlalchemy_driver_validate_success(sqlalchemy_driver):
    pass

def test_sqlalchemy_driver_validate_fails(sqlalchemy_driver):
    pass


