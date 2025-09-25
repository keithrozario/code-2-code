
# Journey 2: Tracking Incomes & Expenses

This document outlines the user journey for tracking incomes and expenses within the moneynote-api system.

## 1. Detailed User Journeys and Flows

The primary journey for tracking incomes and expenses revolves around creating, viewing, updating, and deleting balance flow records. A "balance flow" can be an expense, an income, a transfer between accounts, or a balance adjustment.

### Journey 2.1: Creating a New Income or Expense Record

**Objective:** To allow a user to record a new income or expense transaction.

**Start Point:** The user initiates the creation of a new transaction.

**Flow:**

1.  **User Action:** The user submits a form with the transaction details (via `POST /balance-flows`). This includes:
    *   `type`: `EXPENSE` (100) or `INCOME` (200).
    *   `book`: The ID of the financial book this transaction belongs to.
    *   `createTime`: The timestamp of the transaction.
    *   `account`: The ID of the account from which the money was spent or received.
    *   `categories`: A list of one or more category relations, each with a `category` ID and an `amount`. The sum of these amounts constitutes the total transaction amount.
    *   `payee` (Optional): The ID of the payee.
    *   `tags` (Optional): A list of tag IDs.
    *   `title` (Optional): A short title for the transaction.
    *   `notes` (Optional): Detailed notes.
    *   `confirm`: A boolean indicating if the transaction is confirmed. A confirmed transaction immediately affects the account's balance.
    *   `include`: A boolean indicating if the transaction should be included in financial statistics.

2.  **System Response (Validation):**
    *   The system validates the input. Key validations include:
        *   `book`, `type`, `createTime`, `confirm`, `include` are mandatory.
        *   For `EXPENSE` and `INCOME` types, the `categories` list must not be empty.
        *   The number of categories per transaction is limited (e.g., to 10).
        *   If the transaction `account` uses a foreign currency, a `convertedAmount` must be provided for each category.

3.  **System Response (Processing):**
    *   A new `BalanceFlow` record is created and saved to the `t_user_balance_flow` table.
    *   The total `amount` is calculated by summing the amounts from the `categories` list.
    *   Records are created in `t_category_relation` to link the transaction to its categories.
    *   If tags are provided, records are created in `t_tag_relation`.
    *   **If `confirm` is `true`:**
        *   The system calls the `confirmBalance` logic.
        *   The balance of the specified `Account` (in `t_user_account`) is updated.
            *   For `EXPENSE`, the transaction `amount` is subtracted from the account balance.
            *   For `INCOME`, the transaction `amount` is added to the account balance.

**End Point:** The system confirms the creation of the transaction. The user's account balance is updated if the transaction was confirmed.

---

### Journey 2.2: Modifying an Existing Income or Expense Record

**Objective:** To allow a user to edit the details of a previously recorded transaction.

**Start Point:** The user selects an existing transaction to edit.

**Flow:**

1.  **User Action:** The user submits the updated transaction details (via `PUT /balance-flows/{id}`). The payload is similar to the creation form.
    *   *Note:* The `book`, `type`, and `confirm` status cannot be changed via this endpoint.

2.  **System Response (Processing):** The update process is unconventional.
    *   The system **deletes the original `BalanceFlow` record**.
    *   Before deletion, it calls `refundBalance` to revert the financial impact of the original transaction on the associated account(s).
    *   A **new `BalanceFlow` record is created** with the updated information, following the same logic as "Journey 2.1: Creating a New Income or Expense Record".
    *   Any file attachments from the old transaction are re-associated with the new one.

**End Point:** The original transaction is replaced by a new one with a new ID, and the user's account balance reflects the updated transaction details.

---

### Journey 2.3: Deleting an Income or Expense Record

**Objective:** To allow a user to permanently remove a transaction.

**Start Point:** The user selects an existing transaction to delete.

**Flow:**

1.  **User Action:** The user confirms the deletion (via `DELETE /balance-flows/{id}`).

2.  **System Response (Processing):**
    *   The system retrieves the `BalanceFlow` record.
    *   It calls the `refundBalance` logic to revert the financial impact on the associated account balance.
    *   Any associated file attachments (`t_flow_file`) are deleted.
    *   The `BalanceFlow` record and its associated relations (e.g., in `t_category_relation`) are deleted from the database.

