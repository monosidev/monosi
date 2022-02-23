import pytest
from core.drivers.base import BaseDriverConfiguration

import core.metadata.loaders.metrics as metrics


@pytest.fixture
def destinations():
    return [
        BaseDriverConfiguration(database="database", schema="schema")
    ]

@pytest.fixture
def loader(destinations):
    return metrics.Loader(destinations)

def test_loader__load():
    pass

def test_loader_run():
    pass
