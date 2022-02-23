import pytest

import core.metadata.extractors.sourcemetrics as sourcemetrics


@pytest.fixture
def runner():
    return sourcemetrics.MetricsRunner()

def test_runner__execute(runner):
    pass

def test_runner_run(runner):
    pass


@pytest.fixture
def extractor():
    return sourcemetrics.MetricsExtractor()

def test_run(extractor):
    pass
