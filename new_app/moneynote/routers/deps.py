from fastapi import Depends

from ..security import get_user_identity_from_token, oauth2_scheme


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    return get_user_identity_from_token(token)
