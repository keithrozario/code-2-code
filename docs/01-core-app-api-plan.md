# Technical Design: Phase 1 - Core Application and User Authentication

This document provides a detailed technical design for the first phase of the MoneyNote API implementation, focusing on setting up the application and implementing user authentication.

---

## Step 1: Setup FastAPI Application

**Goal:** Establish the foundational file structure, database connection, and initial data models for the application.

### Dependencies

- **FastAPI**: The main web framework.
- **Uvicorn**: The ASGI server to run the application.
- **SQLAlchemy**: The ORM for database interaction.
- **Pydantic**: For data validation and serialization (schemas).
- **python-dotenv**: To manage environment variables for configuration.

### Implementation Steps

1.  **Project Structure**:
    - Create the main application file: `main.py`.
    - Create supporting modules: `database.py`, `models.py`, `schemas.py`.
    - Create a configuration file: `.env` to store database URLs and secrets.

2.  **`database.py`**:
    - The file should facilitate communication to the sqllite db at `moneynote.db`
    - Create a SQLAlchemy `engine` instance.
    - Create a `SessionLocal` class using `sessionmaker`.
    - Create a declarative `Base` using `declarative_base()`.
    - Define a `get_db` dependency function that yields a database session and ensures it's closed after the request is finished.

3.  **`models.py`**:
    - Import `Base` from `database.py`.
    - Define a `User` class that inherits from `Base`.
        - Columns: `id` (Integer, Primary Key), `username` (String, Unique, Index), `email` (String, Unique, Index), `hashed_password` (String).
        - Add a relationship to `Group`.
    - Define a `Group` class that inherits from `Base`.
        - Columns: `id` (Integer, Primary Key), `name` (String), `owner_id` (Integer, ForeignKey to `user.id`).
        - Add a relationship back to `User`.

4.  **`schemas.py`**:
    - Define a `UserBase` Pydantic model with `username` and `email`.
    - Define a `UserCreate` model that inherits from `UserBase` and adds `password` (string).
    - Define a `User` model for responses that inherits from `UserBase` and adds `id` and `is_active` (boolean), with `orm_mode = True`.
    - Define `Token` and `TokenData` schemas for JWT handling.

5.  **`main.py`**:
    - Create the `FastAPI` app instance.
    - Call `models.Base.metadata.create_all(bind=engine)` to ensure tables are created on startup (for development).
    - Include a root `GET /` endpoint for health checks.

### Unit Test Cases

- **Test Database Connection**: Write a test that uses `SessionLocal` to connect to the database and execute a simple query (e.g., `SELECT 1`) to ensure the connection is valid.
- **Test `get_db` Dependency**: Test that the `get_db` dependency successfully provides a `Session` object.
- **Test Model Creation**: Verify that the `User` and `Group` tables are created correctly in the test database.

---

## Step 2: Implement User Registration

**Goal:** Create the public endpoint for new users to register.

### Dependencies

- **passlib**: For securely hashing and verifying passwords.
- All components from Step 1.

### Implementation Steps

1.  **Create `security.py`**:
    - Add `passlib.context.CryptContext` to manage password hashing (e.g., using `bcrypt`).
    - Create a `get_password_hash(password: str)` function.
    - Create a `verify_password(plain_password: str, hashed_password: str)` function.

2.  **Create `crud.py`**:
    - This module will contain reusable functions for database operations.
    - Create `get_user_by_username(db: Session, username: str)`.
    - Create `get_user_by_email(db: Session, email: str)`.
    - Create `create_user(db: Session, user: schemas.UserCreate)`:
        - Inside this function, call `get_password_hash` on the user's password.
        - Create a new `models.User` instance with the hashed password.
        - Create a default `models.Group` for the user.
        - Add, commit, and refresh the user object.

3.  **Create `api/users.py` Router**:
    - Create a new `APIRouter`.
    - Define the `POST /register` endpoint.
    - The endpoint will take a `schemas.UserCreate` object as the request body.
    - It will first check if a user with the same username or email already exists by calling the `get_user_by_*` functions from `crud.py`. If so, raise an `HTTPException` (400).
    - If the user is unique, call `crud.create_user` to create the new user.
    - Return the newly created user details (using the `schemas.User` response model to exclude the password).

