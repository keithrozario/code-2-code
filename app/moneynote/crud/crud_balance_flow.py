from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.moneynote.models import BalanceFlow

def count_by_book_id(db: Session, book_id: int) -> int:
    return db.execute(select(func.count()).filter(BalanceFlow.book_id == book_id)).scalar_one()
