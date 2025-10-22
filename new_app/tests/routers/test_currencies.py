from unittest.mock import patch


def test_get_currencies_unauthorized(client):
    response = client.get("/api/v1/currencies/all")
    assert response.status_code == 401


@patch("moneynote.routers.deps.get_current_active_user", return_value={"username": "testuser"})
def test_get_currencies_authorized(mock_get_user, client, auth_headers):
    response = client.get("/api/v1/currencies/all", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "code" in response.json()[0]
    assert "name" in response.json()[0]
    assert "symbol" in response.json()[0]
