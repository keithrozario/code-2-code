## 1. Define Pydantic Schemas and Create Static Data Files

Create the Pydantic models for Currency and BookTemplate and the corresponding static JSON data files that will be loaded by the application.

In `moneynote/schemas/`, create new files or update existing ones to define `Currency` and `BookTemplate` Pydantic schemas matching the PRD. In `moneynote/data/`, create `currency.json` and `book_tpl.json` with sample data as specified in the data model section of the PRD.

**Test Strategy**: Manual verification of file contents and schema definitions. The schemas will be implicitly tested by the data loader service tests.


### Subtasks

#### 1.1 Define the Currency Pydantic Schema

Create a new file for the Currency schema and define the model structure, ensuring it inherits from the existing base model.

In the `moneynote/schemas/` directory, create a new file named `currency.py`. Inside this file, import the `Base` model from `moneynote.schemas.base`. Define a new Pydantic class `Currency` that inherits from `Base`. Based on standard currency attributes, add the following fields: `code: str`, `name: str`, and `symbol: str`.

**Test Strategy**: Manual verification of the file `moneynote/schemas/currency.py` to ensure it contains the `Currency` class inheriting from `Base` with the correct fields.


#### 1.2 Define the BookTemplate Pydantic Schema

Create a new file for the BookTemplate schema and define its model structure, following the project's conventions.

In the `moneynote/schemas/` directory, create a new file named `book_template.py`. Import the `Base` model from `moneynote.schemas.base`. Define a new Pydantic class `BookTemplate` that inherits from `Base`. Add the following fields to the model: `id: str`, `name: str`, and `description: str`.

**Test Strategy**: Manual verification of the file `moneynote/schemas/book_template.py` to ensure it contains the `BookTemplate` class inheriting from `Base` with the correct fields.


#### 1.3 Expose New Schemas in the Schemas Module

Update the `__init__.py` file in the schemas directory to make the new Currency and BookTemplate models easily importable from the `moneynote.schemas` package.

Modify the file `moneynote/schemas/__init__.py`. Add import statements to expose the newly created `Currency` and `BookTemplate` schemas. The file should be updated to include `from .currency import Currency` and `from .book_template import BookTemplate`.

**Test Strategy**: Manual verification of `moneynote/schemas/__init__.py` to confirm the new import lines are present.


#### 1.4 Create Static Currency Data File

Create the directory and JSON file containing the list of supported currencies.

Create a new directory `moneynote/data/`. Inside this directory, create a new file named `currency.json`. Populate this file with a JSON array of currency objects that conform to the `Currency` schema. Include at least three sample currencies, for example: USD, EUR, and JPY.

**Test Strategy**: Manual verification of the file `moneynote/data/currency.json` to ensure it exists, is valid JSON, and its objects match the `Currency` schema.


#### 1.5 Create Static Book Template Data File

Create the JSON file containing the list of available book templates.

In the `moneynote/data/` directory, create a new file named `book_tpl.json`. Populate this file with a JSON array of book template objects that conform to the `BookTemplate` schema. Include at least two sample templates, such as a 'Personal' template and a 'Business' template.

**Test Strategy**: Manual verification of the file `moneynote/data/book_tpl.json` to ensure it exists, is valid JSON, and its objects match the `BookTemplate` schema.


## 2. Add Version and Base URL to Application Configuration

Update the application's configuration to include the application version and a base URL for testing purposes.

Modify the Pydantic Settings class in `moneynote/core/config.py`. Add two new fields: `APP_VERSION` and `BASE_URL`. These should be loaded from environment variables. Provide default values for local development.

**Test Strategy**: Unit test that the settings object correctly loads these values from environment variables and uses defaults when they are not set.


### Subtasks

#### 2.1 Add APP_VERSION Field to Settings Class

Modify the `Settings` class in `moneynote/core/config.py` to include the new `APP_VERSION` field.

In the `Settings` class within `moneynote/core/config.py`, add a new attribute `APP_VERSION: str = "0.1.0"`. This will allow the application version to be loaded from an environment variable, with a sensible default for local development.

**Test Strategy**: This will be tested in a subsequent subtask by verifying that the settings object contains this field with the correct default value.


