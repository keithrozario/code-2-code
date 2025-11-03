import json
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_all_book_templates_unauthorized():
    response = client.get("/api/v1/book-templates/all")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_all_book_templates_success(mock_auth):
    response = client.get("/api/v1/book-templates/all", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    with open("app/moneynote/data/book_tpl.json", "r") as f:
        expected_data = json.load(f)
    assert response.json() == expected_data
