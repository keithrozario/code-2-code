## 11. Define Pydantic Schemas for Account Binding and Initial State

Create the necessary Pydantic schemas to support the new endpoints. This includes a request body schema for account binding and response schemas for the initial state hydration.

In `moneynote/schemas/user.py`, create a `UserBind` schema with `username`, `password`, and `inviteCode` fields. In `moneynote/schemas/user.py`, `book.py`, and `group.py`, define the response VOs: `UserSessionVo`, `BookSessionVo`, and `GroupSessionVo`. Finally, create a container schema `InitStateResponse` in `moneynote/schemas/user.py` that includes `user: UserSessionVo`, `book: BookSessionVo | None`, and `group: GroupSessionVo | None`.

**Test Strategy**: Unit tests are not required for Pydantic models. Correct implementation will be verified by integration tests for the endpoints that use them.


### Subtasks

#### 11.1 Create `UserBind` Schema for Account Binding Request

In `moneynote/schemas/user.py`, define a new Pydantic schema `UserBind` to validate the request body for the account binding endpoint.

Based on the analysis of `moneynote/schemas/user.py`, create a new class `UserBind` that inherits from `pydantic.BaseModel`. This schema will be used for the request body of the new account binding endpoint. It must contain the following fields: `username: str`, `password: str`, and `inviteCode: str`.

**Test Strategy**: 


#### 11.2 Create `UserSessionVo` Schema for Initial State

In `moneynote/schemas/user.py`, define the `UserSessionVo` schema to represent the user's session data in the initial state response.

In `moneynote/schemas/user.py`, create a new schema `UserSessionVo`. Based on the `moneynote.models.User` model, it should include `id: int`, `username: str`, `is_guest: bool`, `default_book_id: int | None`, and `default_group_id: int | None`. Ensure it includes a `Config` inner class with `orm_mode = True` to be compatible with SQLAlchemy models, following the pattern of `UserInDBBase`.

**Test Strategy**: 


#### 11.3 Create `BookSessionVo` Schema for Initial State

In `moneynote/schemas/book.py`, define the `BookSessionVo` schema to represent the user's default book data in the initial state response.

In the existing file `moneynote/schemas/book.py`, create a new schema `BookSessionVo`. This schema will be a simplified representation of a book for the initial state. It should include `id: int` and `name: str`. Ensure it includes a `Config` inner class with `orm_mode = True`, similar to the existing `BookInDBBase` schema.

**Test Strategy**: 


#### 11.4 Create `group.py` Schema File and Define `GroupSessionVo`

Create a new schema file `moneynote/schemas/group.py` and define the `GroupSessionVo` schema to represent the user's default group data in the initial state response.

Create a new file at `moneynote/schemas/group.py`. Inside this file, define a `GroupSessionVo` schema that includes `id: int` and `name: str`. It must have a `Config` inner class with `orm_mode = True`. To maintain consistency with other schema files like `book.py`, also create a `GroupBase` schema containing `name: str | None = None`.

**Test Strategy**: 


#### 11.5 Create `InitStateResponse` Container Schema

In `moneynote/schemas/user.py`, create the main `InitStateResponse` schema that aggregates the user, book, and group session data for the initial state endpoint.

In `moneynote/schemas/user.py`, define the final container schema `InitStateResponse`. This schema must import `BookSessionVo` from `moneynote.schemas.book` and `GroupSessionVo` from `moneynote.schemas.group`. It will contain three fields: `user: UserSessionVo`, `book: BookSessionVo | None`, and `group: GroupSessionVo | None`.

**Test Strategy**: 


## 12. Implement Password Hashing Utility

Create a centralized utility for securely hashing and verifying passwords using a strong algorithm like bcrypt.

In `moneynote/security.py`, use the `passlib` library, which is already a dependency. Create a `CryptContext` instance configured for bcrypt. Implement two functions: `hash_password(password: str) -> str` and `verify_password(plain_password: str, hashed_password: str) -> bool`.

**Test Strategy**: Write unit tests for the `security.py` module to verify that a given password can be hashed and then successfully verified, and that it fails for an incorrect password.


### Subtasks

#### 12.1 Configure CryptContext in security.py

In `moneynote/security.py`, create and configure the `CryptContext` instance for password hashing.

Locate the comment `# Password hashing context will be defined here` in `moneynote/security.py`. Instantiate `CryptContext` from the `passlib.context` library. Configure the context to use `bcrypt` as the scheme, like so: `pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")`.

