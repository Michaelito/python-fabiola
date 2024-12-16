from fastapi.testclient import TestClient
from httpx import Response
from pytest import fixture

from main import app


@fixture
def client():
    return TestClient(app)


def test_health(client):
    response: Response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "OK"


def test_version(client):
    response: Response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {'version': {'major': 1, 'minor': 0, 'build': 0}}
