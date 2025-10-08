
Of course. Here is a comprehensive API inventory of the project, grouped by functionality.

### Account Management
Manages user accounts and their properties.

| HTTP Method | Endpoint Path                        | Description                                     |
|-------------|--------------------------------------|-------------------------------------------------|
| POST        | `/accounts`                          | Add a new account.                              |
| GET         | `/accounts`                          | Query for accounts with optional filters.       |
| GET         | `/accounts/{id}`                     | Retrieve a single account by its ID.            |
| GET         | `/accounts/statistics`               | Get statistics for accounts.                    |
| PUT         | `/accounts/{id}`                     | Update an existing account.                     |
| DELETE      | `/accounts/{id}`                     | Remove an account.                              |
| GET         | `/accounts/all`                      | Retrieve all accounts.                          |
| PATCH       | `/accounts/{id}/toggle`              | Toggle the enabled/disabled status of an account.|
| PATCH       | `/accounts/{id}/toggleInclude`       | Toggle whether the account is included in totals. |
| PATCH       | `/accounts/{id}/toggleCanExpense`    | Toggle whether the account can be used for expenses.|
| PATCH       | `/accounts/{id}/toggleCanIncome`     | Toggle whether the account can be used for income.  |
| PATCH       | `/accounts/{id}/toggleCanTransferFrom`| Toggle whether transfers can be made from the account.|
| PATCH       | `/accounts/{id}/toggleCanTransferTo` | Toggle whether transfers can be made to the account.  |
| POST        | `/accounts/{id}/adjust`              | Create a balance adjustment for an account.     |
| PUT         | `/accounts/{id}/adjust`              | Update a balance adjustment for an account.     |
| GET         | `/accounts/overview`                 | Get an overview of all accounts.                |
| PUT         | `/accounts/{id}/updateNotes`         | Update the notes for an account.                |

### Balance Flow Management
Manages the creation and modification of financial transactions (balance flows).

| HTTP Method | Endpoint Path                 | Description                                  |
|-------------|-------------------------------|----------------------------------------------|
| POST        | `/balance-flows`              | Add a new balance flow (transaction).        |
| GET         | `/balance-flows`              | Query for balance flows with filters.        |
| GET         | `/balance-flows/{id}`         | Get a single balance flow by its ID.         |
| PUT         | `/balance-flows/{id}`         | Update an existing balance flow.             |
| DELETE      | `/balance-flows/{id}`         | Delete a balance flow.                       |
| GET         | `/balance-flows/statistics`   | Get statistics for balance flows.            |
| PATCH       | `/balance-flows/{id}/confirm` | Confirm a pending balance flow.              |
| POST        | `/balance-flows/{id}/addFile` | Attach a file to a balance flow.             |
| GET         | `/balance-flows/{id}/files`   | Retrieve files attached to a balance flow.   |

### Book Management
Manages collections of financial records (books).

| HTTP Method | Endpoint Path        | Description                             |
|-------------|----------------------|-----------------------------------------|
| GET         | `/books`             | Query for books with optional filters.  |
| GET         | `/books/{id}`        | Get a single book by its ID.            |
| POST        | `/books`             | Add a new book.                         |
| GET         | `/books/all`         | Retrieve all books.                     |
| PUT         | `/books/{id}`        | Update an existing book.                |
| DELETE      | `/books/{id}`        | Delete a book.                          |
| PATCH       | `/books/{id}/toggle` | Toggle the enabled/disabled status of a book.|
| POST        | `/books/template`    | Add a new book from a template.         |
| POST        | `/books/copy`        | Create a copy of an existing book.      |
| GET         | `/books/{id}/export` | Export a book's data to a file.         |

### Book Template Management
Manages templates for creating new books.

| HTTP Method | Endpoint Path         | Description                   |
|-------------|-----------------------|-------------------------------|
| GET         | `/book-templates`     | Get a list of book templates. |
| GET         | `/book-templates/all` | Get all book templates.       |

### Category Management
Manages transaction categories.

| HTTP Method | Endpoint Path           | Description                                |
|-------------|-------------------------|--------------------------------------------|
| GET         | `/categories`           | Query for categories with optional filters.|
| GET         | `/categories/all`       | Retrieve all categories.                   |
| POST        | `/categories`           | Add a new category.                        |
| PATCH       | `/categories/{id}/toggle`| Toggle the enabled/disabled status of a category.|
| PUT         | `/categories/{id}`      | Update an existing category.               |
| DELETE      | `/categories/{id}`      | Delete a category.                         |

### Currency Management
Manages currency exchange rates and conversions.

| HTTP Method | Endpoint Path         | Description                          |
|-------------|-----------------------|--------------------------------------|
| GET         | `/currencies/all`     | Get all supported currencies.        |
| GET         | `/currencies`         | Query for currencies.                |
| POST        | `/currencies/refresh` | Refresh currency exchange rates.     |
| GET         | `/currencies/rate`    | Get the exchange rate between two currencies.|
| GET         | `/currencies/calc`    | Calculate a currency conversion.     |
| PUT         | `/currencies/{id}/rate`| Manually update a currency's exchange rate.|

### Flow File Management
Manages files associated with balance flows.

| HTTP Method | Endpoint Path      | Description              |
|-------------|--------------------|--------------------------|
| GET         | `/flow-files/view` | View a specific flow file. |
| DELETE      | `/flow-files/{id}` | Delete a flow file.      |

