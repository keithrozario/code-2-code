from unittest.mock import patch


def test_get_book_templates_unauthorized(client):
    response = client.get("/api/v1/book-templates/all")
    assert response.status_code == 401


@patch("moneynote.routers.deps.get_current_active_user", return_value={"username": "testuser"})
def test_get_book_templates_authorized(mock_get_user, client, auth_headers):
    response = client.get("/api/v1/book-templates/all", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert "id" in response.json()[0]
    assert "name" in response.json()[0]
    assert "description" in response.json()[0]
