import pytest

import core.drivers.factory as factory


@pytest.fixture
def fixture_factory():
    return factory.DriverFactory()

def test_factory_load_config_class_exists():
    pass

def test_factory_load_config_class_doesnt_exist():
    pass

def test_factory_load_driver_class_exists():
    pass

def test_factory_load_driver_class_doesnt_exist():
    pass

def test_factory__configuration():
    pass

def test_factory__retrieve_driver_class():
    pass

def test_factory__retrieve_driver_module():
    pass


def test_load_config():
    pass

def test_load_driver():
    pass