**Test Strategy**: This is a setup task; its correctness will be verified by the functionality of subsequent subtasks.


#### 12.2 Implement the hash_password function

Create the `hash_password` function in `moneynote/security.py` to generate a bcrypt hash of a given password.

In `moneynote/security.py`, define a new function `hash_password(password: str) -> str`. This function should use the `pwd_context` instance created in the previous subtask. Call the `pwd_context.hash()` method, passing the plain password to it, and return the resulting hash string.

**Test Strategy**: Unit tests in a later subtask will verify that this function returns a non-empty string that is different from the input password.


#### 12.3 Implement the verify_password function

Create the `verify_password` function in `moneynote/security.py` to compare a plain password against a hashed password.

In `moneynote/security.py`, define a new function `verify_password(plain_password: str, hashed_password: str) -> bool`. This function will use the `pwd_context.verify()` method, passing it the plain password and the hashed password. Return the boolean result of this method call.

**Test Strategy**: Unit tests will be written to confirm this function returns `True` for a correct password and `False` for an incorrect one.


#### 12.4 Create a new test file for security utilities

Create a new file `tests/test_security.py` to house the unit tests for the password hashing and verification functions.

In the `tests/` directory, create a new file named `test_security.py`. Add the necessary imports, including `pytest` and the `hash_password` and `verify_password` functions from `moneynote.security`.

**Test Strategy**: This subtask is structural. The existence and basic structure of the file will be its deliverable.


#### 12.5 Write unit tests for password hashing and verification

In `tests/test_security.py`, add unit tests to validate the `hash_password` and `verify_password` functions.

In `tests/test_security.py`, create a test function, e.g., `test_password_hashing_and_verification`. Inside this test: 1. Define a sample password. 2. Call `hash_password` to get a hashed version. 3. Assert that the hashed password is not the same as the plain password. 4. Call `verify_password` with the correct plain password and the hash, and assert the result is `True`. 5. Call `verify_password` with an incorrect plain password and the hash, and assert the result is `False`.

**Test Strategy**: This task implements the test strategy defined in the parent task, ensuring the utility works as expected.


## 13. Extend User CRUD for Account Binding

Add functions to the user CRUD layer to support checking for username existence and updating a user's credentials.

In `moneynote/crud/crud_user.py`, add a new function `get_by_username(db: Session, *, username: str) -> models.User | None`. Modify or add an `update` function that can take the user object and a dictionary of data to update the `username` and `hashed_password` fields in the database.

**Test Strategy**: Write unit tests for the new CRUD functions. Test `get_by_username` for both a user that exists and one that does not. Test the update function to ensure it correctly modifies the user record in the test database.


### Subtasks

#### 13.1 Implement `get_by_username` function in `CRUDUser`

Add a new method to the `CRUDUser` class to retrieve a user record from the database based on their username.

In the file `moneynote/crud/crud_user.py`, add a new method `get_by_username(self, db: Session, *, username: str) -> models.User | None` to the `CRUDUser` class. This method should perform a query on the `User` model, filtering by the `username` field, and return the first result or `None` if not found. This will be similar to the existing `get_by_email` method.

**Test Strategy**: A unit test will be created in a subsequent subtask to verify this function's correctness for both existing and non-existing usernames.


#### 13.2 Verify and ensure `CRUDUser.update` supports credential updates

Analyze the existing `update` method in `CRUDUser` and its base class to confirm it can handle updates to the `username` and `password` fields.

In `moneynote/crud/crud_user.py`, review the `update` method. Based on analysis of `CRUDBase`, the method should already support updating arbitrary fields like `username`. The existing `CRUDUser.update` method already handles hashing for a new `password`. This subtask is to verify this behavior and ensure no further modifications are needed to support the task requirements. If the implementation is sufficient, add a comment clarifying that it supports `username` and `password` updates.

**Test Strategy**: The functionality will be confirmed via a dedicated unit test in a later subtask.


#### 13.3 Enhance test utilities for user creation with username

Update the test utility functions to allow for the creation of test users that include a username.

Locate the test utility function responsible for creating users for tests (e.g., `create_random_user` in `moneynote/tests/utils/user.py`). Modify this function to optionally accept a `username` parameter. If a username is provided, the created `User` object should have its `username` field populated.

**Test Strategy**: This change will be implicitly tested by the new CRUD tests that rely on it.


