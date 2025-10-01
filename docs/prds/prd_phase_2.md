# Product Requirements Document: Moneynote API - Phase 2

## 1) Goal & Scope

**Goal:** To implement a secure and reliable authentication system for the Moneynote API.

**Scope:** This phase focuses on core user session management functionalities. The deliverables include endpoints for user login, logout, password changes, and retrieving the initial application state for an authenticated user. This phase is critical for securing user data and enabling personalized user experiences.

## 2) Functional Specifications

The API will provide the following functional capabilities:

*   **FS-001: User Authentication:** The system must authenticate users based on their username and password and issue a JWT access token upon success.
*   **FS-002: User Logout:** The system must provide a mechanism for users to securely log out, invalidating their current session.
*   **FS-003: Password Management:** Authenticated users must be able to change their own password by providing their old and new passwords.
*   **FS-004: User Binding:** The system shall allow for binding a username to the current user, potentially for linking accounts.
*   **FS-005: Initial State Retrieval:** Once authenticated, the system must provide the essential initial data (user, book, group info) required for the client application to render the user's dashboard.

## 3) UI / UX Flow

While this document specifies the backend API, the expected user flow is as follows:

1.  A user visits the application and is presented with a login screen.
2.  The user enters their `username` and `password` and clicks "Login".
3.  The application sends a `POST /login` request to the API.
4.  If successful, the API returns an `accessToken`. The client stores this token securely.
5.  The client application then calls `GET /initState` to fetch the user's primary data (default book, group, etc.).
6.  The application dashboard is rendered with the user's financial data.
7.  To change their password, the user navigates to a "Settings" or "Profile" page, enters their old and new passwords, and submits the form, triggering a `PATCH /changePassword` request.
8.  When the user clicks "Logout", the client sends a `POST /logout` request and clears the stored `accessToken`.

## 4) Technical Specifications

### 4.1 API Logic: `POST /login`

*   **Description:** Authenticates a user and returns a JWT access token and refresh token. This endpoint does not require authentication.
*   **Business Logic:**
    1.  Accepts `username` and `password` from the request body.
    2.  Find the user in the database by their `username`. If not found, return an authentication error.
    3.  Compare the provided `password` with the hashed password stored in the database. A secure hashing algorithm (e.g., bcrypt) must be used.
    4.  If the passwords match, generate a short-lived JWT `accessToken` and a longer-lived `refreshToken`.
    5.  Return the tokens and user information to the client.
*   **Request Parameters:**
    *   `username` (String, Mandatory): User's username.
    *   `password` (String, Mandatory): User's password.
    *   `remember` (Boolean, Optional): Flag to remember the login session.
*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns `accessToken`, `refreshToken`, `username`, and `remember` status.
    *   **401 Unauthorized (Failure):** Returned if the username does not exist or the password does not match.
    *   **400 Bad Request (Failure):** Returned if `username` or `password` are missing from the request.
*   **Database CRUD:**
    *   `READ`: From `t_user` table to find the user by username and retrieve the stored password hash.
*   **Database SQL Statements:**
    ```sql
    SELECT id, username, password_hash FROM t_user WHERE username = ?;
    ```

### 4.2 API Logic: `POST /logout`

*   **Description:** Logs out the currently authenticated user.
*   **Business Logic:**
    1.  The primary logic for logout is handled on the client-side by destroying the stored JWT token.
    2.  The backend may implement token blocklisting by adding the token ID (JTI) to a cache (like Redis) to prevent its reuse until it expires.
*   **Request Parameters:** None. Requires `Authorization` header.
*   **Responses and Scenarios:**
    *   **200 OK (Success):** Indicates the server has acknowledged the logout request.
    *   **401 Unauthorized (Failure):** Returned if no valid `Authorization` header is provided.
*   **Database CRUD:** None.
*   **Database SQL Statements:** None.

### 4.3 API Logic: `PATCH /changePassword`

