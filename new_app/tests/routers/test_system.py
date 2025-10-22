from unittest.mock import patch

from config import settings


def test_get_version_unauthorized(client):
    response = client.get("/api/v1/version")
    assert response.status_code == 401


@patch("moneynote.routers.deps.get_current_active_user", return_value={"username": "testuser"})
def test_get_version_authorized(mock_get_user, client, auth_headers):
    response = client.get("/api/v1/version", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"version": settings.APP_VERSION}


def test_get_test3_unauthorized(client):
    response = client.get("/api/v1/test3")
    assert response.status_code == 401


@patch("moneynote.routers.deps.get_current_active_user", return_value={"username": "testuser"})
def test_get_test3_authorized(mock_get_user, client, auth_headers):
    response = client.get("/api/v1/test3", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"base_url": settings.BASE_URL}