#### 2.2 Add BASE_URL Field to Settings Class

Modify the `Settings` class in `moneynote/core/config.py` to include the new `BASE_URL` field for testing purposes.

In the `Settings` class within `moneynote/core/config.py`, add a new attribute `BASE_URL: str = "http://localhost:8000"`. This will define a base URL for the application, loaded from an environment variable, with a default pointing to the local development server.

**Test Strategy**: This will be tested in a subsequent subtask by verifying that the settings object contains this field with the correct default value.


#### 2.3 Create Unit Test for Default Configuration Values

Add a new test case to `tests/core/test_config.py` to verify that `APP_VERSION` and `BASE_URL` are assigned their default values when the corresponding environment variables are not set.

In `tests/core/test_config.py`, create a new test function. Use `unittest.mock.patch.dict` to ensure the environment variables `APP_VERSION` and `BASE_URL` are not present. Reload the `config` module using `importlib.reload` and assert that `settings.APP_VERSION` is "0.1.0" and `settings.BASE_URL` is "http://localhost:8000".

**Test Strategy**: This unit test will directly confirm that the default values are correctly implemented as per the task requirements.


#### 2.4 Create Unit Test for Environment Variable Loading

Add a new test case to `tests/core/test_config.py` to confirm that `APP_VERSION` and `BASE_URL` are correctly loaded from environment variables when they are set.

Following the existing pattern in `tests/core/test_config.py`, create a test function that uses `unittest.mock.patch.dict` to set `APP_VERSION` to "test-v9.9.9" and `BASE_URL` to "http://test.example.com". Reload the `config` module and assert that the `settings` object's attributes match these custom values.

**Test Strategy**: This unit test will verify that the Pydantic settings class correctly overrides default values with those from the environment.


#### 2.5 Document New Environment Variables in .env.example

Update the project's example environment file to include the new configuration variables for other developers.

Locate the `.env.example` file in the project root. Add new lines for the `APP_VERSION` and `BASE_URL` variables, documenting their purpose and default values. For example: `APP_VERSION=0.1.0` and `BASE_URL=http://localhost:8000`. If the file does not exist, create it.

**Test Strategy**: This is a documentation task. Correctness can be verified by code review, ensuring the new variables are present in the `.env.example` file.


## 3. Create Data Loader Service for Caching Static JSON

Implement a service to read and cache the contents of `currency.json` and `book_tpl.json` into memory upon application startup.

Create a new file `moneynote/services/data_loader_service.py`. This service should contain functions to read `currency.json` and `book_tpl.json`, parse them, and validate their contents against the Pydantic schemas. It should cache the resulting lists of objects. Implement robust error handling to log a critical error and prevent application startup if files are missing or malformed, as per the PRD's risk mitigation.

**Test Strategy**: Write unit tests for the data loader service. Use mock file systems to test for successful loading, file-not-found errors, and JSON parsing/validation errors. Verify that appropriate exceptions are raised.


### Subtasks

#### 3.1 Update Configuration with Data File Paths

Add the file paths for `currency.json` and `book_tpl.json` to the `Settings` class in `moneynote/config.py` to make them configurable and centrally managed.

Modify the `Settings` class in `moneynote/config.py`. Add two new attributes: `CURRENCY_DATA_PATH` with a default value of `"moneynote/static/currency.json"` and `BOOK_TPL_DATA_PATH` with a default value of `"moneynote/static/book_tpl.json"`. This will allow the service to access these paths via the application settings.

**Test Strategy**: Verify that the settings object, when instantiated, contains the correct default paths for the two JSON files.


#### 3.2 Create DataLoaderService Class and Custom Exceptions

Create the new file `moneynote/services/data_loader_service.py` and define the `DataLoaderService` class structure, along with a custom exception for loading errors.

Create the file `moneynote/services/data_loader_service.py`. In this file, define a custom exception class `class DataFileError(Exception): pass`. Then, define the `DataLoaderService` class. In its `__init__` method, initialize `self.currencies: list[Currency] = []` and `self.book_templates: list[BookTemplate] = []`. Import `Currency` and `BookTemplate` from `moneynote.schemas`.