#### 13.4 Write unit test for `get_by_username`

Add a unit test to verify the functionality of the new `get_by_username` CRUD function.

In the relevant test file, likely `moneynote/tests/crud/test_user.py`, add a new test case. This test should first create a user with a known username using the updated test utility. Then, call `crud.user.get_by_username` with that username and assert that the correct user object is returned. Additionally, test the negative case by calling the function with a username that does not exist and assert that the result is `None`.

**Test Strategy**: This unit test will cover both the success and failure paths of the `get_by_username` function.


#### 13.5 Write unit test for updating user credentials

Add a unit test to verify that the `update` method correctly modifies a user's `username` and `hashed_password`.

In `moneynote/tests/crud/test_user.py`, add a new test case for the update functionality. The test should: 1. Create a user. 2. Define a new username and a new password. 3. Call `crud.user.update` with the user object and a dictionary containing the new `username` and `password`. 4. Re-fetch the user from the database and assert that the `username` field has been updated. 5. Verify that the `hashed_password` has changed from its original value.

**Test Strategy**: This unit test will confirm that the `update` method correctly handles the specific fields required for account binding.


## 14. Implement `PUT /bind` Endpoint

Create the API endpoint that allows an authenticated user to bind a username and password to their account.

In `moneynote/routers/users.py`, add a new route `PUT /bind`. This endpoint will depend on `get_current_user`. It will use the `UserBind` schema for the body. The logic should: 1. Check if the current user already has a username. 2. Check if the new username is already taken using `crud_user.get_by_username`. 3. Validate the `inviteCode` against a hardcoded value for now. 4. Hash the password using the utility from `security.py`. 5. Update the user record using the CRUD function. Return 200 on success or 400 on validation failure.

**Test Strategy**: Integration tests will be written in a separate task. This task focuses on implementation.


### Subtasks

#### 14.1 Create `UserBind` Schema in `schemas/user.py`

Define a new Pydantic schema named `UserBind` to validate the request body for the `/bind` endpoint. This schema will enforce the structure of the incoming data.

In `moneynote/schemas/user.py`, add a new class `UserBind(BaseModel)` that includes the following fields: `username: str`, `password: str`, and `inviteCode: str`. This schema will be used to deserialize and validate the JSON body of the PUT request.

**Test Strategy**: No specific test needed for this subtask, as it will be validated by its usage in the endpoint implementation.


#### 14.2 Define the `PUT /bind` Endpoint in `routers/users.py`

Create the basic structure for the `PUT /bind` endpoint, including the route decorator, function signature, and necessary dependencies.

In `moneynote/routers/users.py`, add a new route using the `@router.put("/bind", response_model=schemas.User)` decorator. Define an `async` function `bind_user` that accepts `user_bind: schemas.UserBind` from the request body, `db: Session = Depends(get_db)`, and `current_user: models.User = Depends(get_current_user)`. Import `UserBind` from `moneynote.schemas`.

**Test Strategy**: The endpoint can be manually tested with an API client to ensure it's reachable and accepts the correct request body structure, even if the logic is not yet implemented.


#### 14.3 Implement Initial Validation Logic

Add validation to check if the user is already bound and if the provided invite code is correct.

Inside the `bind_user` function in `moneynote/routers/users.py`, add the following checks: 1. If `current_user.username` is not `None`, raise an `HTTPException` with status code 400 and a detail message like 'User is already bound.'. 2. Check if `user_bind.inviteCode` matches a hardcoded string (e.g., 'MONEYNOTE_INVITE'). If it doesn't match, raise an `HTTPException` with status code 400 and a detail message like 'Invalid invite code.'.

**Test Strategy**: Manually test by sending requests with an already-bound user token and with an incorrect invite code to verify that 400 errors are returned.


#### 14.4 Implement Username Uniqueness Check

Add logic to ensure the requested username is not already in use by another user.

In the `bind_user` function, after the initial validation, use the existing CRUD function `crud.user.get_by_username(db, username=user_bind.username)`. If this function returns a user object, it means the username is taken. In this case, raise an `HTTPException` with status code 400 and a detail message like 'Username already registered.'.

**Test Strategy**: Manually test by attempting to bind a username that is already known to exist in the database, expecting a 400 error.


#### 14.5 Hash Password, Update User Record, and Return Response

Finalize the endpoint by hashing the new password, updating the user model in the database, and returning the updated user object.

