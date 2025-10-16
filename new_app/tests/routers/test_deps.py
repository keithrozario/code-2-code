import jwt
import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from moneynote.routers.deps import get_current_user

app = FastAPI()

@app.get("/users/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}

client = TestClient(app)

def test_get_current_user_no_token():
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_current_user_invalid_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_get_current_user_not_bearer():
    response = client.get("/users/me", headers={"Authorization": "Token invalidtoken"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_current_user_valid_token():
    token = jwt.encode({"sub": "test-user"}, "secret", algorithm="HS256")
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() == {"username": "test-user"}