**Test Strategy**: Unit test to ensure the `DataLoaderService` can be instantiated and its `currencies` and `book_templates` attributes are empty lists by default.


#### 3.3 Implement a Generic JSON File Validation Method

Add a private helper method to `DataLoaderService` to load, parse, and validate a list of objects from a JSON file against a given Pydantic model.

Implement a private method `_load_and_validate_json(self, file_path: str, model: Type[BaseModel]) -> list[BaseModel]`. This method should open and read the file at `file_path`, parse its JSON content, and then use `pydantic.parse_obj_as(list[model], ...)` to validate the data. It must wrap `FileNotFoundError`, `json.JSONDecodeError`, and `pydantic.ValidationError` and raise the custom `DataFileError` with a descriptive message.

**Test Strategy**: Unit test this private method using mocks for the file system. Test the success case, a file not found case, a JSON decoding error case, and a Pydantic validation error case, ensuring `DataFileError` is raised appropriately.


#### 3.4 Implement Specific Data Loading and Caching Methods

Create public methods in `DataLoaderService` to load currencies and book templates using the generic loader and cache the results in instance attributes.

In `DataLoaderService`, implement two methods: `load_currencies(self, settings: Settings)` and `load_book_templates(self, settings: Settings)`. Each method will call `_load_and_validate_json`, passing the appropriate file path from the `settings` object (`settings.CURRENCY_DATA_PATH` or `settings.BOOK_TPL_DATA_PATH`) and the corresponding Pydantic schema (`Currency` or `BookTemplate`). The validated list of objects should be assigned to `self.currencies` and `self.book_templates` respectively.

**Test Strategy**: Unit test these methods, mocking the `_load_and_validate_json` method to ensure it's called with the correct parameters and that the instance attributes are correctly updated with the mock return value.


#### 3.5 Implement Main Loader Entrypoint with Error Handling and Logging

Create a single public method `load_all_data()` that orchestrates the loading process and implements the final error handling and logging strategy.

In `DataLoaderService`, create a public method `load_all_data(self, settings: Settings)`. This method will call `self.load_currencies(settings)` and `self.load_book_templates(settings)`. Wrap these calls in a `try...except DataFileError as e:` block. In the `except` block, use Python's `logging` module to log a critical error (e.g., `logging.critical("Failed to load static data: %s", e)`) and then re-raise the exception to halt application startup as required by the PRD.

**Test Strategy**: Unit test `load_all_data`. Verify that both `load_currencies` and `load_book_templates` are called. Mock one of the sub-methods to raise a `DataFileError` and assert that a critical error is logged and the exception is re-raised.


## 4. Integrate Data Loader into Application Startup

Hook the new data loader service into the FastAPI application's startup lifecycle event.

In `main.py`, use the `@app.on_event('startup')` decorator to call the data loader service. The loaded data (currencies and book templates) should be stored in a globally accessible way, for instance, on the `app.state` object, to be available for endpoint logic.

**Test Strategy**: Integration testing will verify this. When the test client starts the app, the data should be loaded. Subsequent endpoint tests will confirm if the data is accessible.


### Subtasks

#### 4.1 Import Data Loader Service and Logging in main.py

Modify `moneynote/main.py` to import the necessary modules for data loading and logging. This includes the `data_loader_service` from `moneynote.services` and Python's built-in `logging` module.

In `moneynote/main.py`, add the following import statements at the top of the file: `from moneynote.services import data_loader_service` and `import logging`. This prepares the file for the subsequent steps.

**Test Strategy**: Code review to ensure imports are correct and follow project conventions.


#### 4.2 Define the Startup Event Handler Function

In `moneynote/main.py`, create the asynchronous function that will be executed on application startup and decorate it correctly.

Below the `app = FastAPI(...)` instantiation in `moneynote/main.py`, add a new async function decorated with `@app.on_event('startup')`. The function should be named `load_static_data` and should initially be empty. Example: `@app.on_event('startup')
async def load_static_data():
    pass`

**Test Strategy**: Run the application to ensure it starts without errors after adding the empty event handler.


#### 4.3 Load Currencies and Store on app.state

Implement the logic within the startup event handler to call the data loader service for currencies and store the result on the application state.

