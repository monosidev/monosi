import pytest
from core.drivers.base import BaseDriver, BaseDriverConfiguration

import core.drivers.column as column

import core.metadata.extractors.metrics as metrics



# Use parameters for the following two tests
def test_column_metric_type_default_for_float():
    float_defaults = metrics.ColumnMetricType.default_for(column.ColumnDataType.FLOAT)
    pass

def test_column_metric_type_default_for_integer():
    pass

def test_column_metric_type_defaults_are_included():
    pass


@pytest.fixture
def runner_config():
    return BaseDriverConfiguration(database="database", schema="schema")

@pytest.fixture
def runner(runner_config):
    return metrics.Runner(
        config=runner_config,
    )

def test_runner__execute_before_initialize(runner):
    # expect exception
    pass

def test_runner__execute_after_initialize(runner):
    pass

def test_runner__initialize(runner):
    assert runner.driver == None
    runner._initialize()
    assert isinstance(runner.driver, BaseDriver)

def test_runner_run(runner):
    pass


@pytest.fixture
def compiler(runner_config):
    return metrics.MetricsCompiler(
        driver_config=runner_config,
        destination=runner_config,
    )

def test_compiler__minutes_ago_no_executions():
    pass

def test_compiler__minutes_ago_executions_exist():
    pass

def test_compiler_init(compiler):
    assert isinstance(compiler, metrics.MetricsCompiler)

def test_compiler__driver(compiler):
    driver = compiler._driver(compiler.destination_config)
    pass
    
def test_compiler__retrieve_columns():
    pass

def test_compiler_compile_select():
    pass

def test_compiler_select_body():
    pass

def test_compiler_compile_from():
    pass

def test_compiler_compile():
    pass


@pytest.fixture
def extractor():
    return metrics.Extractor(source=None, destinations=[])

def test_extractor_run(extractor):
    pass


