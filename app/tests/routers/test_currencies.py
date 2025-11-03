import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import base64

from app.main import app
from app.moneynote.security import oauth2_scheme

client = TestClient(app)

def test_get_all_currencies_unauthorized():
    response = client.get("/api/v1/currencies/all")
    assert response.status_code == 401

def test_get_all_currencies_success(mock_auth):
    response = client.get("/api/v1/currencies/all", headers={"Authorization": "Bearer test"})
    assert response.status_code == 200
    with open("app/moneynote/data/currency.json", "r") as f:
        expected_data = json.load(f)
    assert response.json() == expected_data

@patch('app.moneynote.security.oauth2_scheme')
def test_get_all_currencies_missing_sub(mock_oauth2_scheme):
    # Create a mock token that, when decoded, has no 'sub' field
    # Header: {"alg": "HS256", "typ": "JWT"}
    # Payload: {"user_id": 123}
    header = base64.urlsafe_b64encode(b'{"alg": "HS256", "typ": "JWT"}').decode().rstrip('=')
    payload = base64.urlsafe_b64encode(b'{"user_id": 123}').decode().rstrip('=')
    mock_token = f"{header}.{payload}.signature"

    mock_oauth2_scheme.return_value = mock_token

    response = client.get("/api/v1/currencies/all", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