4.  **Update `main.py`**:
    - Import the router from `api.users.py` and include it in the main FastAPI app using `app.include_router()`.

### Unit Test Cases

- `test_create_user_success`: A test that sends valid data to `POST /register` and asserts a `200 OK` status and the correct user data is returned (without the password).
- `test_create_user_duplicate_username`: A test that attempts to register a user with a username that already exists and asserts an `HTTPException` with status code `400`.
- `test_create_user_duplicate_email`: A test that attempts to register a user with an email that already exists and asserts an `HTTPException` with status code `400`.
- `test_password_hashing`: A test to verify that the password stored in the database for a new user is not the same as the plain text password sent.

---

## Step 3: Implement User Login

**Goal:** Create the endpoint for users to authenticate and receive an access token.

### Dependencies

- **python-jose**: For creating and signing JSON Web Tokens (JWT).
- **FastAPI `Security`**: Specifically `OAuth2PasswordRequestForm`.

### Implementation Steps

1.  **Update `security.py`**:
    - Add JWT configuration settings: `SECRET_KEY`, `ALGORITHM`, and `ACCESS_TOKEN_EXPIRE_MINUTES` (load from `.env`).
    - Create a function `create_access_token(data: dict, expires_delta: timedelta | None = None)` that generates and signs a JWT.

2.  **Update `crud.py`**:
    - Create an `authenticate_user(db: Session, username: str, password: str)` function:
        - It fetches the user by username using `get_user_by_username`.
        - If the user doesn't exist, it returns `False`.
        - It uses `verify_password` to check if the provided password matches the stored hash.
        - If passwords match, it returns the `models.User` object; otherwise, it returns `False`.

3.  **Update `api/users.py` Router**:
    - Define the `POST /login` endpoint.
    - The endpoint will depend on `form_data: OAuth2PasswordRequestForm = Depends()`.
    - Call `crud.authenticate_user` with `form_data.username` and `form_data.password`.
    - If authentication fails, raise an `HTTPException` (401) with an appropriate message.
    - If authentication succeeds, call `create_access_token` to generate a token.
    - Return a `schemas.Token` object containing the `access_token` and `token_type`.

### Unit Test Cases

- `test_login_success`: A test with valid credentials that asserts a `200 OK` status and that the response contains an `access_token`.
- `test_login_invalid_password`: A test with a valid username but incorrect password that asserts an `HTTPException` with status code `401`.
- `test_login_invalid_username`: A test with a non-existent username that asserts an `HTTPException` with status code `401`.

---

## Step 4: Implement Authentication Middleware

**Goal:** Create a reusable dependency to protect endpoints and retrieve the currently authenticated user.

### Dependencies

- **FastAPI `Security`**: Specifically `OAuth2PasswordBearer`.
- All components from previous steps.

### Implementation Steps

1.  **Update `security.py`**:
    - Create an `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")` instance.

2.  **Create `dependencies.py`**:
    - Create a `get_current_user(token: str = Depends(security.oauth2_scheme), db: Session = Depends(get_db))` function.
    - Inside the function, decode the JWT using `jose.jwt.decode`.
    - Extract the username from the token's `sub` claim.
    - If the username is missing or the token is invalid/expired, raise a `401 Unauthorized` `HTTPException`.
    - Fetch the user from the database via `crud.get_user_by_username`.
    - If the user doesn't exist, raise a `401 Unauthorized` `HTTPException`.
    - Return the user object.

3.  **Create a Test Endpoint**:
    - In `api/users.py`, create a new endpoint `GET /users/me`.
    - This endpoint will have a dependency on `get_current_user` (`current_user: models.User = Depends(dependencies.get_current_user)`).
    - The endpoint function will simply return the `current_user` object.

### Unit Test Cases

- `test_get_me_success`: Call `GET /users/me` with a valid `Authorization: Bearer <token>` header and assert a `200 OK` status and that the correct user data is returned.
- `test_get_me_no_token`: Call `GET /users/me` without an `Authorization` header and assert a `401 Unauthorized` status.
- `test_get_me_invalid_token`: Call `GET /users/me` with a malformed or incorrectly signed token and assert a `401 Unauthorized` status.
- `test_get_me_expired_token`: Call `GET /users/me` with an expired token and assert a `401 Unauthorized` status.