**End Point:** The transaction is removed from the system, and the user's account balance is adjusted accordingly.

## 2. Detailed Object Level Data Structures

### `BalanceFlow` (t_user_balance_flow)

This is the central entity for all income and expense transactions.

| Attribute | Data Type | Constraints/Properties | Description |
|---|---|---|---|
| `id` | `integer` | `PRIMARY KEY` | Unique identifier for the balance flow. |
| `book` | `Book` | `FOREIGN KEY (t_user_book)`, `NOT NULL` | The financial book this flow belongs to. |
| `type` | `FlowType` | `NOT NULL` | Type of flow: `EXPENSE`, `INCOME`, `TRANSFER`, `ADJUST`. |
| `amount` | `BigDecimal` | `NOT NULL` | The total amount of the transaction in the account's currency. |
| `convertedAmount` | `BigDecimal` | | The amount converted to the book's default currency. |
| `account` | `Account` | `FOREIGN KEY (t_user_account)` | The source account for the transaction. |
| `to` | `Account` | `FOREIGN KEY (t_user_account)` | The destination account (for `TRANSFER` type). |
| `createTime` | `long` | `NOT NULL` | The timestamp when the transaction occurred. |
| `title` | `string` | `maxLength=32` | An optional title for the flow. |
| `notes` | `string` | `maxLength=1024` | Optional user-provided notes. |
| `creator` | `User` | `FOREIGN KEY (t_user)`, `NOT NULL` | The user who created the flow. |
| `group` | `Group` | `FOREIGN KEY (t_user_group)`, `NOT NULL` | The group this flow belongs to. |
| `payee` | `Payee` | `FOREIGN KEY (t_user_payee)` | The payee associated with the transaction. |
| `confirm` | `boolean` | `NOT NULL` | `true` if the transaction is confirmed and affects balance. |
| `include` | `boolean` | `NOT NULL` | `true` if the transaction is included in statistics. |
| `insertAt` | `long` | `NOT NULL`, `updatable=false` | The timestamp when the record was inserted. |
| `tags` | `Set<TagRelation>` | `One-to-Many` | Tags associated with the flow. |
| `categories` | `Set<CategoryRelation>` | `One-to-Many` | Categories associated with the flow. |
| `files` | `Set<FlowFile>` | `One-to-Many` | Files attached to the flow. |

### `Account` (t_user_account)

Represents a user's financial account.

| Attribute | Data Type | Constraints/Properties | Description |
|---|---|---|---|
| `id` | `integer` | `PRIMARY KEY` | Unique identifier for the account. |
| `name` | `string` | `NOT NULL` | Name of the account (e.g., "Checking Account"). |
| `group` | `Group` | `FOREIGN KEY (t_user_group)`, `NOT NULL` | The group this account belongs to. |
| `type` | `AccountType` | `NOT NULL` | Type of account (e.g., Debit, Credit, Asset). |
| `balance` | `BigDecimal` | `NOT NULL` | The current balance of the account. |
| `currencyCode` | `string` | `NOT NULL`, `maxLength=8` | The currency code for the account (e.g., "USD"). |
| `enable` | `boolean` | `NOT NULL` | Whether the account is active. |
| `include` | `boolean` | `NOT NULL` | Whether to include this account in net worth calculations. |

### `Category` (t_user_category)

Used to classify transactions.

| Attribute | Data Type | Constraints/Properties | Description |
|---|---|---|---|
| `id` | `integer` | `PRIMARY KEY` | Unique identifier for the category. |
| `name` | `string` | `NOT NULL` | Name of the category (e.g., "Groceries", "Salary"). |
| `book` | `Book` | `FOREIGN KEY (t_user_book)`, `NOT NULL` | The book this category belongs to. |
| `type` | `CategoryType` | `NOT NULL` | Type of category: `EXPENSE` or `INCOME`. |
| `parent` | `Category` | `FOREIGN KEY (t_user_category)` | Parent category for creating a hierarchy. |
| `enable` | `boolean` | `NOT NULL` | Whether the category is active. |

## 3. Database Tables to be Updated

