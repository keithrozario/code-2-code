# API Implementation Plan

This document provides a phased, step-by-step plan for building the MoneyNote API. The plan is structured to respect the dependencies between different parts of the application, ensuring a logical and stable development process.

## Phase 1: Core Application and User Authentication

**Goal:** Establish the basic application structure and enable user registration and authentication. This is the foundation for all subsequent features.

1.  **Setup FastAPI Application**:
    - Initialize the main app in `main.py`.
    - Create the database connection logic in `database.py`.
    - Create `models.py` and define the initial `User` and `Group` SQLAlchemy models.
    - Create `schemas.py` and define the Pydantic schemas for User creation and login.

2.  **Implement User Registration**:
    - **Endpoint**: `POST /register`
    - **Details**: Create a new user and an associated default group. Hash the password before saving.

3.  **Implement User Login**:
    - **Endpoint**: `POST /login`
    - **Details**: Authenticate a user against the database and return a JWT access token.

4.  **Implement Authentication Middleware**:
    - **Details**: Create a security dependency that validates the JWT token on all protected endpoints and makes the current user's data available to the request.

## Phase 2: Foundational Structures (Accounts & Books)

**Goal:** Allow authenticated users to create the core structures for bookkeeping: accounts and books.

1.  **Implement Account Management (CRUD)**:
    - **Models/Schemas**: Add `Account` model and Pydantic schemas.
    - **Endpoints**:
        - `POST /accounts`: Create a new financial account.
        - `GET /accounts`: List all accounts for the user's group.
        - `PUT /accounts/{id}`: Update an account.
        - `DELETE /accounts/{id}`: Delete an account.

2.  **Implement Book Management (CRUD)**:
    - **Models/Schemas**: Add `Book` model and Pydantic schemas.
    - **Endpoints**:
        - `POST /books`: Create a new, empty book.
        - `GET /books`: List all books for the user's group.
        - `PUT /books/{id}`: Update a book's details.
        - `DELETE /books/{id}`: Delete a book (with validation to prevent deleting books with transactions).

3.  **Implement Advanced Book Creation**:
    - **Endpoints**:
        - `POST /books/template`: Create a book from a predefined template.
        - `POST /books/copy`: Create a book by copying an existing one.

## Phase 3: Supporting Entities (Categories, Tags, Payees)

**Goal:** Build the CRUD functionality for entities that classify and add detail to transactions.

1.  **Implement Category Management (CRUD)**:
    - **Models/Schemas**: Add `Category` model and Pydantic schemas.
    - **Endpoints**: `POST /categories`, `GET /categories`, `PUT /categories/{id}`, `DELETE /categories/{id}`. All endpoints should be scoped to a specific book.

2.  **Implement Tag Management (CRUD)**:
    - **Models/Schemas**: Add `Tag` model and Pydantic schemas.
    - **Endpoints**: `POST /tags`, `GET /tags`, `PUT /tags/{id}`, `DELETE /tags/{id}`. (These are implied by the data model).

3.  **Implement Payee Management (CRUD)**:
    - **Models/Schemas**: Add `Payee` model and Pydantic schemas.
    - **Endpoints**: `POST /payees`, `GET /payees`, `PUT /payees/{id}`, `DELETE /payees/{id}`. (These are implied by the data model).

## Phase 4: Core Transaction Management

**Goal:** Implement the central feature of the application: creating and managing transactions (Balance Flows).

1.  **Implement Transaction Models**:
    - **Models**: Add `BalanceFlow`, `CategoryRelation`, and `TagRelation` models.
    - **Schemas**: Add Pydantic schemas for creating and displaying transactions.

2.  **Implement Transaction Creation**:
    - **Endpoint**: `POST /balance-flows`
    - **Details**: This is a complex endpoint. It needs to handle the creation of the main `BalanceFlow` record as well as its links to categories and tags. It must also trigger the logic to update the corresponding account's balance if the transaction is confirmed.

3.  **Implement Transaction Viewing and Deletion**:
    - **Endpoints**:
        - `GET /balance-flows`: List and filter transactions.
        - `GET /balance-flows/{id}`: View a single transaction.
        - `DELETE /balance-flows/{id}`: Delete a transaction and correctly refund the account balance.

4.  **Implement Transaction Updates**:
    - **Endpoints**:
        - `PUT /balance-flows/{id}`: Implement the destructive update (delete and re-create) logic.
        - `PATCH /balance-flows/{id}/confirm`: Confirm a pending transaction.

## Phase 5: File Attachments

**Goal:** Allow users to attach files to the transactions created in the previous phase.

1.  **Implement File Attachment Logic**:
    - **Models/Schemas**: Add `FlowFile` model and Pydantic schemas.
    - **Endpoint**: `POST /balance-flows/{id}/addFile`
    - **Details**: Handle multipart file uploads and associate the file with a transaction.

2.  **Implement File Viewing and Deletion**:
    - **Endpoints**:
        - `GET /flow-files/view`: Securely serve the content of an uploaded file.
        - `DELETE /flow-files/{id}`: Delete a file attachment.

## Phase 6: Reporting Endpoints

**Goal:** Provide read-only, aggregated data for financial analysis. This phase depends on all previous phases.

1.  **Implement Account-Based Reports**:
    - **Endpoints**:
        - `GET /accounts/overview`: Calculate and return net worth.
        - `GET /reports/balance`: Provide data for asset vs. debt charts.

2.  **Implement Transaction-Based Reports**:
    - **Endpoints**:
        - `GET /reports/expense-category`: Aggregate expenses by category.
        - (Implement other reporting endpoints like `expense-tag` as needed).

## Phase 7: Currency Management

**Goal:** Add multi-currency support. This can be developed in parallel but should be integrated carefully as it affects many other features.

1.  **Implement Currency Service**:
    - **Details**: Create a service to load currency data from a file and refresh it from an external API.

2.  **Implement Currency Endpoints**:
    - **Endpoints**:
        - `GET /currencies`: List available currencies.
        - `GET /currencies/calc`: Provide a utility for on-the-fly conversions.
        - `PUT /currencies/{id}/rate`: Allow manual rate overrides for the session.
        - `POST /currencies/refresh`: Trigger a manual refresh of rates.
