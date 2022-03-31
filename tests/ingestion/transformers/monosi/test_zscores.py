import pytest

import ingestion.transformers.monosi.zscores as zscores


@pytest.fixture
def metrics():
    return [
        {
            'metric': 'std_dev' 
        }
    ]

@pytest.fixture
def original_schema():
    return zscores.ZScoreTransformer._original_schema()

def test__original_schema_correct(original_schema, metrics):
    is_correct = zscores.ZScoreTransformer.match(metrics, original_schema)

    assert is_correct == True