### Journey 2.1: Creating a New Income or Expense Record

*   **Written to:**
    *   `t_user_balance_flow`: `INSERT` a new row for the transaction.
    *   `t_category_relation`: `INSERT` rows to link the flow to categories.
    *   `t_tag_relation`: `INSERT` rows if tags are provided.
    *   `t_user_account`: `UPDATE` the `balance` of the related account if `confirm` is true.
*   **Read from:**
    *   `t_user`: To get the current user (`creator`).
    *   `t_user_group`: To get the current group.
    *   `t_user_book`: To validate the book ID.
    *   `t_user_account`: To get account details, including currency.
    *   `t_user_category`: To validate category IDs.
    *   `t_user_payee`: To validate the payee ID.

### Journey 2.2: Modifying an Existing Income or Expense Record

*   **Written to:**
    *   `t_user_balance_flow`: `DELETE` the old row, `INSERT` a new one.
    *   `t_category_relation`: `DELETE` old relations, `INSERT` new ones.
    *   `t_tag_relation`: `DELETE` old relations, `INSERT` new ones.
    *   `t_user_account`: `UPDATE` the balance twice (once to refund the old transaction, once to apply the new one).
    *   `t_flow_file`: `UPDATE` to re-link files to the new flow record.
*   **Read from:**
    *   `t_user_balance_flow`: To get the original transaction details.
    *   (And all tables read from during creation).

### Journey 2.3: Deleting an Income or Expense Record

*   **Written to:**
    *   `t_user_balance_flow`: `DELETE` the transaction row.
    *   `t_category_relation`: `DELETE` associated relations.
    *   `t_tag_relation`: `DELETE` associated relations.
    *   `t_flow_file`: `DELETE` associated files.
    *   `t_user_account`: `UPDATE` the `balance` to refund the transaction amount.
*   **Read from:**
    *   `t_user_balance_flow`: To get the transaction details before deletion.
    *   `t_user_account`: To get the account to be refunded.

## 4. Business Rules and Functionality (Detailed)

### Rule 1: Transaction Confirmation
*   **Rule Name:** `ConfirmBalance`
*   **Description:** A transaction only affects an account's financial balance after it has been explicitly confirmed.
*   **Triggering Event:**
    1.  Creating a new `BalanceFlow` with `confirm` set to `true`.
    2.  Calling the `PATCH /balance-flows/{id}/confirm` endpoint.
*   **Logic:**
    *   If `FlowType` is `EXPENSE`, `amount` is subtracted from `Account.balance`.
    *   If `FlowType` is `INCOME`, `amount` is added to `Account.balance`.
*   **Outcome:** The `balance` field of the `t_user_account` table is updated.

### Rule 2: Transaction Reversal
*   **Rule Name:** `RefundBalance`
*   **Description:** When a confirmed transaction is deleted or modified, its financial impact must be reversed.
*   **Triggering Event:**
    1.  Deleting a `BalanceFlow` (`DELETE /balance-flows/{id}`).
    2.  Updating a `BalanceFlow` (`PUT /balance-flows/{id}`), as this involves deleting the old record.
*   **Logic:**
    *   If `FlowType` is `EXPENSE`, `amount` is added back to `Account.balance`.
    *   If `FlowType` is `INCOME`, `amount` is subtracted from `Account.balance`.
*   **Outcome:** The `balance` field of the `t_user_account` table is restored to its state before the transaction.

### Rule 3: Category Requirement for Income/Expense
*   **Rule Name:** `CategoryNotEmpty`
*   **Description:** All income and expense transactions must be assigned to at least one category.
*   **Triggering Event:** Creating or updating a `BalanceFlow` with `type` = `EXPENSE` or `INCOME`.
*   **Logic:** The `categories` list in the `BalanceFlowAddForm` must not be null or empty.
*   **Outcome:** If the rule is violated, the system throws a `FailureMessageException` with the message "add.flow.category.empty" and the operation is aborted.

