import base64
import json
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from app.moneynote.security import oauth2_scheme
from app.moneynote.schemas.token import TokenData
from app.database import get_db
from sqlalchemy.orm import Session
from app.moneynote.crud import crud_user

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # JWT is header.payload.signature
        # We only need the payload part (second part)
        payload_base64 = token.split('.')[1]
        # JWT uses URL-safe Base64 without padding
        # Add padding if necessary
        padding_needed = len(payload_base64) % 4
        if padding_needed:
            payload_base64 += '=' * (4 - padding_needed)
        
        decoded_payload = base64.urlsafe_b64decode(payload_base64).decode('utf-8')
        payload_data = json.loads(decoded_payload)
        
        token_data = TokenData(**payload_data)
    except (IndexError, ValueError, json.JSONDecodeError, ValidationError):
        raise credentials_exception
    
    if token_data.sub is None:
        raise credentials_exception
    return token_data.sub

def get_current_active_group_id(
    current_user_username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> int:
    user = crud_user.get_by_username(db, username=current_user_username)
    if not user or user.default_group_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not have an active group set.")
    return user.default_group_id