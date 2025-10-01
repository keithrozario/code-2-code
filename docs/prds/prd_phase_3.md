# Product Requirements Document: Moneynote API - Phase 3

## 1) Goal & Scope

The goal of this phase is to implement the foundational APIs for creating core data structures within the Moneynote application. This phase focuses exclusively on the creation of "Groups" and "Books," which are essential for organizing a user's financial data. This will enable users to set up their initial accounting structure, either from scratch, from a predefined template, or by copying an existing setup.

## 2) Functional Specifications

*   **FS-001: Group Creation:** Authenticated users must be able to create a new "Group" to hold their financial books.
*   **FS-002: Book Creation:** Authenticated users must be able to create a new, empty "Book" within a group, specifying a name and default currency.
*   **FS-003: Book Creation from Template:** Users must be able to create a new "Book" from a list of predefined templates, which pre-populates the book with standard categories, tags, and payees.
*   **FS-004: Book Copying:** Users must be able to create a new "Book" by duplicating an existing book they have access to, preserving its structure of categories, tags, and payees.

## 3) UI / UX Flow

While this PRD is for the backend API, the conceptual user flow is as follows:

1.  A user signs up and logs in (Phases 1 & 2).
2.  To begin, the user is prompted to create a **Group** (e.g., "Personal", "Family"). The user provides a name and other details.
3.  Within that Group, the user is prompted to create their first **Book** (e.g., "Daily Spending").
4.  The user is presented with three options for book creation:
    *   **Start Fresh:** Creates a blank book where the user must configure everything manually. -> `POST /books`
    *   **Use a Template:** The user selects from a list like "Standard Household" or "Small Business". -> `POST /books/template`
    *   **Copy Existing:** If other books exist, the user can select one to duplicate. -> `POST /books/copy`
5.  Upon successful creation, the user can start adding accounts and recording transactions within the new book.

## 4) Technical Specifications

### 4.1 API Logic

---

#### **Endpoint: `POST /groups`**

*   **Description:** Adds a new group for the authenticated user. A group acts as a container for multiple books and allows for collaboration. Creating a group from a template also creates an initial book.

*   **Business Logic:**
    *   Validates that the `name` for the group is unique for the user.
    *   Validates that the `templateId` is valid.
    *   Creates a new `Group` entity associated with the current user.
    *   Creates a default `Book` within the group using the structure from the specified template (`templateId`). This involves creating associated `Category`, `Tag`, and `Payee` records for the new book.

*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
    *   **Request Body (`GroupAddForm`):**
        | Name | Data type | Optionality | Description |
        | :--- | :--- | :--- | :--- |
        | `name` | String | Mandatory | Name for the new group. |
        | `defaultCurrencyCode` | String | Mandatory | Default currency for the group (e.g., "USD"). |
        | `notes` | String | Optional | Descriptive notes for the group. |
        | `templateId` | Integer | Mandatory | The ID of the template to use for the initial book. |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the newly created `Group` object.
    *   **400 Bad Request:**
        *   If the `name` is missing or empty.
        *   If `defaultCurrencyCode` is missing or invalid.
        *   If `templateId` is missing or invalid.
        *   If the group name already exists for the user.
    *   **401 Unauthorized:** If the JWT token is missing or invalid.

*   **Database CRUD Operations:**
    *   `CREATE`: A new record in the `t_user_group` table.
    *   `CREATE`: A new record in the `t_user_book` table for the default book.
    *   `CREATE`: Multiple records in `t_user_category`, `t_user_tag`, and `t_user_payee` based on the template.
    *   `READ`: The `t_user_group` table to check for name uniqueness.
    *   `READ`: The book template definition (e.g., from `book_tpl.json`).

*   **Database SQL Statements:**
    ```sql
    -- Check for existing group name
    SELECT COUNT(*) FROM t_user_group WHERE creator_id = ? AND name = ?;

    -- Insert new group
    INSERT INTO t_user_group (name, notes, default_currency_code, creator_id) VALUES (?, ?, ?, ?);

    -- Insert new book (and associated categories, tags, payees from template)
    INSERT INTO t_user_book (name, group_id, default_currency_code, ...) VALUES (?, ?, ?, ...);
    INSERT INTO t_user_category (name, book_id, type, ...) VALUES (?, ?, ?, ...);
    -- ... more inserts for tags and payees
    ```

