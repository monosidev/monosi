import uuid
import pytest

from server import create_app

MONITORS_ENDPOINT = "/v1/api/monitors"
NUM_MONITORS_ENDPOINT = 1

@pytest.fixture
def client(tmpdir):
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_monitors_get_all(client):
    response = client.get(f"{MONITORS_ENDPOINT}")

    assert response.status_code == 200
    assert len(response.json) == NUM_MONITORS_ENDPOINT

def test_monitors_post(client):
    new_monitor_json = {"table_name": uuid.uuid4().hex + "table_name", "database": "database", "schema": "schema", "timestamp_field": "timestamp", "workspace": "workspace", "source": "source", "type": "table_health"}
    response = client.post(f"{MONITORS_ENDPOINT}", json=new_monitor_json)

    assert response.status_code == 200

def test_monitors_post_job(client):
    pass
    # creates job

def test_monitors_destroy_job(client):
    pass
    # deletes job

def test_monitors_destroy_associated(client):
    pass
    # deletes metrics and executions

def test_monitors_post_error(client):
    missing_monitor_information_json = {}
    response = client.post(f"{MONITORS_ENDPOINT}", json=missing_monitor_information_json)

    assert response.status_code == 500

def test_monitor_single(client):
    response = client.get(f"{MONITORS_ENDPOINT}/126")

    assert response.status_code == 200
    assert response.json["monitor"] is not None

def test_monitor_not_found(client):
    response = client.get(f"{MONITORS_ENDPOINT}/7")

    assert response.status_code == 404



