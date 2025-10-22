from typing import Generator

from config import Settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_settings() -> Generator:
    yield Settings()


def get_current_active_user(token: str = Depends(oauth2_scheme)):
    # This is a placeholder for the actual authentication logic.
    # For now, we'll just check if a token is present and not "fake-token".
    if not token or token == "fake-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # In a real app, you'd decode the token and get the user.
    return {"username": "testuser"}
