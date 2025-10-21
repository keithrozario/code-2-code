# User Journey Analysis: Journey 2: Tracking Incomes & Expenses

### 1.0 Detailed User Journeys and Flows
(Capture the step-by-step interactions a user has with the system to achieve the specific business goal of this journey. Document each distinct flow, including user actions, system responses, decision points, alternative paths, and error handling. Clearly identify start and end points.)

**User Goal:** To accurately record a financial transaction (income or expense) to keep their financial records up-to-date.

**Primary Flow: Recording a New Expense**

1.  **Start Point:** The user is logged into the application and is viewing their default "Book".
2.  **User Action:** The user clicks the "Add Expense" button.
3.  **System Response:** The system displays a form for entering transaction details. The form is pre-populated with the default expense account for the current book, and the transaction date is set to the current date.
4.  **User Action:** The user fills in the transaction details:
    *   Selects the account used for the transaction (e.g., "Checking Account").
    *   Enters the amount of the transaction.
    *   Selects one or more categories for the expense (e.g., "Groceries").
    *   Optionally adds tags, a payee, and descriptive notes.
5.  **System Response:** As the user types, the system provides suggestions for categories, tags, and payees.
6.  **User Action:** The user clicks the "Save" button.
7.  **System Response:**
    *   The system validates the submitted data. If validation fails (e.g., no category is selected), an error message is displayed.
    *   If validation succeeds, the system creates a new transaction record.
    *   The balance of the selected account is updated (decreased for an expense).
    *   The system displays a confirmation message and adds the new transaction to the user's transaction list.
8.  **End Point:** The user can see the newly created expense in their transaction history, and the corresponding account balance is updated.

**Alternative Flow: Recording a Split-Category Expense**

1.  **Context:** The user is at step 4 of the Primary Flow. They have made a purchase that spans multiple categories (e.g., a supermarket purchase including groceries and household items).
2.  **User Action:**
    *   The user adds the first category ("Groceries") and enters the amount spent in that category.
    *   The user clicks an "Add Split" or similar button to add another category line.
    *   The user adds the second category ("Household Goods") and enters the corresponding amount.
3.  **System Response:** The system shows the total transaction amount, which is the sum of the amounts from all split categories.
4.  **User Action:** The user proceeds to save the transaction.
5.  **System Response:** The system creates a single transaction record but links it to multiple categories, each with its own specified amount. The total transaction amount is deducted from the account balance.

**Error Flow: Invalid Transaction Data**

1.  **Context:** The user is at step 6 of the Primary Flow.
2.  **User Action:** The user clicks "Save" but has failed to select a category for the expense.
3.  **System Response:** The system prevents the transaction from being saved and displays an error message, such as "A category is required for expense transactions." The form remains populated with the data the user has already entered.
4.  **User Action:** The user corrects the error by selecting a category and saves the transaction again.

---

### 2.0 Detailed Object Level Data Structures
(Document the structure and attributes of key data entities involved in this journey. For each entity, list its attributes, data types, constraints (e.g., `NOT NULL`, `FOREIGN KEY`), and a brief description. Indicate relationships between entities.)

The primary data entity for this journey is `BalanceFlow`, which is supported by several other entities.

**Entity: `BalanceFlow` (Table: `t_user_balance_flow`)**
Represents a single financial transaction.

| Attribute | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**. |
| `book_id` | `INTEGER` | **Foreign Key** -> `t_user_book(id)`. `NOT NULL`. Links the transaction to a specific ledger. |
| `type` | `INTEGER` | `NOT NULL`. The type of transaction (e.g., `EXPENSE`, `INCOME`). |
| `amount` | `DECIMAL(15,2)` | `NOT NULL`. The total amount of the transaction in its original currency. |
| `converted_amount` | `DECIMAL(15,2)` | The amount converted to the book's default currency. |
| `account_id` | `INTEGER` | **Foreign Key** -> `t_user_account(id)`. The source account for the transaction. |
| `create_time` | `BIGINT` | `NOT NULL`. The timestamp when the transaction occurred. |
| `title` | `VARCHAR(32)` | An optional title for the transaction. |
| `notes` | `VARCHAR(1024)` | Optional detailed notes. |
| `payee_id` | `INTEGER` | **Foreign Key** -> `t_user_payee(id)`. The payee involved in the transaction. |
| `confirm` | `BOOLEAN` | `NOT NULL`. If `true`, the transaction affects account balances. |

*   **Relationships:**
    *   Many-to-One with `Book`
    *   Many-to-One with `Account`
    *   Many-to-One with `Payee`
    *   One-to-Many with `CategoryRelation`
    *   One-to-Many with `TagRelation`

**Entity: `CategoryRelation` (Table: `t_user_category_relation`)**
A join table linking a `BalanceFlow` to a `Category` and storing the amount for that specific category.

