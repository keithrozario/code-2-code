from sqlalchemy.orm import Session
from sqlalchemy import select

from app.moneynote.models.category import Category

def copy_categories(db: Session, from_book_id: int, to_book_id: int):
    categories = db.execute(select(Category).filter(Category.book_id == from_book_id)).scalars().all()
    category_map = {}

    # First pass: create all categories without parent_id
    for category in categories:
        new_category = Category(
            name=category.name,
            book_id=to_book_id,
            notes=category.notes,
            enable=category.enable,
            type=category.type,
            sort=category.sort,
        )
        db.add(new_category)
        db.flush() # Flush to get the new ID
        category_map[category.id] = new_category.id

    # Second pass: update parent_id
    for category in categories:
        if category.parent_id:
            new_parent_id = category_map.get(category.parent_id)
            if new_parent_id:
                new_category_id = category_map.get(category.id)
                if new_category_id:
                    new_category = db.get(Category, new_category_id)
                    if new_category:
                        new_category.parent_id = new_parent_id
                        db.add(new_category)

    db.commit()
