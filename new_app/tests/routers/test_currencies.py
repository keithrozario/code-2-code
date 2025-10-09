from fastapi.testclient import TestClient
import jwt

from main import app
from moneynote.schemas.currency import Currency

client = TestClient(app)

def test_get_all_currencies_unauthenticated():
    response = client.get("/currencies/all")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_all_currencies_authenticated():
    token = jwt.encode({"sub": "test-user"}, "secret", algorithm="HS256")
    response = client.get("/currencies/all", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0
    for item in response_data:
        Currency(**item)