---

#### **Endpoint: `POST /books`**

*   **Description:** Adds a new, empty book to the user's current group.

*   **Business Logic:**
    *   Validates that the `name` for the book is unique within the current `Group`.
    *   Checks if the user has exceeded the maximum number of books allowed per group.
    *   Creates a new `Book` entity associated with the user's current group.
    *   No categories, tags, or payees are created.

*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
    *   **Request Body (`BookAddForm`):**
        | Name | Data type | Optionality | Description |
        | :--- | :--- | :--- | :--- |
        | `name` | String | Mandatory | Name for the new book. |
        | `defaultCurrencyCode` | String | Mandatory | Default currency for the book (e.g., "USD"). |
        | `defaultExpenseAccountId` | Integer | Optional | ID of the default account for expenses. |
        | `defaultIncomeAccountId` | Integer | Optional | ID of the default account for income. |
        | `notes` | String | Optional | Descriptive notes for the book. |
        | `sort` | Integer | Optional | A number for sorting the book in a list. |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the newly created `Book` object.
    *   **400 Bad Request:**
        *   If the `name` is missing or already exists within the group.
        *   If `defaultCurrencyCode` is missing or invalid.
        *   If the user has reached the maximum book limit for the group.
    *   **401 Unauthorized:** If the JWT token is missing or invalid.

*   **Database CRUD Operations:**
    *   `CREATE`: A new record in the `t_user_book` table.
    *   `READ`: The `t_user_book` table to check for name uniqueness within the group.
    *   `READ`: The `t_user_book` table to count the number of books in the group.

*   **Database SQL Statements:**
    ```sql
    -- Check for existing book name in group
    SELECT COUNT(*) FROM t_user_book WHERE group_id = ? AND name = ?;

    -- Check book count in group
    SELECT COUNT(*) FROM t_user_book WHERE group_id = ?;

    -- Insert new book
    INSERT INTO t_user_book (name, group_id, default_currency_code, notes, sort, default_expense_account_id, default_income_account_id) VALUES (?, ?, ?, ?, ?, ?, ?);
    ```

---

#### **Endpoint: `POST /books/template`**

*   **Description:** Adds a new book to the user's current group based on a predefined template.

*   **Business Logic:**
    *   Validates that the `templateId` is valid.
    *   Performs the same validations as `POST /books` (unique name, max book count).
    *   Creates a new `Book` entity.
    *   Reads the specified template (from `book_tpl.json`) and creates new `Category`, `Tag`, and `Payee` entities associated with the new book.

*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
    *   **Request Body (`BookAddByTemplateForm`):**
        | Name | Data type | Optionality | Description |
        | :--- | :--- | :--- | :--- |
        | `templateId` | Integer | Mandatory | The ID of the template to use. |
        | `book` | `BookAddForm` | Mandatory | The details for the new book (name, currency, etc.). |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the newly created `Book` object.
    *   **400 Bad Request:**
        *   If `templateId` is invalid.
        *   If any validation from the nested `BookAddForm` fails (e.g., duplicate name).
    *   **401 Unauthorized:** If the JWT token is missing or invalid.

*   **Database CRUD Operations:**
    *   `CREATE`: A new record in `t_user_book`.
    *   `CREATE`: Multiple records in `t_user_category`.
    *   `CREATE`: Multiple records in `t_user_tag`.
    *   `CREATE`: Multiple records in `t_user_payee`.
    *   `READ`: Book template definition (from `book_tpl.json`).
    *   `READ`: `t_user_book` for validation.