In the `bind_user` function, after all validations pass: 1. Import `hash_password` from `moneynote.security`. 2. Generate the hashed password by calling `hashed_password = hash_password(user_bind.password)`. 3. Create a dictionary or a `UserUpdate` schema object containing the update data: `{"username": user_bind.username, "hashed_password": hashed_password}`. 4. Call `crud.user.update(db, db_obj=current_user, obj_in=update_data)` to persist the changes. 5. Return the updated user object, which will be serialized by the `response_model`.

**Test Strategy**: Perform a successful request with a valid, unbound user, a valid invite code, and a unique username. Verify that the response is 200 OK and contains the updated user details (excluding the password), and that the user can subsequently log in with the new credentials (in a future task).


## 15. Create CRUD Operations for Group Model

Create the CRUD file and basic 'get' function for the Group model to support the initState endpoint.

Create a new file `moneynote/crud/crud_group.py`. Based on the existing pattern in `crud_book.py`, implement a `get(db: Session, id: int) -> models.Group | None` function that retrieves a group by its primary key.

**Test Strategy**: Write a simple unit test for the `get` function to ensure it can retrieve a group from the test database.


### Subtasks

#### 15.1 Create the Group SQLAlchemy Model

Create the `Group` model which is a prerequisite for creating CRUD operations. This model will represent the 'groups' table in the database.

Create a new file `moneynote/models/group.py`. Inside this file, define a `Group` class that inherits from `Base` (from `moneynote.db.base_class`). The model should include an `id` (primary key), a `name` (string), and a `user_id` (integer with a ForeignKey to `user.id`). Finally, import the new `Group` model in `moneynote/models/__init__.py` to make it accessible.

**Test Strategy**: This change will be tested implicitly by the tests for the CRUD operations that rely on this model.


#### 15.2 Create Pydantic Schemas for the Group Model

Create the necessary Pydantic schemas for the Group model, which are required by the `CRUDBase` generic class for validation and serialization.

Create a new file `moneynote/schemas/group.py`. Following the pattern in `moneynote/schemas/book.py`, define the following classes: `GroupBase` (with `name`), `GroupCreate` (inherits from `GroupBase`), `GroupUpdate` (inherits from `GroupBase`), and `Group` (inherits from `GroupInDBBase`, which you will also create, to represent the model returned from the API).

**Test Strategy**: These schemas will be validated by the unit tests for the CRUD operations.


#### 15.3 Implement the CRUDGroup Class in crud_group.py

Create the `crud_group.py` file and implement the `CRUDGroup` class that inherits from `CRUDBase`, providing the core database operations for the Group model.

Create the file `moneynote/crud/crud_group.py`. Import `CRUDBase`, the `Group` model, and the `GroupCreate` and `GroupUpdate` schemas. Define `class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate]):`. Add a `create_with_owner` method similar to the one in `CRUDBook` to associate a group with a user. Finally, create an instance `group = CRUDGroup(Group)`. The `get` method will be inherited from `CRUDBase`.

**Test Strategy**: The functionality of this class will be directly tested in the subsequent subtask.


#### 15.4 Integrate the Group CRUD Module

Make the new `group` CRUD object accessible throughout the application by importing it into the `crud` package's `__init__.py` file.

Modify the file `moneynote/crud/__init__.py`. Add the line `from .crud_group import group` to expose the `group` instance alongside the existing `user`, `book`, `category`, and `entry` objects. This follows the established pattern and allows for access via `crud.group`.

**Test Strategy**: This integration is verified by the ability of the unit tests to import and use `crud.group`.


#### 15.5 Create Unit Test for crud.group.get Function

Write a unit test to verify that the `get` function for the Group model correctly retrieves a group from the database by its ID.

Create a new test file `tests/crud/test_crud_group.py`. Add a test function `test_get_group(db: Session)`. Inside the test, first create a user and a group associated with that user using `crud.group.create_with_owner`. Then, call `crud.group.get(db=db, id=created_group.id)`. Use `assert` statements to verify that the returned object is not `None` and that its `id` and `name` match the group that was created.

**Test Strategy**: This subtask is the test strategy for the `get` function as requested in the main task.


## 16. Implement `GET /initState` Endpoint

Create the API endpoint that provides the client with the essential user, book, and group data upon application load.