*   **Description:** Allows an authenticated user to change their password.
*   **Business Logic:**
    1.  Identify the current user from the `Authorization` token.
    2.  Verify the provided `oldPassword` against the user's current hashed password in the database.
    3.  If the `oldPassword` is correct, securely hash the `newPassword`.
    4.  Update the user's record in the database with the new password hash.
*   **Request Parameters:**
    *   `oldPassword` (String, Mandatory): The user's current password.
    *   `newPassword` (String, Mandatory): The user's desired new password.
*   **Responses and Scenarios:**
    *   **200 OK (Success):** Password was successfully updated.
    *   **401 Unauthorized (Failure):** Returned if the `oldPassword` is incorrect.
    *   **400 Bad Request (Failure):** Returned if `oldPassword` or `newPassword` are missing or do not meet complexity requirements.
*   **Database CRUD:**
    *   `READ`: From `t_user` to get the current user's password hash for verification.
    *   `UPDATE`: To `t_user` to set the new password hash.
*   **Database SQL Statements:**
    ```sql
    SELECT password_hash FROM t_user WHERE id = ?;
    UPDATE t_user SET password_hash = ? WHERE id = ?;
    ```

### 4.4 API Logic: `PUT /bind`

*   **Description:** Binds a username to the current user.
*   **Business Logic:** This endpoint's purpose appears to be for linking an external identity or finalizing an account setup (e.g., after a social login or initial registration with a temporary ID).
    1.  Identify the current user from the `Authorization` token.
    2.  Validate the `inviteCode`.
    3.  Update the user's record with the provided `username` and a hashed version of the `password`.
*   **Request Parameters:**
    *   `username` (String, Mandatory): Username to bind.
    *   `password` (String, Mandatory): Password to set for the user.
    *   `inviteCode` (String, Mandatory): An invitation code for validation.
*   **Responses and Scenarios:**
    *   **200 OK (Success):** The binding was successful.
    *   **401 Unauthorized (Failure):** If the user is not authenticated.
    *   **400 Bad Request (Failure):** If the `inviteCode` is invalid or the `username` is already taken.
*   **Database CRUD:**
    *   `UPDATE`: The `t_user` table to set the `username` and `password_hash` for the current user's ID.
*   **Database SQL Statements:**
    ```sql
    UPDATE t_user SET username = ?, password_hash = ? WHERE id = ?;
    ```

### 4.5 API Logic: `GET /initState`

*   **Description:** Gets the initial application state for the authenticated user.
*   **Business Logic:**
    1.  Identify the current user from the `Authorization` token.
    2.  Fetch the user's core information (e.g., username, ID).
    3.  Fetch the user's default `Book` and `Group` information.
    4.  Aggregate this information into a single response object.
*   **Request Parameters:** None. Requires `Authorization` header.
*   **Responses and Scenarios:**
    *   **200 OK (Success):** Returns the `user`, `book`, and `group` session objects.
    *   **401 Unauthorized (Failure):** If the user is not authenticated.
*   **Database CRUD:**
    *   `READ`: From `t_user`, `t_user_book`, and `t_user_group` tables to gather the required initial state.
*   **Database SQL Statements:**
    ```sql
    SELECT id, username, default_book_id, default_group_id FROM t_user WHERE id = ?;
    SELECT * FROM t_user_book WHERE id = ?;
    SELECT * FROM t_user_group WHERE id = ?;
    ```

## 5) Data Model

The primary data model affected is the `User` entity.

**`t_user` Table**

| Column Name | Data Type | Constraints & Properties | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique identifier for the user. |
| `username` | `VARCHAR` | `UNIQUE`, `NOT NULL` | User's login name. |
| `password_hash` | `VARCHAR` | `NOT NULL` | Securely hashed and salted password. |
| `default_book_id` | `INTEGER` | `FOREIGN KEY` | ID of the user's default book. |
| `default_group_id`| `INTEGER` | `FOREIGN KEY` | ID of the user's default group. |
| `create_time` | `TIMESTAMP` | `NOT NULL` | Timestamp of user creation. |

