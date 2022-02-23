import uuid
import pytest

from server import create_app

DATASOURCES_ENDPOINT = "/v1/api/datasources"
NUM_DATASOURCES_IN_DB = 1

@pytest.fixture
def client(tmpdir):
    # temp_db_file = f"sqlite:///{tmpdir.dirpath()}/"
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_datasources_get_all(client):
    response = client.get(f"{DATASOURCES_ENDPOINT}")

    assert response.status_code == 200
    assert len(response.json) == NUM_DATASOURCES_IN_DB

def test_datasources_post(client):
    datasource_name = "datasource " + uuid.uuid4().hex
    new_datasource_json = {"name": datasource_name, "type": "snowflake", "config": {}}
    response = client.post(f"{DATASOURCES_ENDPOINT}", json=new_datasource_json)

    assert response.status_code == 200
    assert response.json["datasources"]["name"] == datasource_name

def test_datasources_post_error(client):
    missing_datasource_info_json = {"name": "D.K. Metcalf"}
    response = client.post(f"{DATASOURCES_ENDPOINT}", json=missing_datasource_info_json)

    assert response.status_code == 500

def test_datasources_single(client):
    response = client.get(f"{DATASOURCES_ENDPOINT}/1")

    assert response.status_code == 200
    assert response.json["datasource"] is not None

def test_datasource_not_found(client):
    response = client.get(f"{DATASOURCES_ENDPOINT}/7")

    assert response.status_code == 404

# def test_datasource_test_connection_success(client):
#     response = client.get(f"{DATASOURCES_ENDPOINT}/1/test")

#     assert response.json['connection'] == "true"

# def test_datasource_test_connection_failure(client):
#     response = client.get(f"{DATASOURCES_ENDPOINT}/4/test")

#     assert response.json['connection'] == "false"

