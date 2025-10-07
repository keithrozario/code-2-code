Here is the analysis of the API endpoints, grouped by likely business functionality:

### Account Management
This section deals with managing financial accounts, including adding, updating, and retrieving account information.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `POST` | `/accounts` | Add a new account. |
| `GET` | `/accounts` | Query for accounts with pagination. |
| `GET` | `/accounts/{id}` | Get a specific account by its ID. |
| `GET` | `/accounts/statistics` | Get statistics for accounts. |
| `PUT` | `/accounts/{id}` | Update a specific account. |
| `DELETE` | `/accounts/{id}` | Remove a specific account. |
| `GET` | `/accounts/all` | Get all accounts without pagination. |
| `PATCH` | `/accounts/{id}/toggle` | Toggle the status of an account. |
| `PATCH` | `/accounts/{id}/toggleInclude` | Toggle whether an account is included in statistics. |
| `PATCH` | `/accounts/{id}/toggleCanExpense` | Toggle whether an account can be used for expenses. |
| `PATCH` | `/accounts/{id}/toggleCanIncome` | Toggle whether an account can be used for income. |
| `PATCH` | `/accounts/{id}/toggleCanTransferFrom` | Toggle whether an account can be used for transfers from. |
| `PATCH` | `/accounts/{id}/toggleCanTransferTo` | Toggle whether an account can be used for transfers to. |
| `POST` | `/accounts/{id}/adjust` | Adjust the balance of an account. |
| `PUT` | `/accounts/{id}/adjust` | Update an account balance adjustment. |
| `GET` | `/accounts/overview` | Get an overview of all accounts. |
| `PUT` | `/accounts/{id}/updateNotes` | Update the notes for an account. |

### Balance Flow
This section handles the flow of money, including expenses, income, and transfers.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `POST` | `/balance-flows` | Add a new balance flow record. |
| `GET` | `/balance-flows` | Query for balance flow records with pagination. |
| `GET` | `/balance-flows/{id}` | Get a specific balance flow record by its ID. |
| `PUT` | `/balance-flows/{id}` | Update a specific balance flow record. |
| `DELETE` | `/balance-flows/{id}` | Delete a specific balance flow record. |
| `GET` | `/balance-flows/statistics` | Get statistics for balance flow records. |
| `PATCH` | `/balance-flows/{id}/confirm` | Confirm a balance flow record. |
| `POST` | `/balance-flows/{id}/addFile` | Add a file to a balance flow record. |
| `GET` | `/balance-flows/{id}/files` | Get all files associated with a balance flow record. |

### Book Management
This section is for managing financial books, which can be thought of as separate ledgers.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/books` | Query for books with pagination. |
| `GET` | `/books/{id}` | Get a specific book by its ID. |
| `POST` | `/books` | Add a new book. |
| `GET` | `/books/all` | Get all books without pagination. |
| `PUT` | `/books/{id}` | Update a specific book. |
| `DELETE` | `/books/{id}` | Delete a specific book. |
| `PATCH` | `/books/{id}/toggle` | Toggle the status of a book. |
| `POST` | `/books/template` | Add a new book from a template. |
| `POST` | `/books/copy` | Add a new book by copying an existing one. |
| `GET` | `/books/{id}/export` | Export a book's data to an Excel file. |

### Book Templates
This section is for managing templates for creating new books.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/book-templates` | Get a list of available book templates. |
| `GET` | `/book-templates/all` | Get a list of all available book templates with IDs and names. |

### Category Management
This section is for managing expense and income categories.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/categories` | Query for categories with pagination. |
| `GET` | `/categories/all` | Get all categories without pagination. |
| `POST` | `/categories` | Add a new category. |
| `PATCH` | `/categories/{id}/toggle` | Toggle the status of a category. |
| `PUT` | `/categories/{id}` | Update a specific category. |
| `DELETE` | `/categories/{id}` | Delete a specific category. |

### Currency Management
This section is for managing currencies and exchange rates.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/currencies/all` | Get all available currencies. |
| `GET` | `/currencies` | Query for currencies with pagination. |
| `POST` | `/currencies/refresh` | Refresh currency exchange rates from a remote source. |
| `GET` | `/currencies/rate` | Get the exchange rate between two currencies. |
| `GET` | `/currencies/calc` | Calculate the converted amount between two currencies. |
| `PUT` | `/currencies/{id}/rate` | Update the exchange rate for a currency. |

