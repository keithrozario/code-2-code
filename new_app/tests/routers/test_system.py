import jwt
from fastapi.testclient import TestClient
from main import app

from config import settings

client = TestClient(app)

def test_get_version_unauthenticated():
    response = client.get("/version")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_version_authenticated():
    token = jwt.encode({"sub": "test-user"}, "secret", algorithm="HS256")
    response = client.get("/version", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"version": settings.APP_VERSION}

def test_get_test3_unauthenticated():
    response = client.get("/test3")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_test3_authenticated():
    token = jwt.encode({"sub": "test-user"}, "secret", algorithm="HS256")
    response = client.get("/test3", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"base_url": settings.BASE_URL}