*   **Database SQL Statements:**
    ```sql
    -- Validations (same as POST /books)

    -- Insert new book
    INSERT INTO t_user_book (name, group_id, ...) VALUES (?, ?, ...);

    -- Get new book ID
    -- SELECT LAST_INSERT_ID();

    -- Insert categories, tags, and payees from template
    INSERT INTO t_user_category (book_id, name, type, ...) VALUES (?, ?, ?, ...);
    INSERT INTO t_user_tag (book_id, name, ...) VALUES (?, ?, ...);
    INSERT INTO t_user_payee (book_id, name, ...) VALUES (?, ?, ...);
    -- (Repeat for all items in template)
    ```

---

#### **Endpoint: `POST /books/copy`**

*   **Description:** Adds a new book by copying the structure (categories, tags, payees) of an existing book.

*   **Business Logic:**
    *   Validates that the source `bookId` exists and the user has access to it.
    *   Performs the same validations as `POST /books` (unique name for the new book, max book count).
    *   Creates a new `Book` entity.
    *   Copies all `Category`, `Tag`, and `Payee` entities from the source book and associates the new copies with the new book.

*   **Request Parameters:**
    *   **Headers:**
        *   `Authorization: Bearer <JWT_TOKEN>` (Mandatory)
    *   **Request Body (`BookAddByBookForm`):**
        | Name | Data type | Optionality | Description |
        | :--- | :--- | :--- | :--- |
        | `bookId` | Integer | Mandatory | The ID of the source book to copy. |
        | `book` | `BookAddForm` | Mandatory | The details for the new book (name, currency, etc.). |

*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the newly created `Book` object.
    *   **400 Bad Request:**
        *   If source `bookId` is invalid or not accessible.
        *   If any validation from the nested `BookAddForm` fails.
    *   **401 Unauthorized:** If the JWT token is missing or invalid.

*   **Database CRUD Operations:**
    *   `CREATE`: A new record in `t_user_book`.
    *   `CREATE`: Multiple new records in `t_user_category`.
    *   `CREATE`: Multiple new records in `t_user_tag`.
    *   `CREATE`: Multiple new records in `t_user_payee`.
    *   `READ`: The source `Book` and its related categories, tags, and payees.
    *   `READ`: `t_user_book` for validation.

*   **Database SQL Statements:**
    ```sql
    -- Validations (same as POST /books)

    -- Read categories, tags, payees from source book
    SELECT * FROM t_user_category WHERE book_id = ?;
    SELECT * FROM t_user_tag WHERE book_id = ?;
    SELECT * FROM t_user_payee WHERE book_id = ?;

    -- Insert new book
    INSERT INTO t_user_book (name, group_id, ...) VALUES (?, ?, ...);

    -- Get new book ID

    -- Insert copied categories, tags, and payees
    INSERT INTO t_user_category (book_id, name, type, ...) VALUES (?, ?, ?, ...); -- New book_id, old data
    -- (Repeat for all items)
    ```

## 5) Data Model

This phase impacts the `Group` and `Book` entities, along with their relationships.

### `t_user_group` Table

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO_INCREMENT` | Unique identifier for the group. |
| `name` | `VARCHAR` | `NOT NULL` | Name of the group. |
| `notes` | `VARCHAR(1024)` | | Optional descriptive notes. |
| `default_currency_code` | `VARCHAR(8)` | `NOT NULL` | Default currency for the group. |
| `creator_id` | `INTEGER` | `FK to t_user` | The user who created the group. |
| `...` | | | Other columns like `insert_at`, `update_at`. |

### `t_user_book` Table

| Column | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PK`, `AUTO_INCREMENT` | Unique identifier for the book. |
| `name` | `VARCHAR` | `NOT NULL` | Name of the book, unique within a group. |
| `group_id` | `INTEGER` | `FK to t_user_group`, `NOT NULL` | The group this book belongs to. |
| `notes` | `VARCHAR(1024)` | | Optional descriptive notes. |
| `enable` | `BOOLEAN` | `NOT NULL`, `DEFAULT true` | Whether the book is active. |
| `default_currency_code` | `VARCHAR(8)` | `NOT NULL` | Default currency for transactions in this book. |
| `default_expense_account_id` | `INTEGER` | `FK to t_user_account` | Optional default expense account. |
| `default_income_account_id` | `INTEGER` | `FK to t_user_account` | Optional default income account. |
| `sort` | `INTEGER` | | Sort order. |
| `...` | | | Other columns like `insert_at`, `update_at`. |