| Attribute | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**. |
| `category_id` | `INTEGER` | **Foreign Key** -> `t_user_category(id)`. |
| `balance_flow_id` | `INTEGER` | **Foreign Key** -> `t_user_balance_flow(id)`. |
| `amount` | `DECIMAL(15,2)` | `NOT NULL`. The portion of the transaction's total amount allocated to this category. |

*   **Relationships:**
    *   Many-to-One with `Category`
    *   Many-to-One with `BalanceFlow`

**Entity: `TagRelation` (Table: `t_user_tag_relation`)**
A join table linking a `BalanceFlow` to a `Tag`.

| Attribute | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**. |
| `tag_id` | `INTEGER` | **Foreign Key** -> `t_user_tag(id)`. |
| `balance_flow_id` | `INTEGER` | **Foreign Key** -> `t_user_balance_flow(id)`. |

*   **Relationships:**
    *   Many-to-One with `Tag`
    *   Many-to-One with `BalanceFlow`

**Entity: `Account` (Table: `t_user_account`)**
Represents a financial account.

| Attribute | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**. |
| `name` | `VARCHAR(64)` | `NOT NULL`. The name of the account. |
| `balance` | `DECIMAL(20,2)` | `NOT NULL`. The current balance of the account. |
| `currency_code` | `VARCHAR(8)` | `NOT NULL`. The currency of the account. |

---

### 3.0 Database Tables to be Updated
(Identify which database tables are directly impacted by this user journey. List the tables that are read from and written to (`INSERT`, `UPDATE`, `DELETE`). Specify the operations performed on each table within the context of the journey.)

During the "Tracking Incomes & Expenses" journey, the following tables are updated:

| Table Name | Operation | Description |
| :--- | :--- | :--- |
| **`t_user_balance_flow`** | `INSERT` | A new row is inserted to represent the income or expense transaction being recorded. |
| **`t_user_account`** | `UPDATE` | The `balance` column of the corresponding account is updated. The balance is decreased for an `EXPENSE` and increased for an `INCOME`. |
| **`t_user_category_relation`** | `INSERT` | One or more rows are inserted to link the new `BalanceFlow` record to the selected `Category` records and store the allocated amounts. |
| **`t_user_tag_relation`** | `INSERT` | (Optional) If tags are added to the transaction, one or more rows are inserted to link the `BalanceFlow` to the selected `Tag` records. |
| **`t_user_payee`** | `READ` | The table is read from to populate payee suggestions and link the transaction to an existing payee. A new payee might be created if it doesn't exist. |
| **`t_user_category`** | `READ` | The table is read from to populate category suggestions for the user. |
| **`t_user_tag`** | `READ` | The table is read from to populate tag suggestions for the user. |

---

