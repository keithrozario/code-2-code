from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_version_authorized(mock_auth):
    response = client.get("/api/v1/version", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    assert "version" in response.json()

def test_get_test3_authorized(mock_auth):
    response = client.get("/api/v1/test3", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    assert "base_url" in response.json()

def test_get_version_unauthorized():
    response = client.get("/api/v1/version")
    assert response.status_code == 401

def test_get_test3_unauthorized():
    response = client.get("/api/v1/test3")
    assert response.status_code == 401
