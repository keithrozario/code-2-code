from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_identity_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")