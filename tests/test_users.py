from datetime import timedelta
from fastapi.testclient import TestClient

import models
import security

# Fixtures like `client` and `db_session` are now loaded from conftest.py

def test_create_user_success(client, db_session):
    response = client.post(
        "/users/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_create_user_duplicate_email(client, db_session):
    client.post(
        "/users/register",
        json={"username": "testuser1", "email": "test1@example.com", "password": "password"},
    )
    response = client.post(
        "/users/register",
        json={"username": "testuser2", "email": "test1@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_create_user_duplicate_username(client, db_session):
    client.post(
        "/users/register",
        json={"username": "testuser3", "email": "test3@example.com", "password": "password"},
    )
    response = client.post(
        "/users/register",
        json={"username": "testuser3", "email": "test4@example.com", "password": "password"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

def test_password_hashing(client, db_session):
    response = client.post(
        "/users/register",
        json={"username": "testuser5", "email": "test5@example.com", "password": "a_very_secret_password"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]
    
    user_in_db = db_session.query(models.User).filter(models.User.id == user_id).first()
    assert user_in_db
    assert user_in_db.hashed_password != "a_very_secret_password"

def test_login_success(client, db_session):
    client.post(
        "/users/register",
        json={"username": "logintest", "email": "login@test.com", "password": "password"},
    )
    response = client.post(
        "/users/login",
        data={"username": "logintest", "password": "password"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client, db_session):
    client.post(
        "/users/register",
        json={"username": "logintest2", "email": "login2@test.com", "password": "password"},
    )
    response = client.post(
        "/users/login",
        data={"username": "logintest2", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_login_invalid_username(client):
    response = client.post(
        "/users/login",
        data={"username": "nonexistentuser", "password": "password"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_get_me_success(authenticated_client):
    client = authenticated_client
    response = client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_get_me_no_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_get_me_invalid_token(client):
    response = client.get("/users/me", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

def test_get_me_expired_token(client):
    expired_token = security.create_access_token(
        data={"sub": "testuser"}, expires_delta=timedelta(minutes=-1)
    )
    response = client.get("/users/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
