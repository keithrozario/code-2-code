
Here is the inventory of API endpoints based on my analysis of the controller files:

### TestController

-   **GET /version**: Get the application version.
-   **GET /test3**: Get the base URL of the application.

### AccountController (Base Path: `/accounts`)

-   **POST /**: Add a new account.
-   **GET /**: Query for accounts with pagination.
-   **GET /{id}**: Get details of a specific account.
-   **GET /statistics**: Get statistics for accounts.
-   **PUT /{id}**: Update a specific account.
-   **DELETE /{id}**: Remove a specific account.
-   **GET /all**: Get all accounts without pagination.
-   **PATCH /{id}/toggle**: Toggle the status of an account.
-   **PATCH /{id}/toggleInclude**: Toggle whether to include an account in statistics.
-   **PATCH /{id}/toggleCanExpense**: Toggle whether an account can be used for expenses.
-   **PATCH /{id}/toggleCanIncome**: Toggle whether an account can be used for income.
-   **PATCH /{id}/toggleCanTransferFrom**: Toggle whether an account can be used for transferring funds from.
-   **PATCH /{id}/toggleCanTransferTo**: Toggle whether an account can be used for transferring funds to.
-   **POST /{id}/adjust**: Adjust the balance of an account.
-   **PUT /{id}/adjust**: Update an account balance adjustment.
-   **GET /overview**: Get an overview of all accounts.
-   **PUT /{id}/updateNotes**: Update the notes for an account.

### BalanceFlowController (Base Path: `/balance-flows`)

-   **POST /**: Add a new balance flow record.
-   **GET /**: Query for balance flow records with pagination.
-   **GET /{id}**: Get details of a specific balance flow record.
-   **PUT /{id}**: Update a specific balance flow record.
-   **DELETE /{id}**: Delete a specific balance flow record.
-   **GET /statistics**: Get statistics for balance flow records.
-   **PATCH /{id}/confirm**: Confirm a balance flow record.
-   **POST /{id}/addFile**: Add a file to a balance flow record.
-   **GET /{id}/files**: Get all files associated with a balance flow record.

### BookController (Base Path: `/books`)

-   **GET /**: Query for books with pagination.
-   **GET /{id}**: Get details of a specific book.
-   **POST /**: Add a new book.
-   **GET /all**: Get all books without pagination.
-   **PUT /{id}**: Update a specific book.
-   **DELETE /{id}**: Delete a specific book.
-   **PATCH /{id}/toggle**: Toggle the status of a book.
-   **POST /template**: Add a new book from a template.
-   **POST /copy**: Add a new book by copying an existing one.
-   **GET /{id}/export**: Export balance flow records of a book to an Excel file.

### BookTemplateController (Base Path: `/book-templates`)

-   **GET /**: Get a list of book templates.
-   **GET /all**: Get a list of all book templates with only ID and name.

### CategoryController (Base Path: `/categories`)

-   **GET /**: Query for categories with pagination.
-   **GET /all**: Get all categories without pagination.
-   **POST /**: Add a new category.
-   **PATCH /{id}/toggle**: Toggle the status of a category.
-   **PUT /{id}**: Update a specific category.
-   **DELETE /{id}**: Delete a specific category.

### CurrencyController (Base Path: `/currencies`)

-   **GET /all**: Get all currencies.
-   **GET /**: Query for currencies with pagination.
-   **POST /refresh**: Refresh currency exchange rates.
-   **GET /rate**: Get the exchange rate between two currencies.
-   **GET /calc**: Calculate the converted amount between two currencies.
-   **PUT /{id}/rate**: Update the exchange rate for a currency.

### FlowFileController (Base Path: `/flow-files`)

-   **GET /view**: View a file associated with a balance flow.
-   **DELETE /{id}**: Delete a file.

### GroupController (Base Path: `/groups`)

-   **GET /**: Query for groups with pagination.
-   **POST /**: Add a new group.
-   **PUT /{id}**: Update a specific group.
-   **DELETE /{id}**: Delete a specific group.
-   **POST /{id}/inviteUser**: Invite a user to a group.
-   **POST /{id}/removeUser**: Remove a user from a group.
-   **POST /{id}/agree**: Agree to join a group.
-   **POST /{id}/reject**: Reject an invitation to join a group.
-   **GET /{id}/users**: Get all users in a group.

### NoteDayController (Base Path: `/note-days`)

-   **POST /**: Add a new note day.
-   **GET /**: Query for note days with pagination.
-   **PUT /{id}**: Update a specific note day.
-   **DELETE /{id}**: Delete a specific note day.
-   **PATCH /{id}/run**: Run a note day.
-   **PATCH /{id}/recall**: Recall a note day.

### PayeeController (Base Path: `/payees`)

-   **POST /**: Add a new payee.
-   **GET /**: Query for payees with pagination.
-   **PUT /{id}**: Update a specific payee.
-   **GET /all**: Get all payees without pagination.
-   **PATCH /{id}/toggle**: Toggle the status of a payee.
-   **PATCH /{id}/toggleCanExpense**: Toggle whether a payee can be used for expenses.
-   **PATCH /{id}/toggleCanIncome**: Toggle whether a payee can be used for income.
-   **DELETE /{id}**: Delete a specific payee.

### ReportController (Base Path: `/reports`)

-   **GET /expense-category**: Get a report of expenses by category.
-   **GET /income-category**: Get a report of income by category.
-   **GET /expense-tag**: Get a report of expenses by tag.
-   **GET /income-tag**: Get a report of income by tag.
-   **GET /expense-payee**: Get a report of expenses by payee.
-   **GET /income-payee**: Get a report of income by payee.
-   **GET /balance**: Get a balance report.

### TagController (Base Path: `/tags`)

-   **GET /**: Query for tags with pagination.
-   **GET /all**: Get all tags without pagination.
-   **POST /**: Add a new tag.
-   **PATCH /{id}/toggle**: Toggle the status of a tag.
-   **PATCH /{id}/toggleCanExpense**: Toggle whether a tag can be used for expenses.
-   **PATCH /{id}/toggleCanIncome**: Toggle whether a tag can be used for income.
-   **PATCH /{id}/toggleCanTransfer**: Toggle whether a tag can be used for transfers.
-   **PUT /{id}**: Update a specific tag.
-   **DELETE /{id}**: Delete a specific tag.

### TagRelationController (Base Path: `/tag-relations`)

-   **PUT /{id}**: Update a tag relation.

### UserController

-   **POST /login**: User login.
-   **POST /logout**: User logout.
-   **POST /register**: User registration.
-   **PUT /bind**: Bind a username to the current user.
-   **GET /initState**: Get the initial state for the current user.
-   **PATCH /setDefaultBook/{id}**: Set the default book for the current user.
-   **PATCH /setDefaultGroup/{id}**: Set the default group for the current user.
-   **PATCH /changePassword**: Change the current user's password.
-   **GET /bookSelect/all**: Get a list of books for selection.
-   **PATCH /setDefaultGroupAndBook/{id}**: Set the default group and book for the current user.
