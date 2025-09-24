# Technical Design: Phase 3 - Supporting Entities (Categories, Tags, Payees)

This document provides a detailed technical design for the third phase of the MoneyNote API implementation. The goal of this phase is to build the CRUD (Create, Read, Update, Delete) functionality for the entities that are used to classify and add detail to transactions.

**Prerequisite**: All components from Phase 1 and Phase 2 must be completed and tested. This includes working CRUD APIs for Accounts and Books, and a robust authentication system.

---

## Step 1: Implement Category Management (CRUD)

**Goal:** Enable users to create, manage, and organize hierarchical categories for their transactions within a specific book.

### Dependencies

- All modules from previous phases.
- `Enum` from Python's standard library for `CategoryType`.

### Implementation Steps

1.  **Update `models.py`**:
    - Create a `Category` class inheriting from `Base`.
    - Define columns:
        - `id` (Integer, Primary Key)
        - `name` (String)
        - `type` (String) - To store `EXPENSE` or `INCOME`.
        - `book_id` (Integer, ForeignKey to `books.id`)
        - `parent_id` (Integer, ForeignKey to `categories.id`, nullable=True)
    - Define relationships:
        - `book = relationship("Book", back_populates="categories")`
        - `parent = relationship("Category", remote_side=[id], back_populates="children")`
        - `children = relationship("Category", back_populates="parent")`
    - In the `Book` model, add the back-populating relationship: `categories = relationship("Category", back_populates="book")`.

2.  **Update `schemas.py`**:
    - Create a `CategoryType(str, Enum)` with values `EXPENSE = "EXPENSE"` and `INCOME = "INCOME"`.
    - Create `CategoryBase(BaseModel)` with `name: str` and `type: CategoryType`.
    - Create `CategoryCreate(CategoryBase)` with an optional `parent_id: int | None = None`.
    - Create `CategoryUpdate(BaseModel)` with all fields from `CategoryBase` as optional.
    - Create a `Category(CategoryBase)` response schema that includes `id: int`, `book_id: int`, and `parent_id: int | None`. Ensure `Config.orm_mode = True`.

3.  **Update `crud.py`**:
    - `create_category(db: Session, category: schemas.CategoryCreate, book_id: int)`: Creates a new `models.Category`.
    - `get_categories_by_book(db: Session, book_id: int)`: Retrieves all categories for a given book.
    - `get_category(db: Session, category_id: int)`: Retrieves a single category by its ID.
    - `delete_category(db: Session, db_category: models.Category)`: Deletes a category. Add a check to prevent deletion if the category has children (`if db_category.children:`).

4.  **Create `api/categories.py`**:
    - Create a new `APIRouter`.
    - **`POST /`**: Depends on `get_current_user`. Takes a `book_id` and a `CategoryCreate` schema. It must verify the user owns the book before calling `crud.create_category`.
    - **`GET /`**: Depends on `get_current_user`. Takes a `book_id` as a query parameter. It must verify the user owns the book before calling `crud.get_categories_by_book`.
    - **`DELETE /{category_id}`**: Depends on `get_current_user`. Fetches the category, verifies it belongs to a book the user owns, and then calls `crud.delete_category`.

5.  **Update `main.py`**:
    - Import the new router from `api.categories` and include it in the main app with a `/categories` prefix.

### Unit Test Cases

- `test_create_category_for_owned_book`: As an authenticated user, create a book, then create a category for that book. Assert 200 OK.
- `test_create_category_for_unowned_book`: Create two users. As User 1, try to create a category for a book owned by User 2. Assert 404 Not Found (as the book is not visible to User 1).
- `test_get_categories_for_book`: Create a book and several categories. Query the `GET /categories?book_id=...` endpoint and assert the correct categories are returned.
- `test_delete_category_fails_if_has_children`: Create a parent and a child category. Attempt to delete the parent and assert 400 Bad Request.
- `test_delete_empty_category_success`: Create a category with no children and delete it successfully.

---

## Step 2: Implement Tag Management (CRUD)

**Goal:** Enable users to create and manage tags for transactions within a specific book.

### Dependencies

- All components from previous steps.

### Implementation Steps

1.  **Update `models.py`**:
    - Create a `Tag` class inheriting from `Base`.
    - Define columns: `id`, `name`, `book_id` (ForeignKey to `books.id`).
    - Define relationship: `book = relationship("Book", back_populates="tags")`.
    - In the `Book` model, add the back-populating relationship: `tags = relationship("Tag", back_populates="book")`.

2.  **Update `schemas.py`**:
    - Create `TagBase`, `TagCreate`, `TagUpdate`, and `Tag` (response) Pydantic schemas.

3.  **Update `crud.py`**:
    - Add CRUD functions for tags: `create_tag`, `get_tags_by_book`, `get_tag`, `delete_tag`.

4.  **Create `api/tags.py`**:
    - Create a new `APIRouter`.
    - Implement `POST` and `GET` endpoints, scoped by `book_id` and protected by `get_current_user` with ownership verification.
    - Implement `DELETE /{tag_id}` with ownership verification.

5.  **Update `main.py`**:
    - Import and include the new `tags` router.

### Unit Test Cases

- `test_create_tag_for_owned_book`: Create a book and then a tag for it. Assert 200 OK.
- `test_get_tags_for_book`: Create a book and several tags. Query for them and assert they are returned.
- `test_delete_tag_success`: Create and delete a tag successfully.
- `test_user_cannot_see_tags_for_unowned_book`: As User 1, attempt to get tags for a book owned by User 2. Assert an empty list is returned.

---

## Step 3: Implement Payee Management (CRUD)

**Goal:** Enable users to create and manage a list of payees (merchants, people) for their transactions.

### Dependencies

- All components from previous steps.

### Implementation Steps

1.  **Update `models.py`**:
    - Create a `Payee` class inheriting from `Base`.
    - Define columns: `id`, `name`, `book_id` (ForeignKey to `books.id`).
    - Define relationship: `book = relationship("Book", back_populates="payees")`.
    - In the `Book` model, add the back-populating relationship: `payees = relationship("Payee", back_populates="book")`.

2.  **Update `schemas.py`**:
    - Create `PayeeBase`, `PayeeCreate`, `PayeeUpdate`, and `Payee` (response) Pydantic schemas.

3.  **Update `crud.py`**:
    - Add CRUD functions for payees: `create_payee`, `get_payees_by_book`, `get_payee`, `delete_payee`.

4.  **Create `api/payees.py`**:
    - Create a new `APIRouter`.
    - Implement `POST`, `GET`, and `DELETE` endpoints, scoped by `book_id` and protected by `get_current_user` with ownership verification.

5.  **Update `main.py`**:
    - Import and include the new `payees` router.

### Unit Test Cases

- `test_create_payee_for_owned_book`: Create a book and then a payee for it. Assert 200 OK.
- `test_get_payees_for_book`: Create a book and several payees. Query for them and assert they are returned.
- `test_delete_payee_success`: Create and delete a payee successfully.
