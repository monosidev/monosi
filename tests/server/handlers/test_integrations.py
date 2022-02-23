import uuid
import pytest

from server import create_app

INTEGRATIONS_ENDPOINT = "/v1/api/integrations"
NUM_INTEGRATIONS_IN_DB = 1

@pytest.fixture
def client(tmpdir):
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_integrations_get_all(client):
    response = client.get(f"{INTEGRATIONS_ENDPOINT}")

    assert response.status_code == 200
    assert len(response.json) == NUM_INTEGRATIONS_IN_DB

def test_integrations_post(client):
    integration_name = "integration " + uuid.uuid4().hex
    new_integration_json = {"name": integration_name, "type": "slack",  "config": {}}
    response = client.post(f"{INTEGRATIONS_ENDPOINT}", json=new_integration_json)

    assert response.status_code == 200
    assert response.json["integrations"]["name"] == integration_name

def test_integrations_post_error(client):
    missing_integration_info_json = {}
    response = client.post(f"{INTEGRATIONS_ENDPOINT}", json=missing_integration_info_json)

    assert response.status_code == 500

def test_integrations_single(client):
    response = client.get(f"{INTEGRATIONS_ENDPOINT}/99")

    assert response.status_code == 200
    assert response.json["integration"] is not None
    # assert response.json["name"] == "Example Integration"

def test_integration_not_found(client):
    response = client.get(f"{INTEGRATIONS_ENDPOINT}/7")

    assert response.status_code == 404