In `moneynote/routers/users.py`, add a new route `GET /initState`. This endpoint will depend on `get_current_user`. The logic should: 1. Fetch the full user object. 2. Use `user.default_book_id` to fetch the default book using `crud_book.get`. 3. Use `user.default_group_id` to fetch the default group using `crud_group.get`. 4. Handle cases where `default_book_id` or `default_group_id` are null. 5. If an ID is present but the resource is not found, return a 404 error as specified in the PRD. 6. Assemble the data into the `InitStateResponse` schema and return it.

**Test Strategy**: Integration tests will be written in a separate task. This task focuses on implementation.


### Subtasks

#### 16.1 Define `InitStateResponse` Schema

Create the Pydantic schema for the `initState` endpoint's response. This schema will structure the data returned to the client.

In `moneynote/schemas/user.py`, define a new Pydantic model class named `InitStateResponse`. It should include three fields: `user` of type `schemas.User`, `book` of type `Optional[schemas.Book]`, and `group` of type `Optional[schemas.Group]`. You will need to import `schemas.Book` from `..schemas.book` and `schemas.Group` from `..schemas.group`.

**Test Strategy**: 


#### 16.2 Create `GET /initState` Endpoint Skeleton

Set up the basic structure for the new API endpoint in the user router file.

In `moneynote/routers/users.py`, add a new route using the `@router.get` decorator for the path `/initState`. Set the `response_model` to the newly created `schemas.user.InitStateResponse`. Define the endpoint function `get_initial_state` that takes `current_user: models.User = Depends(get_current_user)` and `db: Session = Depends(get_db)` as parameters. Ensure all necessary modules like `Depends`, `Session`, `schemas`, `models`, and `get_current_user` are imported.

**Test Strategy**: 


#### 16.3 Implement Default Book Fetching Logic

Add the logic to fetch the user's default book based on `default_book_id` and handle potential errors.

Inside the `get_initial_state` function in `moneynote/routers/users.py`, initialize a `default_book` variable to `None`. Check if `current_user.default_book_id` is not `None`. If it has a value, call `crud.crud_book.get(db=db, book_id=current_user.default_book_id)`. If the result is `None` (meaning the book was not found for the given ID), raise an `HTTPException` with a `status_code` of 404 and a detail message like 'Default book not found'. Otherwise, assign the fetched book object to the `default_book` variable. You will need to import `crud.crud_book`.

**Test Strategy**: 


#### 16.4 Implement Default Group Fetching Logic

Add the logic to fetch the user's default group based on `default_group_id` and handle potential errors.

Similar to the book logic, inside the `get_initial_state` function in `moneynote/routers/users.py`, initialize a `default_group` variable to `None`. Check if `current_user.default_group_id` is not `None`. If it has a value, call `crud.crud_group.get(db=db, group_id=current_user.default_group_id)`. If the result is `None`, raise an `HTTPException` with a `status_code` of 404 and a detail message like 'Default group not found'. Otherwise, assign the fetched group object to the `default_group` variable. You will need to import `crud.crud_group`.

**Test Strategy**: 


#### 16.5 Assemble and Return Final Response

Construct the final response object using the fetched data and return it from the endpoint.

At the end of the `get_initial_state` function in `moneynote/routers/users.py`, create an instance of the `schemas.user.InitStateResponse` model. Populate it with the `current_user`, the `default_book` (which will be the fetched book object or `None`), and the `default_group` (which will be the fetched group object or `None`). Return this `InitStateResponse` instance.

**Test Strategy**: 


## 17. Verify User Model and Generate Migration if Needed

Verify that the User model in the database schema supports account binding and create a migration if it doesn't.

Examine `moneynote/models/user.py`. Confirm that the `User` model's `username` column has `unique=True` and `nullable=True`, and that `hashed_password` is `nullable=True`. If these attributes are missing, add them and use Alembic to generate a new migration script to apply the changes to the database schema.

**Test Strategy**: Manual verification of the model file. If a migration is generated, it should be tested by running `alembic upgrade head` and `alembic downgrade` on a test database.


### Subtasks

#### 17.1 Analyze User Model for Required Schema Changes

Examine the `User` model in `moneynote/models/user.py` to confirm the current definitions of the `username` and `hashed_password` columns. Verify if `username` has `nullable=True` and if `hashed_password` has `nullable=True`.

Read the file `moneynote/models/user.py` and inspect the `User` class. Note the existing parameters for `Column('username', ...)` and `Column('hashed_password', ...)`. This analysis will confirm the exact changes needed in the subsequent tasks.