Inside the `load_static_data` function in `moneynote/main.py`, call `data_loader_service.load_currencies()`. Assign the returned data to `app.state.currencies`. Add a log info message indicating that currencies have been loaded successfully.

**Test Strategy**: Temporarily add a print statement or use a debugger to verify that `app.state.currencies` is populated after startup.


#### 4.4 Load Book Templates and Store on app.state

Implement the logic within the startup event handler to call the data loader service for book templates and store the result on the application state.

Inside the `load_static_data` function in `moneynote/main.py`, call `data_loader_service.load_book_templates()`. Assign the returned data to `app.state.book_templates`. Add a log info message indicating that book templates have been loaded successfully.

**Test Strategy**: Temporarily add a print statement or use a debugger to verify that `app.state.book_templates` is populated after startup.


#### 4.5 Implement Critical Error Handling for Data Loading

Wrap the data loading calls in the startup event with a try/except block to handle potential errors, log them as critical, and prevent the application from starting if loading fails.

In the `load_static_data` function, wrap the calls to `load_currencies()` and `load_book_templates()` in a `try...except Exception as e` block. In the `except` block, use `logging.critical` to log a message like 'Failed to load static data on startup. Application will not start. Error: {e}'. Then, re-raise the exception to ensure the FastAPI application startup is halted.

**Test Strategy**: Manually test by temporarily renaming or corrupting `currency.json` or `book_tpl.json` and verifying that the application fails to start and logs a critical error.


## 5. Implement `GET /version` Endpoint

Create the API endpoint to return the application's current version from the configuration.

In `moneynote/routers/`, create a new router (e.g., `system.py`) or use an existing one. Add a `GET /version` endpoint that depends on the authentication mechanism from `deps.py`. The endpoint logic should access the settings object and return the `APP_VERSION` in the specified JSON format.

**Test Strategy**: Integration test to verify the endpoint returns a 200 status and the correct version string with a valid token. Test for a 401/403 response when no token is provided.


### Subtasks

#### 5.1 Create New Router File for System Endpoints

Create a new file at `moneynote/routers/system.py` to house system-level API endpoints, starting with the version endpoint.

Following the project's structure seen in `moneynote/routers/users.py` and `auth.py`, create the file `moneynote/routers/system.py`. This file will contain the router for system-related endpoints.

**Test Strategy**: N/A


#### 5.2 Define Pydantic Schema for Version Response

Create a Pydantic model to define the structure of the JSON response for the `/version` endpoint, ensuring a consistent API contract.

Create a new file `moneynote/schemas/system.py`. Inside this file, define a Pydantic `BaseModel` named `VersionResponse` with a single string field: `version: str`. This will model the expected output: `{"version": "..."}`.

**Test Strategy**: N/A


#### 5.3 Implement the GET /version Endpoint Logic

In `moneynote/routers/system.py`, implement the `GET /version` endpoint that retrieves and returns the application version from the configuration settings.

In `moneynote/routers/system.py`, import `APIRouter`, `Depends` from `fastapi`, `get_settings` and `get_current_active_user` from `moneynote.deps`, `Settings` from `moneynote.config`, and `VersionResponse` from `moneynote.schemas.system`. Create an `APIRouter` instance. Define an async function for the `GET /version` path with `response_model=VersionResponse`. The endpoint must be protected by `Depends(get_current_active_user)`. Inject the settings via `settings: Settings = Depends(get_settings)` and return `VersionResponse(version=settings.APP_VERSION)`.

**Test Strategy**: This logic will be tested via integration tests in a subsequent subtask.


#### 5.4 Integrate System Router into FastAPI Application

Modify `moneynote/main.py` to include the newly created system router, making the `/version` endpoint accessible through the main application.

Open `moneynote/main.py`. Import the `router` object from `moneynote.routers.system`. Register it with the main FastAPI app instance using `app.include_router(system.router, prefix="/api/v1", tags=["system"])`, following the pattern used for other routers like `users` and `auth`.

**Test Strategy**: Manual verification by running the application and checking the OpenAPI docs at `/docs` for the new `/api/v1/version` endpoint.


#### 5.5 Add Integration Tests for GET /version Endpoint

Create integration tests to verify the functionality and security of the new `/version` endpoint, ensuring it returns the correct data and is properly authenticated.

