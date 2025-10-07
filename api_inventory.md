
Here is the API inventory for the `moneynote-api` repository, grouped by functionality:

### Test

Provides an endpoint to check the application's version.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /version | Get the application version. |
| GET | /test3 | Get the base URL. |

### User

Manages user authentication, registration, and preferences.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| POST | /login | Logs in a user. |
| POST | /logout | Logs out a user. |
| POST | /register | Registers a new user. |
| PUT | /bind | Binds a username to an account. |
| GET | /initState | Gets the initial state of the application for the user. |
| PATCH | /setDefaultBook/{id} | Sets the default book for the user. |
| PATCH | /setDefaultGroup/{id} | Sets the default group for the user. |
| PATCH | /changePassword | Changes the user's password. |
| GET | /bookSelect/all | Gets the list of books for the user to select. |
| PATCH | /setDefaultGroupAndBook/{id} | Sets the default group and book for the user. |

### Tag Relation

Manages the relationship between tags and other entities.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| PUT | /tag-relations/{id} | Updates a tag relation. |

### Tag

Manages tags for categorizing transactions.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /tags | Queries tags. |
| GET | /tags/all | Gets all tags. |
| POST | /tags | Adds a new tag. |
| PATCH | /tags/{id}/toggle | Toggles the enabled status of a tag. |
| PATCH | /tags/{id}/toggleCanExpense | Toggles whether the tag can be used for expenses. |
| PATCH | /tags/{id}/toggleCanIncome | Toggles whether the tag can be used for income. |
| PATCH | /tags/{id}/toggleCanTransfer | Toggles whether the tag can be used for transfers. |
| PUT | /tags/{id} | Updates a tag. |
| DELETE | /tags/{id} | Deletes a tag. |

### Report

Provides endpoints for generating financial reports.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /reports/expense-category | Generates a report for expense categories. |
| GET | /reports/income-category | Generates a report for income categories. |
| GET | /reports/expense-tag | Generates a report for expense tags. |
| GET | /reports/income-tag | Generates a report for income tags. |
| GET | /reports/expense-payee | Generates a report for expense payees. |
| GET | /reports/income-payee | Generates a report for income payees. |
| GET | /reports/balance | Generates a balance report. |

### Payee

Manages payees for transactions.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| POST | /payees | Adds a new payee. |
| GET | /payees | Queries payees. |
| PUT | /payees/{id} | Updates a payee. |
| GET | /payees/all | Gets all payees. |
| PATCH | /payees/{id}/toggle | Toggles the enabled status of a payee. |
| PATCH | /payees/{id}/toggleCanExpense | Toggles whether the payee can be used for expenses. |
| PATCH | /payees/{id}/toggleCanIncome | Toggles whether the payee can be used for income. |
| DELETE | /payees/{id} | Deletes a payee. |

### Note Day

Manages daily notes.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| POST | /note-days | Adds a new note day. |
| GET | /note-days | Queries note days. |
| PUT | /note-days/{id} | Updates a note day. |
| DELETE | /note-days/{id} | Deletes a note day. |
| PATCH | /note-days/{id}/run | Runs a note day. |
| PATCH | /note-days/{id}/recall | Recalls a note day. |

### Group

Manages user groups.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /groups | Queries groups. |
| POST | /groups | Adds a new group. |
| PUT | /groups/{id} | Updates a group. |
| DELETE | /groups/{id} | Deletes a group. |
| POST | /groups/{id}/inviteUser | Invites a user to a group. |
| POST | /groups/{id}/removeUser | Removes a user from a group. |
| POST | /groups/{id}/agree | Agrees to a group invitation. |
| POST | /groups/{id}/reject | Rejects a group invitation. |
| GET | /groups/{id}/users | Gets the users in a group. |

### Flow File

Manages files associated with balance flows.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /flow-files/view | Views a flow file. |
| DELETE | /flow-files/{id} | Deletes a flow file. |

### Currency

Manages currencies and exchange rates.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /currencies/all | Gets all currencies. |
| GET | /currencies | Queries currencies. |
| POST | /currencies/refresh | Refreshes currency rates. |
| GET | /currencies/rate | Gets the exchange rate between two currencies. |
| GET | /currencies/calc | Calculates the exchange between two currencies with a given amount. |
| PUT | /currencies/{id}/rate | Updates the exchange rate for a currency. |

### Category

Manages transaction categories.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /categories | Queries categories. |
| GET | /categories/all | Gets all categories. |
| POST | /categories | Adds a new category. |
| PATCH | /categories/{id}/toggle | Toggles the enabled status of a category. |
| PUT | /categories/{id} | Updates a category. |
| DELETE | /categories/{id} | Deletes a category. |

### Book Template

Manages templates for creating new books.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /book-templates | Gets all book templates. |
| GET | /book-templates/all | Gets all book templates with id and name. |

### Book

Manages financial books.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| GET | /books | Queries books. |
| GET | /books/{id} | Gets a book by ID. |
| POST | /books | Adds a new book. |
| GET | /books/all | Gets all books. |
| PUT | /books/{id} | Updates a book. |
| DELETE | /books/{id} | Deletes a book. |
| PATCH | /books/{id}/toggle | Toggles the enabled status of a book. |
| POST | /books/template | Adds a new book from a template. |
| POST | /books/copy | Adds a new book by copying an existing one. |
| GET | /books/{id}/export | Exports a book's data to an Excel file. |

### Balance Flow

Manages the flow of balances, such as income, expenses, and transfers.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| POST | /balance-flows | Adds a new balance flow. |
| GET | /balance-flows | Queries balance flows. |
| GET | /balance-flows/{id} | Gets a balance flow by ID. |
| PUT | /balance-flows/{id} | Updates a balance flow. |
| DELETE | /balance-flows/{id} | Deletes a balance flow. |
| GET | /balance-flows/statistics | Gets statistics for balance flows. |
| PATCH | /balance-flows/{id}/confirm | Confirms a balance flow. |
| POST | /balance-flows/{id}/addFile | Adds a file to a balance flow. |
| GET | /balance-flows/{id}/files | Gets the files associated with a balance flow. |

### Account

Manages financial accounts.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| POST | /accounts | Adds a new account. |
| GET | /accounts | Queries accounts. |
| GET | /accounts/{id} | Gets an account by ID. |
| GET | /accounts/statistics | Gets statistics for accounts. |
| PUT | /accounts/{id} | Updates an account. |
| DELETE | /accounts/{id} | Deletes an account. |
| GET | /accounts/all | Gets all accounts. |
| PATCH | /accounts/{id}/toggle | Toggles the enabled status of an account. |
| PATCH | /accounts/{id}/toggleInclude | Toggles whether to include the account in the total balance. |
| PATCH | /accounts/{id}/toggleCanExpense | Toggles whether the account can be used for expenses. |
| PATCH | /accounts/{id}/toggleCanIncome | Toggles whether the account can be used for income. |
| PATCH | /accounts/{id}/toggleCanTransferFrom | Toggles whether the account can be used for transfers from. |
| PATCH | /accounts/{id}/toggleCanTransferTo | Toggles whether the account can be used for transfers to. |
| POST | /accounts/{id}/adjust | Adjusts the balance of an account. |
| PUT | /accounts/{id}/adjust | Updates an account balance adjustment. |
| GET | /accounts/overview | Gets an overview of all accounts. |
| PUT | /accounts/{id}/updateNotes | Updates the notes for an account. |