### Flow File Management
This section is for managing files associated with balance flow records.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/flow-files/view` | View a file associated with a balance flow record. |
| `DELETE` | `/flow-files/{id}` | Delete a file associated with a balance flow record. |

### Group Management
This section is for managing user groups for collaborative bookkeeping.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/groups` | Query for groups with pagination. |
| `POST` | `/groups` | Add a new group. |
| `PUT` | `/groups/{id}` | Update a specific group. |
| `DELETE` | `/groups/{id}` | Delete a specific group. |
| `POST` | `/groups/{id}/inviteUser` | Invite a user to a group. |
| `POST` | `/groups/{id}/removeUser` | Remove a user from a group. |
| `POST` | `/groups/{id}/agree` | Agree to join a group. |
| `POST` | `/groups/{id}/reject` | Reject an invitation to join a group. |
| `GET` | `/groups/{id}/users` | Get all users in a group. |

### Note Day Management
This section is for managing daily notes.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `POST` | `/note-days` | Add a new daily note. |
| `GET` | `/note-days` | Query for daily notes with pagination. |
| `PUT` | `/note-days/{id}` | Update a specific daily note. |
| `DELETE` | `/note-days/{id}` | Delete a specific daily note. |
| `PATCH` | `/note-days/{id}/run` | Run a daily note. |
| `PATCH` | `/note-days/{id}/recall` | Recall a daily note. |

### Payee Management
This section is for managing payees for transactions.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `POST` | `/payees` | Add a new payee. |
| `GET` | `/payees` | Query for payees with pagination. |
| `PUT` | `/payees/{id}` | Update a specific payee. |
| `GET` | `/payees/all` | Get all payees without pagination. |
| `PATCH` | `/payees/{id}/toggle` | Toggle the status of a payee. |
| `PATCH` | `/payees/{id}/toggleCanExpense` | Toggle whether a payee can be used for expenses. |
| `PATCH` | `/payees/{id}/toggleCanIncome` | Toggle whether a payee can be used for income. |
| `DELETE` | `/payees/{id}` | Delete a specific payee. |

### Reporting
This section is for generating financial reports.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/reports/expense-category` | Get a report of expenses by category. |
| `GET` | `/reports/income-category` | Get a report of income by category. |
| `GET` | `/reports/expense-tag` | Get a report of expenses by tag. |
| `GET` | `/reports/income-tag` | Get a report of income by tag. |
| `GET` | `/reports/expense-payee` | Get a report of expenses by payee. |
| `GET` | `/reports/income-payee` | Get a report of income by payee. |
| `GET` | `/reports/balance` | Get a balance report. |

### Tag Management
This section is for managing tags for transactions.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/tags` | Query for tags with pagination. |
| `GET` | `/tags/all` | Get all tags without pagination. |
| `POST` | `/tags` | Add a new tag. |
| `PATCH` | `/tags/{id}/toggle` | Toggle the status of a tag. |
| `PATCH` | `/tags/{id}/toggleCanExpense` | Toggle whether a tag can be used for expenses. |
| `PATCH` | `/tags/{id}/toggleCanIncome` | Toggle whether a tag can be used for income. |
| `PATCH` | `/tags/{id}/toggleCanTransfer` | Toggle whether a tag can be used for transfers. |
| `PUT` | `/tags/{id}` | Update a specific tag. |
| `DELETE` | `/tags/{id}` | Delete a specific tag. |

### Tag Relation Management
This section is for managing the relationship between tags and other entities.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `PUT` | `/tag-relations/{id}` | Update a tag relation. |

### User Management
This section is for managing user accounts and authentication.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `POST` | `/login` | User login. |
| `POST` | `/logout` | User logout. |
| `POST` | `/register` | User registration. |
| `PUT` | `/bind` | Bind a username to an account. |
| `GET` | `/initState` | Get the initial state for the user. |
| `PATCH` | `/setDefaultBook/{id}` | Set the default book for the user. |
| `PATCH` | `/setDefaultGroup/{id}` | Set the default group for the user. |
| `PATCH` | `/changePassword` | Change the user's password. |
| `GET` | `/bookSelect/all` | Get a list of books for selection. |
| `PATCH` | `/setDefaultGroupAndBook/{id}` | Set the default group and book for the user. |

### System
This section is for system-level operations.

| HTTP Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `GET` | `/version` | Get the application version. |
| `GET` | `/test3` | Test endpoint to get the base URL. |