Create a new test file, `moneynote/tests/api/v1/test_system.py`. Add a test case that makes an authenticated request to `GET /api/v1/version` and asserts a 200 OK status and that the response body contains the correct `APP_VERSION`. Add a second test case that makes a request without an authentication token and asserts a 401 Unauthorized status code.

**Test Strategy**: Use the existing test client fixture and utilities for creating authenticated headers to write the tests.


## 6. Implement `GET /test3` Endpoint

Create the API endpoint to return the application's base URL for testing and configuration.

In the same router as the version endpoint, add a `GET /test3` endpoint protected by authentication. The logic should access the settings object and return the `BASE_URL` in the specified JSON format (`{"base_url": "..."}`).

**Test Strategy**: Integration test to verify the endpoint returns a 200 status and the correct URL with a valid token. Test for a 401/403 response when no token is provided.


### Subtasks

#### 6.1 Add BASE_URL to Configuration

Add the `BASE_URL` field to the application's settings model to make it accessible throughout the application.

In `moneynote/config.py`, modify the `Settings` class to include a new field `BASE_URL: str`. Assign a default value, for example, `"http://localhost:8000"`. This ensures the setting is available for the new endpoint to consume.

**Test Strategy**: This change will be implicitly tested by the integration test in a later subtask, which will rely on this setting being present.


#### 6.2 Define the BaseUrlResponse Schema

Create a Pydantic schema for the JSON response of the `/test3` endpoint to ensure a consistent and validated output format.

In `moneynote/schemas/system.py`, add a new Pydantic model class named `BaseUrlResponse`. This class should inherit from `BaseModel` and contain a single field: `base_url: str`.

**Test Strategy**: The FastAPI framework will use this schema for response validation and OpenAPI documentation generation. Correct implementation will be verified by the endpoint's integration test.


#### 6.3 Create the GET /test3 Endpoint Route

Add the route definition for the `GET /test3` endpoint in the system router, including authentication and response model specifications.

In `moneynote/routers/system.py`, add a new endpoint using the `@router.get()` decorator for the path `/test3`. Configure it with `response_model=schemas.BaseUrlResponse`, `dependencies=[Depends(deps.get_current_user)]`, and `tags=["System"]` to match the conventions used by the existing `/version` endpoint.

**Test Strategy**: This subtask sets up the route structure. The logic will be implemented in the next step.


#### 6.4 Implement the Endpoint Logic

Write the function body for the `/test3` endpoint to retrieve the `BASE_URL` from settings and return it.

In `moneynote/routers/system.py`, implement the function for the `/test3` route (e.g., `get_base_url`). The function should access the imported `settings` object from `moneynote.config` and return an instance of the `schemas.BaseUrlResponse` model, populated with the value of `settings.BASE_URL`.

**Test Strategy**: The logic will be directly tested by the integration test, which will assert the content of the response body.


#### 6.5 Write Integration Tests for the /test3 Endpoint

Add integration tests to verify the functionality and security of the new `/test3` endpoint.

In `tests/integration/test_system.py`, add two test functions following the existing patterns: 1. `test_get_base_url_authenticated`: Uses the `authorized_user_headers` fixture to make an authenticated request to `/api/v1/system/test3`. Assert that the status code is 200 and the response body is `{"base_url": settings.BASE_URL}`. 2. `test_get_base_url_unauthenticated`: Makes a request without authentication and asserts that the status code is 401.

**Test Strategy**: These tests will confirm that the endpoint works as expected for both authenticated and unauthenticated scenarios, validating the implementation from the previous subtasks.


## 7. Implement `GET /currencies/all` Endpoint

Create the API endpoint to return the list of all supported currencies.

Create a new router file `moneynote/routers/currencies.py`. Add a `GET /currencies/all` endpoint protected by authentication. The endpoint should retrieve the cached currency list from `app.state` (or the chosen global access method) and return it as a JSON array.

**Test Strategy**: Integration test to verify the endpoint returns a 200 status and a JSON array matching the contents of `currency.json` when a valid token is used. Test for a 401/403 response without a token.


### Subtasks

#### 7.1 Create `moneynote/routers/currencies.py` and Initialize Router

