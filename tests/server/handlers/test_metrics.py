import pytest

from server import create_app


METRICS_ENDPOINT = "/v1/api/monitors/{monitor_id}/metrics?metric={metric}&column_name={column_name}"
NUM_METRICS_FOR_MONITOR = 4

@pytest.fixture
def client(tmpdir):
    temp_db_file = f"sqlite:///{tmpdir.dirpath()}"
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_metrics_get_individ(client):
    response = client.get(METRICS_ENDPOINT.format(
        monitor_id=1,
        metric="approx_distinct_count",
        column_name="user_id",
    ))

    assert response.status_code == 200
    assert len(response.json) == NUM_METRICS_FOR_MONITOR


def test_metrics_get_individ_failure(client):
    response = client.get(METRICS_ENDPOINT.format(
        monitor_id=1,
        metric="metric_doesnt_exist",
        column_name="missing_column_name",
    ))

    assert response.status_code == 500