### Group Management
Manages user groups for shared financial tracking.

| HTTP Method | Endpoint Path             | Description                         |
|-------------|---------------------------|-------------------------------------|
| GET         | `/groups`                 | Query for user groups.              |
| POST        | `/groups`                 | Add a new group.                    |
| PUT         | `/groups/{id}`            | Update an existing group.           |
| DELETE      | `/groups/{id}`            | Delete a group.                     |
| POST        | `/groups/{id}/inviteUser` | Invite a user to a group.           |
| POST        | `/groups/{id}/removeUser` | Remove a user from a group.         |
| POST        | `/groups/{id}/agree`      | Accept an invitation to join a group.|
| POST        | `/groups/{id}/reject`     | Decline an invitation to join a group.|
| GET         | `/groups/{id}/users`      | Get a list of users in a group.     |

### Note Day Management
Manages daily notes or reminders.

| HTTP Method | Endpoint Path        | Description                  |
|-------------|----------------------|------------------------------|
| POST        | `/note-days`         | Add a new daily note.        |
| GET         | `/note-days`         | Query for daily notes.       |
| PUT         | `/note-days/{id}`    | Update an existing daily note.|
| DELETE      | `/note-days/{id}`    | Delete a daily note.         |
| PATCH       | `/note-days/{id}/run`  | Mark a daily note as completed.|
| PATCH       | `/note-days/{id}/recall`| Recall a completed daily note. |

### Payee Management
Manages payees for transactions.

| HTTP Method | Endpoint Path           | Description                                  |
|-------------|-------------------------|----------------------------------------------|
| POST        | `/payees`               | Add a new payee.                             |
| GET         | `/payees`               | Query for payees with optional filters.      |
| PUT         | `/payees/{id}`          | Update an existing payee.                    |
| GET         | `/payees/all`           | Retrieve all payees.                         |
| PATCH       | `/payees/{id}/toggle`   | Toggle the enabled/disabled status of a payee.|
| PATCH       | `/payees/{id}/toggleCanExpense`| Toggle whether the payee can be used for expenses.|
| PATCH       | `/payees/{id}/toggleCanIncome` | Toggle whether the payee can be used for income.  |
| DELETE      | `/payees/{id}`          | Delete a payee.                              |

### Report Management
Provides endpoints for generating financial reports.

| HTTP Method | Endpoint Path             | Description                          |
|-------------|---------------------------|--------------------------------------|
| GET         | `/reports/expense-category`| Get a report of expenses by category.|
| GET         | `/reports/income-category` | Get a report of income by category.  |
| GET         | `/reports/expense-tag`     | Get a report of expenses by tag.     |
| GET         | `/reports/income-tag`      | Get a report of income by tag.       |
| GET         | `/reports/expense-payee`   | Get a report of expenses by payee.   |
| GET         | `/reports/income-payee`    | Get a report of income by payee.     |
| GET         | `/reports/balance`         | Get a balance report.                |

### Tag Management
Manages tags for categorizing transactions.

| HTTP Method | Endpoint Path            | Description                                  |
|-------------|--------------------------|----------------------------------------------|
| GET         | `/tags`                  | Query for tags with optional filters.        |
| GET         | `/tags/all`              | Retrieve all tags.                           |
| POST        | `/tags`                  | Add a new tag.                               |
| PATCH       | `/tags/{id}/toggle`      | Toggle the enabled/disabled status of a tag. |
| PATCH       | `/tags/{id}/toggleCanExpense`| Toggle whether the tag can be used for expenses.|
| PATCH       | `/tags/{id}/toggleCanIncome` | Toggle whether the tag can be used for income.  |
| PATCH       | `/tags/{id}/toggleCanTransfer`| Toggle whether the tag can be used for transfers.|
| PUT         | `/tags/{id}`             | Update an existing tag.                      |
| DELETE      | `/tags/{id}`             | Delete a tag.                                |

### Tag Relation Management
Manages the relationships between tags and other entities.

| HTTP Method | Endpoint Path         | Description                |
|-------------|-----------------------|----------------------------|
| PUT         | `/tag-relations/{id}` | Update a tag relationship. |

### User Management
Handles user authentication and profile settings.

| HTTP Method | Endpoint Path                    | Description                          |
|-------------|----------------------------------|--------------------------------------|
| POST        | `/login`                         | Authenticate a user and create a session.|
| POST        | `/logout`                        | Log out the current user.            |
| POST        | `/register`                      | Register a new user.                 |
| PUT         | `/bind`                          | Bind a username to an account.       |
| GET         | `/initState`                     | Get the initial state for the user.  |
| PATCH       | `/setDefaultBook/{id}`           | Set the user's default book.         |
| PATCH       | `/setDefaultGroup/{id}`          | Set the user's default group.        |
| PATCH       | `/changePassword`                | Change the user's password.          |
| GET         | `/bookSelect/all`                | Get all book selections for the user.|
| PATCH       | `/setDefaultGroupAndBook/{id}`   | Set the user's default group and book.|

### Miscellaneous
General and test endpoints.

| HTTP Method | Endpoint Path | Description               |
|-------------|---------------|---------------------------|
| GET         | `/version`    | Get the application version.|
| GET         | `/test3`      | A test endpoint.          |
