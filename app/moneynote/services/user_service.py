from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.moneynote.schemas.user import InitStateResponse, UserSessionVo, GroupSessionVo, BookSessionVo
from app.moneynote.models.user import User
from app.moneynote.crud import crud_user, crud_group, crud_book

def get_init_state(db: Session, current_user_username: str) -> InitStateResponse:
    user = crud_user.get_by_username(db, current_user_username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_session_vo = UserSessionVo(id=user.id, username=user.username, email=user.email)

    group_session_vo = None
    if user.default_group_id:
        group = crud_group.get(db, user.default_group_id)
        if group:
            group_session_vo = GroupSessionVo(id=group.id, name=group.name)

    book_session_vo = None
    if user.default_book_id:
        book = crud_book.get(db, user.default_book_id)
        if book:
            book_session_vo = BookSessionVo(id=book.id, name=book.name)

    return InitStateResponse(user=user_session_vo, group=group_session_vo, book=book_session_vo)