Create a new Python file at `moneynote/routers/currencies.py`. Inside this file, import `APIRouter` from `fastapi` and instantiate a router object. This file will contain the currency-related endpoints.

The file should contain the basic boilerplate for a FastAPI router: `from fastapi import APIRouter; router = APIRouter()`.

**Test Strategy**: File existence and basic syntax check.


#### 7.2 Define Pydantic Schema for Currency Data

To ensure type safety and proper API documentation, define a Pydantic model for the currency data. Based on the project structure, this should be in a new file `moneynote/schemas/currency.py`.

Create `moneynote/schemas/currency.py` and define a `Currency` model inheriting from `pydantic.BaseModel`. The model should have fields like `code: str`, `name: str`, and `symbol: str` to match the structure of the data loaded from `currency.json`.

**Test Strategy**: Unit test the Pydantic model to ensure it validates correct data and rejects incorrect data.


#### 7.3 Define `GET /all` Endpoint with Authentication

In `moneynote/routers/currencies.py`, define an async function for the `GET /all` route. This function should be decorated with `@router.get("/all")`. Import and apply the authentication dependency from `moneynote.dependencies` to protect the endpoint.

Import `Depends` from `fastapi`, `User` from `moneynote.models.user`, and `get_current_active_user` from `moneynote.dependencies`. The endpoint signature should be `async def get_all_currencies(current_user: User = Depends(get_current_active_user))`. The function body can be a placeholder (`pass`) for now.

**Test Strategy**: An integration test can be prepared to check for a 401/403 response when calling this endpoint without a valid token.


#### 7.4 Implement Endpoint Logic to Return Currencies from `app.state`

Implement the body of the `get_all_currencies` function. It needs to access the cached currency list from the application state and return it. The endpoint's response model should also be set.

Import `Request` from `fastapi`, `List` from `typing`, and the `Currency` schema from `moneynote.schemas.currency`. Add `request: Request` to the function signature. The function body should be `return request.app.state.currencies`. Update the decorator to `@router.get("/all", response_model=List[Currency])`.

**Test Strategy**: Integration test to verify the endpoint returns a 200 status and a JSON array of currencies when a valid token is provided.


#### 7.5 Register the Currencies Router in `main.py`

Integrate the new `currencies` router into the main FastAPI application in `moneynote/main.py`. This will make the `/currencies/all` endpoint accessible through the API.

In `moneynote/main.py`, add `from moneynote.routers import currencies` to the import section. Then, add the line `app.include_router(currencies.router, prefix="/currencies", tags=["currencies"])` to register the router with the main `app` instance.

**Test Strategy**: After this change, the full integration test for the endpoint should pass, confirming it's correctly wired into the application.


## 8. Implement `GET /book-templates/all` Endpoint

Create the API endpoint to return the list of all available book templates.

Create a new router file `moneynote/routers/book_templates.py`. Add a `GET /book-templates/all` endpoint protected by authentication. The endpoint should retrieve the cached book template list from `app.state` and return it as a JSON array.

**Test Strategy**: Integration test to verify the endpoint returns a 200 status and a JSON array matching the contents of `book_tpl.json` when a valid token is used. Test for a 401/403 response without a token.


### Subtasks

#### 8.1 Create `book_templates.py` and Initialize APIRouter

Create a new file at `moneynote/routers/book_templates.py`. In this file, import `APIRouter` from `fastapi` and create a router instance with the prefix `/book-templates` and the tag `Book Templates`.

Following the pattern in other router files like `currencies.py`, the new file should contain:
```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/book-templates",
    tags=["Book Templates"],
)
```

**Test Strategy**: Code review to ensure file creation and correct router initialization.


#### 8.2 Define the Endpoint Path and Function Signature

In `moneynote/routers/book_templates.py`, define an asynchronous function `get_all_book_templates` decorated with `@router.get("/all")`. The function should accept `request: Request` as an argument to access the application state.

Import `Request` from `fastapi`. The function signature should be `async def get_all_book_templates(request: Request):`. The response model can be set to `list` for now.

**Test Strategy**: Static analysis to check for the correct decorator, path, and function signature.


#### 8.3 Add Authentication Dependency to the Endpoint

