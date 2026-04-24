from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200


@patch("api.main.redis.Redis")
def test_redis_mock(mock_redis):
    mock_instance = mock_redis.return_value
    mock_instance.ping.return_value = True

    response = client.get("/health")
    assert response.status_code == 200
