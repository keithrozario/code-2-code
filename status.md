# Project Status

## Current Status

All planned development tasks for this phase have been successfully completed or intentionally cancelled based on revised project scope.

- **All Code Implemented:** All required features, including data models, CRUD functions, services, and API endpoints, have been implemented.
- **All Tests Passing:** The comprehensive test suite, including unit tests for CRUD logic and integration tests for all API endpoints, is passing without errors.
- **Deployment Ready:** The application is fully containerized using a `Dockerfile`.
- **Deployment Scripts:** Scripts for deploying to Google Cloud Run (`deploy.sh`) and for testing the live deployment (`test_deployment.py`) have been created and verified.
- **Local Environment:** The local development environment is stable, with schema and dependency issues resolved.

The project is considered feature-complete for this phase and is in a stable, tested, and deployable state.

## Implemented API Endpoints

The following API endpoints have been created and are fully functional. All endpoints require a valid JWT `Authorization: Bearer <token>` header.

| Method | Path                               | Description                                                              |
| :----- | :--------------------------------- | :----------------------------------------------------------------------- |
| `GET`  | `/api/v1/version`                  | Retrieves the application's version number.                              |
| `GET`  | `/api/v1/test3`                    | Retrieves the application's configured base URL.                         |
| `GET`  | `/api/v1/currencies/all`           | Returns a list of all supported currencies.                              |
| `GET`  | `/api/v1/book-templates/all`       | Returns a list of all available book templates.                          |
| `GET`  | `/api/v1/users/initState`          | Retrieves the initial state for a logged-in user (user, group, book info). |
| `POST` | `/api/v1/groups/`                  | Creates a new group and a default book within it.                        |
| `POST` | `/api/v1/books/`                   | Creates a new, empty book within a specified group.                      |
| `POST` | `/api/v1/books/template`           | Creates a new book from a system-defined template.                       |
| `POST` | `/api/v1/books/copy`               | Creates a new book by copying the structure of an existing book.         |