Secure the `GET /all` endpoint by adding the authentication dependency. Import the `get_current_user` dependency from `moneynote.auth.deps` and add it to the `dependencies` list of the `@router.get` decorator.

The decorator should be updated to `@router.get("/all", dependencies=[Depends(deps.get_current_user)])`. You will need to import `Depends` from `fastapi` and `deps` from `moneynote.auth`.

**Test Strategy**: An integration test will later confirm that accessing this endpoint without a token results in a 401/403 error.


#### 8.4 Implement Endpoint Logic to Return Book Templates

Inside the `get_all_book_templates` function, implement the logic to retrieve the list of book templates from the application state and return it. The data is expected to be available at `request.app.state.book_templates`.

The implementation should be a single line: `return request.app.state.book_templates`. This relies on Task 4, which loads this data into the app state on startup. FastAPI will handle the JSON serialization.

**Test Strategy**: An integration test will verify that the endpoint returns a JSON array matching the contents of `book_tpl.json` when properly authenticated.


#### 8.5 Register the Book Templates Router in `main.py`

Integrate the newly created router into the main FastAPI application by importing it in `moneynote/main.py` and using `app.include_router()`.

In `moneynote/main.py`, add `from moneynote.routers import book_templates` with the other router imports. Then, add the line `app.include_router(book_templates.router)` to register it with the application.

**Test Strategy**: After this change, the `/docs` page should show the new `/book-templates/all` endpoint. Running the application and hitting the endpoint will confirm it's correctly registered.


## 9. Include New Routers in Main Application

Ensure the main FastAPI application is aware of the new routers for system, currencies, and book templates.

In `main.py`, import and include the newly created routers (`system_router`, `currencies_router`, `book_templates_router`) using `app.include_router()`. Ensure they are prefixed correctly under `/api/v1` if applicable.

**Test Strategy**: This is verified by the successful execution of the integration tests for the new endpoints. If the routers are not included, the tests will fail with 404 Not Found errors.


### Subtasks

#### 9.1 Import All New Routers in `main.py`

Modify `moneynote/main.py` to import the `system_router`, `currencies_router`, and `book_templates_router` from their respective modules.

Based on the existing pattern in `moneynote/main.py`, add the following import statements alongside the other router imports:
```python
from moneynote.routers.system import router as system_router
from moneynote.routers.currencies import router as currencies_router
from moneynote.routers.book_templates import router as book_templates_router
```

**Test Strategy**: 


#### 9.2 Include the System Router in the FastAPI App

In `moneynote/main.py`, register the `system_router` with the main FastAPI application instance, ensuring it is prefixed correctly.

Following the pattern for `users_router`, add the following line to the router inclusion section of `moneynote/main.py`:
`app.include_router(system_router, prefix="/api/v1", tags=["System"])`

**Test Strategy**: 


#### 9.3 Include the Currencies Router in the FastAPI App

In `moneynote/main.py`, register the `currencies_router` with the main FastAPI application instance, ensuring it is prefixed correctly.

Following the pattern for `users_router`, add the following line to the router inclusion section of `moneynote/main.py`:
`app.include_router(currencies_router, prefix="/api/v1", tags=["Currencies"])`

**Test Strategy**: 


#### 9.4 Include the Book Templates Router in the FastAPI App

In `moneynote/main.py`, register the `book_templates_router` with the main FastAPI application instance, ensuring it is prefixed correctly.

Following the pattern for `users_router`, add the following line to the router inclusion section of `moneynote/main.py`:
`app.include_router(book_templates_router, prefix="/api/v1", tags=["Book Templates"])`

**Test Strategy**: 


#### 9.5 Review and Organize Router Configuration

Review the `moneynote/main.py` file to ensure all router imports and `app.include_router` calls are clean, consistently formatted, and logically ordered.

Verify that all new routers are grouped with the other `/api/v1` routers. Ensure imports are sorted according to PEP 8. This final check improves code readability and maintainability.

**Test Strategy**: 


## 10. Write Integration Tests for All Phase 1 Endpoints

Create a comprehensive suite of integration tests for all four new endpoints to verify functionality and security.

