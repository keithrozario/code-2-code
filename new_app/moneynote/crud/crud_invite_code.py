from typing import Optional

from sqlalchemy.orm import Session

from .base import CRUDBase
from moneynote.models.invite_code import InviteCode
from moneynote.schemas.invite_code import InviteCodeCreate, InviteCodeUpdate


class CRUDInviteCode(CRUDBase[InviteCode, InviteCodeCreate, InviteCodeUpdate]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[InviteCode]:
        return db.query(InviteCode).filter(InviteCode.code == code).first()


invite_code = CRUDInviteCode(InviteCode)
