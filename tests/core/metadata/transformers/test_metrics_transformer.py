import pytest

import core.metadata.transformers.metrics as metrics


@pytest.fixture
def transformer():
    return metrics.Transformer()

def test_transformer__extract_window_from_row():
    pass

def test_transformer__extract_metric_and_col_from_alias():
    pass

def test_transformer__filter_columns():
    pass

def test_transformer_run():
    pass