In the `tests/` directory, create test files corresponding to the new routers. Using FastAPI's `TestClient`, write tests for each endpoint (`/version`, `/test3`, `/currencies/all`, `/book-templates/all`). Cover both the happy path (200 OK with correct data) and the unauthorized path (401/403 without a valid token), as outlined in the PRD's test cases.

**Test Strategy**: Run the pytest suite and ensure all new tests pass. This task validates the completion of all other implementation tasks.


### Subtasks

#### 10.1 Create Test Files and Structure for New Routers

Create the necessary test files within the `tests/` directory to house the new integration tests. This involves creating a `routers` subdirectory and the specific test files for the system and data endpoints.

Based on the project structure with `moneynote/routers/system.py` and `moneynote/routers/data.py`, create corresponding test files: `tests/routers/test_system.py` and `tests/routers/test_data.py`. Add basic boilerplate to each file, such as importing `TestClient` and the `client` fixture from `conftest.py`.

**Test Strategy**: Verify that the new empty test files are created in the correct location and that the test suite (e.g., `pytest`) can discover them.


#### 10.2 Implement Integration Tests for System Endpoints (/version, /test3)

In `tests/routers/test_system.py`, write integration tests for the `GET /version` and `GET /test3` endpoints. Cover both authenticated and unauthenticated requests.

Using the `client` fixture from `conftest.py`, write four test functions: 
1. `test_get_version_unauthorized`: Call `/version` without headers, assert status code 401. 
2. `test_get_version_authorized`: Call `/version` with `{"Authorization": "Bearer fake-token"}` header, assert status code 200 and correct JSON response (`{"version": "..."}`). 
3. `test_get_test3_unauthorized`: Call `/test3` without headers, assert status code 401. 
4. `test_get_test3_authorized`: Call `/test3` with auth header, assert status code 200 and correct JSON response (`{"base_url": "..."}`).

**Test Strategy**: Run `pytest tests/routers/test_system.py` and ensure all four tests pass, correctly validating the endpoint's security and data response.


#### 10.3 Implement Integration Tests for /currencies/all Endpoint

In `tests/routers/test_data.py`, write integration tests for the `GET /currencies/all` endpoint, verifying both security and data integrity.

Using the `client` fixture, write two test functions:
1. `test_get_currencies_unauthorized`: Call `/currencies/all` without headers and assert a 401 status code.
2. `test_get_currencies_authorized`: Call `/currencies/all` with an `{"Authorization": "Bearer fake-token"}` header. Assert a 200 status code and that the response body is a JSON list. Assert that the list is not empty and that at least one item in the list has the expected keys (`code`, `name`, `symbol`).

**Test Strategy**: Run `pytest tests/routers/test_data.py` and ensure the tests for the currencies endpoint pass.


#### 10.4 Implement Integration Tests for /book-templates/all Endpoint

In `tests/routers/test_data.py`, add integration tests for the `GET /book-templates/all` endpoint, verifying both security and data integrity.

In the same file as the previous subtask, add two more test functions:
1. `test_get_book_templates_unauthorized`: Call `/book-templates/all` without headers and assert a 401 status code.
2. `test_get_book_templates_authorized`: Call `/book-templates/all` with an `{"Authorization": "Bearer fake-token"}` header. Assert a 200 status code and that the response body is a JSON list. Assert that the list is not empty and that at least one item has the expected keys (`template_id`, `name`, `description`).

**Test Strategy**: Run `pytest tests/routers/test_data.py` and ensure all tests in the file, including the new book template tests, pass.


#### 10.5 Refactor Authentication into a Reusable `auth_headers` Fixture

To improve maintainability and reduce code duplication, create a shared pytest fixture for the authentication headers and refactor the newly created tests to use it.

In `tests/conftest.py`, add a new function-scoped fixture named `auth_headers` that returns the dictionary `{"Authorization": "Bearer fake-token"}`. Then, go through `tests/routers/test_system.py` and `tests/routers/test_data.py` and replace the hardcoded header dictionary in the authorized test cases with this new `auth_headers` fixture.

**Test Strategy**: Re-run the entire test suite (`pytest`) and confirm that all tests still pass after the refactoring. This ensures the fixture is working correctly and has been integrated properly.