**Test Strategy**: Manual verification of the model file's contents.


#### 17.2 Update 'username' Column in User Model

Modify the `username` column definition in the `User` model within `moneynote/models/user.py` to add the `nullable=True` parameter. The existing `unique=True` parameter must be retained.

In `moneynote/models/user.py`, locate the line `username = Column(...)` within the `User` class. Update it to `username = Column(String, unique=True, index=True, nullable=True)`.

**Test Strategy**: Code review to ensure the parameter is added correctly without removing existing ones.


#### 17.3 Update 'hashed_password' Column in User Model

Modify the `hashed_password` column definition in the `User` model within `moneynote/models/user.py` to add the `nullable=True` parameter.

In `moneynote/models/user.py`, locate the line `hashed_password = Column(...)` within the `User` class. Update it to `hashed_password = Column(String, nullable=True)`.

**Test Strategy**: Code review to ensure the `nullable=True` parameter is correctly added.


#### 17.4 Generate Alembic Migration for User Model Changes

After updating the SQLAlchemy model, use Alembic to automatically generate a new migration script that reflects the changes to the `username` and `hashed_password` columns.

Run the following command from the project's root directory: `alembic revision --autogenerate -m "Allow null username and password for account binding"`. This will create a new file in the `migrations/versions/` directory.

**Test Strategy**: Confirm that a new migration script is created in the `migrations/versions` directory.


#### 17.5 Review and Finalize Generated Migration Script

Inspect the newly created migration file in `migrations/versions/`. Verify that it correctly uses `op.alter_column` to make the `username` and `hashed_password` columns nullable and that the `upgrade` and `downgrade` functions are correct.

Open the new migration script. The `upgrade` function should contain two `op.alter_column` calls, one for the 'users' table's 'username' column and one for 'hashed_password', both setting `nullable=True`. The `downgrade` function should reverse these changes by setting `nullable=False`.

**Test Strategy**: Test the migration on a test database by running `alembic upgrade head` to apply it and `alembic downgrade -1` to revert it, ensuring both operations complete successfully.


## 18. Write Integration Tests for `PUT /bind` Endpoint

Create comprehensive integration tests for the account binding endpoint to cover all specified scenarios.

In `tests/`, create or extend a test file for the users router. Using `TestClient`, write tests that cover: 1. (TC-P2-01) A successful binding for a guest user. 2. (TC-P2-02) An attempt to bind a username that is already taken. 3. (TC-P2-03) An attempt to bind with an invalid `inviteCode`. 4. An attempt by an unauthenticated user (expect 401/403). 5. An attempt by an already-bound user.

**Test Strategy**: These are the integration tests themselves. Use pytest fixtures to set up the necessary user and database state for each test case.


### Subtasks

#### 18.1 Create Test File and Guest User Fixture

Set up the necessary testing infrastructure. This involves creating the new test file `tests/api/v1/test_users.py` and adding a pytest fixture to generate an authenticated 'guest' user (a user with no username or password) and their corresponding JWT token headers.

Create a new file `tests/api/v1/test_users.py`. In `tests/conftest.py` or a suitable utility file, add a new fixture named `guest_user_token_headers`. This fixture should programmatically create a user in the database with `username` and `hashed_password` as NULL, then generate and return a valid access token header dictionary for this user. This will be the primary fixture for testing the bind endpoint.

**Test Strategy**: The fixture itself can be validated by ensuring it successfully creates a user in the test DB and returns a valid token header dictionary.


#### 18.2 Test Successful Binding for a Guest User (TC-P2-01)

Implement the integration test for the happy path, where a guest user successfully binds a username and password to their account.

In `tests/api/v1/test_users.py`, create a test function `test_bind_account_success`. Use the `client` and `guest_user_token_headers` fixtures. Make a `PUT` request to `/api/v1/users/bind` with a valid payload (new username, password, and correct invite code). Assert that the response status code is 200. Assert that the returned user object contains the new username. Optionally, query the database to confirm the `username` and `hashed_password` fields are correctly populated for that user.

**Test Strategy**: Assert status code, response body structure, and database state change.


#### 18.3 Test Binding with an Already-Taken Username (TC-P2-02)

Implement the integration test to ensure the system prevents a user from binding a username that is already in use by another user.