## 6) Test Cases

| Test Case ID | Endpoint | Feature Being Tested | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-P3-01** | `POST /groups` | Happy Path - Group Creation | Send a valid `GroupAddForm`. | 200 OK. A new Group and a default Book are created. |
| **TC-P3-02** | `POST /books` | Happy Path - Book Creation | Send a valid `BookAddForm` with a unique name. | 200 OK. A new, empty Book is created. |
| **TC-P3-03** | `POST /books` | Negative Path - Duplicate Name | Send a `BookAddForm` with a name that already exists in the group. | 400 Bad Request with an error message indicating the name is taken. |
| **TC-P3-04** | `POST /books/template` | Happy Path - Book from Template | Send a `BookAddByTemplateForm` with a valid `templateId` and book details. | 200 OK. A new Book is created with categories, tags, and payees from the template. |
| **TC-P3-05** | `POST /books/template` | Negative Path - Invalid Template ID | Send a `BookAddByTemplateForm` with a non-existent `templateId`. | 400 Bad Request with an error message. |
| **TC-P3-06** | `POST /books/copy` | Happy Path - Copy Book | Send a `BookAddByBookForm` with a valid source `bookId` and new book details. | 200 OK. A new Book is created that mirrors the structure of the source book. |
| **TC-P3-07** | `POST /books/copy` | Negative Path - Invalid Source Book | Send a `BookAddByBookForm` with a `bookId` that doesn't exist or the user can't access. | 400 Bad Request with an error message. |

## 7) Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| **Race Condition on Name Uniqueness:** Two simultaneous requests try to create a book with the same name. | Low | Medium | Add a `UNIQUE` constraint to the database on `(group_id, name)` for the `t_user_book` table. This provides a definitive safeguard. |
| **Inconsistent Data on Copy/Template:** The process of copying entities from a template or another book fails midway. | Low | High | Wrap the entire creation process (book + categories + tags + payees) in a single database transaction. If any part fails, the entire operation is rolled back. |
| **Template File Not Found/Corrupt:** The `book_tpl.json` file is missing or malformed, breaking the `POST /groups` and `POST /books/template` endpoints. | Medium | High | Implement robust error handling during application startup. Log a critical error and potentially prevent the application from starting if templates are essential. The endpoints should return a clear server error if a template cannot be loaded. |

## 8) Open Questions

1.  What is the defined maximum number of books allowed per group? The logic checks for a limit, but the value is not specified in the documents.
2.  What are the specific user roles or permissions required to create a group or a book? Is it just any authenticated user, or are there group-level roles (e.g., admin, member)?
3.  How are the book templates (`book_tpl.json`) created, managed, and versioned? Is this a manual process?
4.  When a group is created, the `GroupAddForm` requires a `templateId`. Does this mean it's impossible to create a group with an empty book initially?

## 9) Task Seeds (for Agent Decomposition)

*   Implement `POST /groups` endpoint in `GroupController`.
*   Implement `GroupService.add` method, including logic to call `BookService.addByTpl`.
*   Implement `POST /books` endpoint in `BookController`.
*   Implement `BookService.add` method with validations for unique name and max count.
*   Implement `POST /books/template` endpoint in `BookController`.
*   Implement `BookService.addByTpl` method to load template data and create associated entities.
*   Implement `POST /books/copy` endpoint in `BookController`.
*   Implement `BookService.addByBook` method to copy entities from a source book.
*   Add database transaction management (`@Transactional`) to all service methods that perform multiple database writes.
*   Write unit tests for `BookService` covering `add`, `addByTpl`, and `addByBook`.
*   Write integration tests for all four new endpoints.
*   Add `UNIQUE` constraint on `(group_id, name)` to the `t_user_book` database schema.
