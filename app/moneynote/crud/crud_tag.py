from sqlalchemy.orm import Session
from sqlalchemy import select

from app.moneynote.models.tag import Tag

def copy_tags(db: Session, from_book_id: int, to_book_id: int):
    tags = db.execute(select(Tag).filter(Tag.book_id == from_book_id)).scalars().all()
    tag_map = {}

    # First pass: create all tags without parent_id
    for tag in tags:
        new_tag = Tag(
            name=tag.name,
            book_id=to_book_id,
            notes=tag.notes,
            enable=tag.enable,
            canExpense=tag.canExpense,
            canIncome=tag.canIncome,
            canTransfer=tag.canTransfer,
            sort=tag.sort,
        )
        db.add(new_tag)
        db.flush() # Flush to get the new ID
        tag_map[tag.id] = new_tag.id

    # Second pass: update parent_id
    for tag in tags:
        if tag.parent_id:
            new_parent_id = tag_map.get(tag.parent_id)
            if new_parent_id:
                new_tag_id = tag_map.get(tag.id)
                if new_tag_id:
                    new_tag = db.get(Tag, new_tag_id)
                    if new_tag:
                        new_tag.parent_id = new_parent_id
                        db.add(new_tag)

    db.commit()

def remove_by_book_id(db: Session, book_id: int):
    db.query(Tag).filter(Tag.book_id == book_id).delete(synchronize_session=False)
    db.commit()