## 6) Test Cases

| Test Case ID | Endpoint | Feature Being Tested | Test Steps | Expected Result |
| :--- | :--- | :--- | :--- | :--- |
| **TC-AUTH-01** | `POST /login` | Happy Path - Correct Credentials | 1. Send request with valid `username` and `password`. | 200 OK. Response contains `accessToken` and `refreshToken`. |
| **TC-AUTH-02** | `POST /login` | Sad Path - Incorrect Password | 1. Send request with valid `username` and invalid `password`. | 401 Unauthorized. |
| **TC-AUTH-03** | `POST /login` | Sad Path - Non-existent User | 1. Send request with a `username` that does not exist. | 401 Unauthorized. |
| **TC-AUTH-04** | `POST /logout` | Happy Path - Logout | 1. Send request with a valid `Authorization` header. | 200 OK. |
| **TC-AUTH-05** | `PATCH /changePassword` | Happy Path - Correct Old Password | 1. Send request with correct `oldPassword` and a `newPassword`. | 200 OK. User can log in with the new password. |
| **TC-AUTH-06** | `PATCH /changePassword` | Sad Path - Incorrect Old Password | 1. Send request with incorrect `oldPassword`. | 401 Unauthorized. |
| **TC-AUTH-07** | `GET /initState` | Happy Path - Authenticated User | 1. Send request with a valid `Authorization` header. | 200 OK. Response contains `user`, `book`, and `group` objects. |
| **TC-AUTH-08** | `GET /initState` | Sad Path - Unauthenticated User | 1. Send request with no `Authorization` header. | 401 Unauthorized. |

## 7) Risks & Mitigations

| Risk | Mitigation |
| :--- | :--- |
| **JWT Token Theft:** An attacker could steal a user's JWT token from client-side storage. | Implement short-lived access tokens (e.g., 15 minutes) and use refresh tokens to obtain new access tokens. Store tokens in secure `HttpOnly` cookies to prevent XSS access. |
| **Insecure Password Storage:** Storing passwords in plain text or with weak hashing. | All passwords must be hashed and salted using a modern, strong algorithm like **bcrypt** or **Argon2**. |
| **Brute-force Attacks:** An attacker could repeatedly try to guess a user's password. | Implement rate limiting on the `/login` endpoint to slow down repeated failed attempts from the same IP address. |

## 8) Open Questions

1.  **`PUT /bind` Invite Code:** What is the logic for generating and validating the `inviteCode`? Is it a one-time use code? Does it expire?
2.  **Refresh Token Invalidation:** What is the strategy for invalidating refresh tokens, for example, when a user changes their password?
3.  **`remember` Flag:** What is the specific mechanism for the `remember` flag? Does it simply extend the refresh token's expiration time?

## 9) Task Seeds

*   **Task 1:** Implement `POST /login` endpoint.
    *   Add logic to `UserService` to find a user by username.
    *   Implement password verification using bcrypt.
    *   Implement JWT `accessToken` and `refreshToken` generation.
*   **Task 2:** Implement `PATCH /changePassword` endpoint.
    *   Add logic to `UserService` to verify the old password.
    *   Add logic to hash and update the new password.
*   **Task 3:** Implement `GET /initState` endpoint.
    *   Create service methods to fetch the default book and group for a user.
    *   Construct the `UserSessionVo`, `BookSessionVo`, and `GroupSessionVo` objects.
*   **Task 4:** Implement `POST /logout`.
    *   If using a blocklist, implement the caching logic for storing invalidated token IDs.
*   **Task 5:** Implement `PUT /bind`.
    *   Clarify and implement the business logic for the `inviteCode` validation.
*   **Task 6:** Security Hardening.
    *   Implement rate limiting on authentication endpoints.
    *   Write unit and integration tests for all authentication flows, including failure cases.
