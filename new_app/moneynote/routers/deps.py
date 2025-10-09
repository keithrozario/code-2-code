from fastapi import Depends
from ..security import oauth2_scheme, get_user_identity_from_token

async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    return get_user_identity_from_token(token)
