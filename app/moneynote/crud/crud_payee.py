from sqlalchemy.orm import Session
from sqlalchemy import select

from app.moneynote.models.payee import Payee

def copy_payees(db: Session, from_book_id: int, to_book_id: int):
    payees = db.execute(select(Payee).filter(Payee.book_id == from_book_id)).scalars().all()
    for payee in payees:
        new_payee = Payee(
            name=payee.name,
            book_id=to_book_id,
            notes=payee.notes,
            enable=payee.enable,
            canExpense=payee.canExpense,
            canIncome=payee.canIncome,
            sort=payee.sort,
        )
        db.add(new_payee)
    db.commit()

def remove_by_book_id(db: Session, book_id: int):
    db.query(Payee).filter(Payee.book_id == book_id).delete(synchronize_session=False)
    db.commit()