### Rule 4: Foreign Currency Handling
*   **Rule Name:** `RequireConvertedAmount`
*   **Description:** If a transaction involves an account with a currency different from the book's default currency, the converted amount must be explicitly provided.
*   **Triggering Event:** Creating or updating a `BalanceFlow` where `Account.currencyCode` does not match `Book.defaultCurrencyCode`.
*   **Logic:** The `convertedAmount` field in the `CategoryRelationForm` must not be null.
*   **Outcome:** If the rule is violated, the system throws a `FailureMessageException` and the operation is aborted.

## 5. Detailed Test Cases

| Test Case ID | Feature Being Tested | Preconditions | Test Steps | Test Data | Expected Result |
|---|---|---|---|---|---|
| TC-IE-001 | Happy Path: Create Confirmed Expense | User is logged in. An `Account` with ID `1` and balance `1000` exists. A `Category` with ID `10` exists. | 1. Send `POST /balance-flows`. <br> 2. Query account balance. | `type: EXPENSE`, `account: 1`, `categories: [{category: 10, amount: 50}]`, `confirm: true` | 1. API returns `200 OK`. <br> 2. A new `BalanceFlow` record is created. <br> 3. The balance of `Account` ID `1` is now `950`. |
| TC-IE-002 | Happy Path: Create Unconfirmed Income | User is logged in. An `Account` with ID `2` and balance `500` exists. A `Category` with ID `20` exists. | 1. Send `POST /balance-flows`. <br> 2. Query account balance. | `type: INCOME`, `account: 2`, `categories: [{category: 20, amount: 200}]`, `confirm: false` | 1. API returns `200 OK`. <br> 2. A new `BalanceFlow` record is created. <br> 3. The balance of `Account` ID `2` remains `500`. |
| TC-IE-003 | Negative Path: Create Expense without Category | User is logged in. | 1. Send `POST /balance-flows`. | `type: EXPENSE`, `account: 1`, `categories: []`, `confirm: true` | 1. API returns an error (e.g., `400 Bad Request`). <br> 2. Response body contains error message "add.flow.category.empty". |
| TC-IE-004 | Happy Path: Delete Expense | A confirmed expense of `50` exists for `Account` ID `1`, whose balance is `950`. | 1. Send `DELETE /balance-flows/{id}` for the expense. <br> 2. Query account balance. | `id`: ID of the expense record. | 1. API returns `200 OK`. <br> 2. The `BalanceFlow` record is deleted. <br> 3. The balance of `Account` ID `1` is restored to `1000`. |
| TC-IE-005 | Happy Path: Update Expense Amount | A confirmed expense of `50` exists for `Account` ID `1`, whose balance is `950`. | 1. Send `PUT /balance-flows/{id}` with a new amount. <br> 2. Query account balance. | `id`: ID of the expense record. `categories: [{category: 10, amount: 70}]` | 1. API returns `200 OK` with the new record ID. <br> 2. The old `BalanceFlow` record is deleted. <br> 3. A new `BalanceFlow` record is created. <br> 4. The balance of `Account` ID `1` is now `930`. |
| TC-IE-006 | Happy Path: Confirm an Unconfirmed Flow | An unconfirmed income of `200` exists for `Account` ID `2`, whose balance is `500`. | 1. Send `PATCH /balance-flows/{id}/confirm`. <br> 2. Query account balance. | `id`: ID of the income record. | 1. API returns `200 OK`. <br> 2. The `BalanceFlow` record's `confirm` flag is now `true`. <br> 3. The balance of `Account` ID `2` is now `700`. |

## 6. State Any Assumptions

*   **Assumption 1:** The user is authenticated and has a valid session, providing the necessary `User`, `Group`, and `Book` context for all operations. The `SessionUtil` class is assumed to correctly manage this context.
*   **Assumption 2:** The front-end application is responsible for providing valid IDs for `book`, `account`, `category`, `payee`, and `tags`. The back-end assumes these entities exist and will throw an `ItemNotFoundException` if they don't.
*   **Assumption 3:** The logic for currency conversion rates is handled outside the core `BalanceFlow` service. The service expects the correct `convertedAmount` to be provided in the request payload when dealing with multi-currency scenarios.
*   **Assumption 4:** The `update` operation's strategy (delete and re-create) is an intentional design choice, possibly to simplify the logic of recalculating balances and relations. This has the side effect of changing the unique identifier (`id`) of a transaction when it is edited.
