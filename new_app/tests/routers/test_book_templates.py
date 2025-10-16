import jwt
from fastapi.testclient import TestClient
from main import app
from moneynote.schemas.book_template import BookTemplate

client = TestClient(app)

def test_get_all_book_templates_unauthenticated():
    response = client.get("/book-templates/all")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_all_book_templates_authenticated():
    token = jwt.encode({"sub": "test-user"}, "secret", algorithm="HS256")
    response = client.get("/book-templates/all", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0
    for item in response_data:
        BookTemplate(**item)