In `tests/api/v1/test_users.py`, create `test_bind_account_username_taken`. This test requires two users: one existing user with a defined username (the `normal_user_token_headers` fixture can be used to get this user's data), and a guest user. The test should use the `guest_user_token_headers` to make a `PUT` request to `/api/v1/users/bind`, attempting to use the username of the existing user. Assert that the API returns a 400 Bad Request status code and an appropriate error message.

**Test Strategy**: Set up conflicting data state using fixtures, then assert the expected 400-level error response.


#### 18.4 Test Binding by Unauthenticated and Already-Bound Users

Implement tests for two authorization/state scenarios: an unauthenticated user attempting to bind, and an already-bound user attempting to bind again.

In `tests/api/v1/test_users.py`, add two test functions. First, `test_bind_account_unauthenticated`: make a `PUT` request to `/api/v1/users/bind` without an `Authorization` header and assert a 401 Unauthorized status. Second, `test_bind_account_for_already_bound_user`: use the `normal_user_token_headers` fixture (which represents a standard, bound user) to make a `PUT` request to the bind endpoint. Assert that the API returns a 400 Bad Request or 403 Forbidden status code, as a user cannot be bound twice.

**Test Strategy**: For the unauthenticated test, make a request with no token. For the already-bound test, use a standard user fixture and assert the request is rejected.


#### 18.5 Test Binding with an Invalid Invite Code (TC-P2-03)

Implement the integration test to verify that the binding process fails when an incorrect `inviteCode` is provided.

In `tests/api/v1/test_users.py`, create a test function `test_bind_account_invalid_invite_code`. Use the `guest_user_token_headers` fixture. Make a `PUT` request to `/api/v1/users/bind` with a valid username and password, but an intentionally incorrect `inviteCode` string in the payload. Assert that the API returns a 400 Bad Request status code and a specific error message indicating the invite code is invalid.

**Test Strategy**: Use a valid guest user token but provide invalid data in the request body, then assert the expected 400-level error response.


## 19. Write Integration Tests for `GET /initState` Endpoint

Create comprehensive integration tests for the initial state hydration endpoint.

In the user router test file, add tests for `GET /initState`. The tests should cover: 1. (TC-P2-04) A successful request for a user with valid default book and group IDs. 2. (TC-P2-05) A request for a user where `default_book_id` and/or `default_group_id` are NULL. 3. (TC-P2-06) A request where `default_book_id` points to a book that does not exist (expect 404). 4. An unauthenticated request (expect 401/403).

**Test Strategy**: These are the integration tests themselves. Use pytest fixtures to create users with different default ID configurations (valid, null, invalid).


### Subtasks

#### 19.1 Create Pytest Fixtures for initState Test Scenarios

In `tests/routers/test_users.py`, create the necessary pytest fixtures to represent the different user states required for testing the `GET /initState` endpoint. These fixtures will provide the data setup for subsequent tests.

Based on the existing patterns in `tests/conftest.py` and `tests/routers/test_users.py`, create the following fixtures:
1. A fixture that creates a user, a book, and a group, and then updates the user's `default_book_id` and `default_group_id` to point to the created book and group.
2. A fixture for a user where `default_book_id` and `default_group_id` are `NULL`.
3. A fixture for a user where `default_book_id` is set to a non-existent ID (e.g., 99999).
4. Corresponding authentication header fixtures for each of these user fixtures.

**Test Strategy**: These are fixtures, not tests. Correctness will be verified by the tests in the subsequent subtasks that use them.


#### 19.2 Implement Test for Successful initState with Valid Defaults (TC-P2-04)

In `tests/routers/test_users.py`, write an integration test for a successful `GET /initState` request where the user has valid `default_book_id` and `default_group_id`.

Using the `TestClient` and the fixture for the user with valid defaults, make an authenticated GET request to `/users/initState`. Assert that the HTTP status code is 200. Validate that the JSON response body contains the correct user data, and that the `defaultBook` and `defaultGroup` keys contain the full objects for the associated book and group.

**Test Strategy**: This test covers the primary success path for the endpoint.


#### 19.3 Implement Test for initState with Null Default IDs (TC-P2-05)

In `tests/routers/test_users.py`, add a test case for a user whose `default_book_id` and `default_group_id` are `NULL`.

Using the `TestClient` and the fixture for the user with `NULL` defaults, make an authenticated GET request to `/users/initState`. Assert that the HTTP status code is 200. Verify that the `defaultBook` and `defaultGroup` keys in the JSON response are `null`.

**Test Strategy**: This test covers the valid scenario where a user has not yet set up or been assigned default entities.


#### 19.4 Implement Test for initState with an Invalid Default Book ID (TC-P2-06)

In `tests/routers/test_users.py`, write a test to ensure the endpoint returns a 404 error when a user's `default_book_id` refers to a book that does not exist.

Using the `TestClient` and the fixture for the user with an invalid `default_book_id`, make an authenticated GET request to `/users/initState`. Assert that the HTTP status code is 404, as specified in the endpoint's requirements.

**Test Strategy**: This test covers the specific error handling case for a dangling reference in the user's default settings.


#### 19.5 Implement Test for Unauthenticated initState Request

In `tests/routers/test_users.py`, add a test to verify that unauthenticated requests to `GET /initState` are rejected.

Using the `TestClient`, make a GET request to `/users/initState` without including an `Authorization` header. Assert that the HTTP status code is 401 Unauthorized, which is the expected behavior for protected endpoints in the application.

**Test Strategy**: This test ensures the endpoint is properly protected by the `get_current_user` dependency.


## 20. Update Main Router and API Documentation

Include the updated user router in the main application and ensure the API documentation is accurate.

Verify that the `users.router` is correctly included in `main.py`. Run the application locally and access the auto-generated OpenAPI documentation at `/docs`. Review the documentation for `/bind` and `/initState` to ensure the models, parameters, and responses are correctly represented.

**Test Strategy**: Manual review of the running application's Swagger/OpenAPI documentation.


### Subtasks

#### 20.1 Analyze Router Inclusion in main.py

Examine the main application file to understand how FastAPI routers are currently being included and determine if the user router is already present.

Use the Read tool to inspect `app/main.py`. Look for `app.include_router()` calls. Use the Grep tool to search for `users.router` within `app/main.py` to confirm whether it's already included. Note the pattern used for including other routers, such as prefixes and tags.

**Test Strategy**: Verify by reading `app/main.py` and confirming the presence or absence of the user router inclusion.


#### 20.2 Include User Router in Main Application

Modify `app/main.py` to import and include the user router, ensuring it follows the existing patterns for router configuration.

In `app/main.py`, add the import statement for the user router: `from app.api.v1.endpoints import users`. Then, add the line `api_router.include_router(users.router, prefix="/users", tags=["users"])` within the file, consistent with how other routers are included in `api_router`.

**Test Strategy**: After modification, run the application and check for any startup errors. The application should run successfully.


#### 20.3 Locate and Analyze /bind and /initState Endpoints

Find the endpoint definitions for `/bind` and `/initState` within the user router file and analyze their current implementation, including request models and response models.

Use the Read tool to examine `app/api/v1/endpoints/users.py`. Locate the functions decorated with `@router.post("/bind")` and `@router.post("/initState")`. Identify the Pydantic models used for the request body and the `response_model` specified in the decorator.

**Test Strategy**: Confirm the existence of the two endpoints and their associated Pydantic models by reading the `app/api/v1/endpoints/users.py` file.


#### 20.4 Enhance Pydantic Models for Clearer Documentation

Update the Pydantic models associated with the `/bind` and `/initState` endpoints to include descriptive details that will improve the auto-generated OpenAPI documentation.

In `app/schemas/user.py` (or wherever the relevant models are defined), import `Field` from `pydantic`. For the models used in `/bind` and `/initState`, add `description` and `example` attributes to each field using `Field(...)`. For example: `email: str = Field(..., description="The user's email address.", example="user@example.com")`. This will make the documentation in `/docs` more informative.

**Test Strategy**: Review the code changes in the schema files to ensure `Field` is used correctly to add descriptions and examples to the model properties.


#### 20.5 Run App and Validate OpenAPI Docs for User Endpoints

Run the FastAPI application locally, access the `/docs` endpoint, and verify that the user router and its `/bind` and `/initState` endpoints are correctly documented.

Execute the application using the standard run command. Open a web browser to `http://127.0.0.1:8000/docs`. Expand the 'users' tag. Verify that the `/users/bind` and `/users/initState` endpoints are listed. Click on them to check that the request body schema, parameters, and response models are accurately represented with the descriptions and examples added in the previous step.

**Test Strategy**: Manual review of the Swagger UI at `/docs` to confirm the presence and accuracy of the user endpoints' documentation.