### 4.0 Business Rules and Functionality (Detailed)
(Capture the explicit and implicit logic governing the system's behavior for this journey. For each rule, specify its name, description, trigger, logic, and outcome. Detail both front-end and back-end validations.)

| Rule ID | Name | Description | Trigger | Logic | Outcome |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **BR-TRK-01** | Transaction Type Support | The system must support the creation of four transaction types: Expense, Income, Transfer, and Adjust. | User initiates a new transaction. | The user selects a type from a predefined list. The system logic branches based on the selected `FlowType` enum. | A transaction of the specified type is created. |
| **BR-TRK-02** | Mandatory Book and Account Association | All transactions must be associated with a specific book and a financial account. | User saves a new transaction. | The backend validation checks for the presence of `book_id` and `account_id` in the request. | If missing, the transaction is rejected with an error. Otherwise, the transaction is linked correctly. |
| **BR-TRK-03** | Mandatory Category for Income/Expense | For Expense and Income types, a transaction must be linked to at least one spending/earning category. | User saves a new Expense or Income transaction. | The `BalanceFlowService.checkBeforeAdd()` method verifies that the list of categories is not empty. | If no category is provided, the save operation fails with a validation error. |
| **BR-TRK-04** | Split-Category Transaction | The system must allow for transactions to be split across multiple categories, each with its own amount. | User adds more than one category to a transaction form. | The request payload contains a list of category relations. The backend iterates through this list, creating a `CategoryRelation` record for each. | A single transaction record is created with multiple links in the `t_user_category_relation` table. |
| **BR-TRK-05** | Automatic Balance Update | Upon confirmation of a transaction, the system must automatically update the balance of the associated account(s). | A transaction is saved with `confirm=true`. | The `BalanceFlowService.confirmBalance()` method is called. It reads the account's current balance, adds (for income) or subtracts (for expense) the transaction amount, and saves the updated account. | The account balance reflects the financial impact of the transaction, ensuring data consistency. |
| **BR-TRK-06** | Transaction Edit/Delete and Balance Reversal | Users must be able to edit and delete existing transactions. Deleting a confirmed transaction must reverse the financial change on the associated account balance. | User deletes a confirmed transaction. | The `BalanceFlowService.remove()` method calls `refundBalance()`, which performs the inverse operation of `confirmBalance()` (e.g., adds the amount back for a deleted expense). | The account balance is restored to its state before the transaction occurred. |
| **BR-TRK-07** | Unconfirmed Transaction State | Users can mark transactions as "unconfirmed," which prevents them from affecting account balances until confirmed. | A transaction is saved with `confirm=false`. | The `confirmBalance()` method is not called for unconfirmed transactions. The transaction is saved, but the account balance remains unchanged. | The transaction is recorded for future reference or confirmation without immediately impacting financial summaries. |

---

### 5.0 Test Cases
(Create a comprehensive set of test cases to verify the correct implementation of the user journey and its business rules. Each test case should include an ID, the feature being tested, preconditions, steps, test data, and expected results. Cover happy paths, negative paths, boundary conditions, and error handling.)

| Test Case ID | Feature Tested | Preconditions | Steps | Test Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-TRK-01** | **Happy Path:** Create a single-category expense | User is logged in. An account "Checking" exists with a balance of $1000. A category "Food" exists. | 1. Navigate to "Add Expense". <br> 2. Select "Checking" account. <br> 3. Enter amount `50.00`. <br> 4. Select category "Food". <br> 5. Click "Save". | Amount: 50.00, Account: Checking, Category: Food | Transaction is created successfully. The balance of the "Checking" account is now $950.00. |
| **TC-TRK-02** | **Happy Path:** Create a multi-category expense | User is logged in. An account "Credit Card" exists with a balance of $500. Categories "Entertainment" and "Food" exist. | 1. Navigate to "Add Expense". <br> 2. Select "Credit Card" account. <br> 3. Add category "Food" with amount `30.00`. <br> 4. Add category "Entertainment" with amount `70.00`. <br> 5. Click "Save". | Split 1: Food, 30.00 <br> Split 2: Entertainment, 70.00 | A single transaction is created with a total amount of $100.00. The balance of the "Credit Card" account is now $400.00. |
| **TC-TRK-03** | **Happy Path:** Create and confirm an unconfirmed transaction | User is logged in. An account "Checking" exists with a balance of $1000. | 1. Create an expense of `25.00` but save it as "unconfirmed". <br> 2. Verify account balance is still $1000. <br> 3. Find the unconfirmed transaction and click "Confirm". | Amount: 25.00, Confirmed: false -> true | The transaction is now confirmed. The balance of the "Checking" account is updated to $975.00. |
| **TC-TRK-04** | **Negative Path:** Create an expense with no category | User is logged in. An account "Checking" exists. | 1. Navigate to "Add Expense". <br> 2. Select "Checking" account. <br> 3. Enter amount `10.00`. <br> 4. Do not select a category. <br> 5. Click "Save". | Amount: 10.00, Category: null | The system displays a validation error: "Category is required". The transaction is not saved. The account balance remains unchanged. |
| **TC-TRK-05** | **Negative Path:** Create an expense with zero amount | User is logged in. An account "Checking" exists. | 1. Navigate to "Add Expense". <br> 2. Select "Checking" account. <br> 3. Enter amount `0.00`. <br> 4. Select category "General". <br> 5. Click "Save". | Amount: 0.00 | The system displays a validation error: "Amount must be greater than zero". The transaction is not saved. |
| **TC-TRK-06** | **Boundary:** Delete a confirmed transaction | A confirmed expense of `50.00` exists for the "Checking" account. The current balance is $950.00. | 1. Find the `50.00` expense transaction. <br> 2. Click the "Delete" button. <br> 3. Confirm the deletion. | Transaction ID of the `50.00` expense. | The transaction is deleted. The `refundBalance()` logic is triggered, and the balance of the "Checking" account is restored to $1000.00. |

---

### 6.0 Assumptions
(Document any assumptions made during the analysis due to ambiguity or lack of definitive information. Explain the reasoning for each assumption.)

*   **CodMod Report Accuracy:** It is assumed that the provided CodMod analysis reports (`customized_report_money_note_detailed_journeys.md` and `customized_report_money_note_data_layer.md`) are accurate and faithful representations of the `moneynote-api` source code. The analysis in this document relies heavily on the details and code references within those reports.
*   **User Interface Implementation:** The user flows described are based on the backend business logic and API capabilities. It is assumed that the frontend client implements a user interface that logically corresponds to these backend processes (e.g., providing forms, buttons, and error messages as described).
*   **Default Configurations:** It is assumed that users have default books and accounts set up, as the system logic often relies on these defaults to pre-populate forms and streamline the user experience.
*   **Permissions:** It is assumed that the user performing these actions has the necessary permissions (e.g., `Operator` or `Owner` role) within their group to create and manage transactions. The journey does not cover the behavior for read-only users (e.g., `Guest` role).

---
