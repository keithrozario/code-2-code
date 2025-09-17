# Journey 2: Tracking Incomes & Expenses

This document details the user journey for tracking incomes and expenses within the MoneyNote application. This is the core bookkeeping functionality of the system.

## 1. Detailed User Journey and Flows

This journey encompasses the creation, modification, and deletion of financial transactions. There are three primary flows: adding an expense/income, adding a transfer, and adjusting an account balance.

### Journey 1: Adding an Expense or Income

This is the most common flow. A user records a financial transaction, either money spent (expense) or money received (income).

**User Flow:**
1.  The user is within a specific "Book" (e.g., "Personal Finances").
2.  They click the "Add Transaction" button and select either "Expense" or "Income".
3.  A form appears, prompting for the following details:
    *   **Account**: The source/destination of the funds (e.g., "Checking Account", "Cash").
    *   **Date & Time**: When the transaction occurred.
    *   **Categories**: The user must select at least one category (e.g., "Food", "Salary") and enter an amount for it. They can split the transaction across multiple categories.
    *   **Payee (Optional)**: The merchant or person involved (e.g., "Supermarket", "Employer").
    *   **Tags (Optional)**: Descriptive tags for filtering (e.g., "lunch", "project-x").
    *   **Notes (Optional)**: Any additional text.
4.  The user saves the transaction.
5.  The system validates the input, creates a new `BalanceFlow` record, and updates the balance of the selected `Account`.

### Journey 2: Adding a Transfer

This flow is used to record the movement of funds between two accounts owned by the user (e.g., moving money from a savings account to a checking account).

**User Flow:**
1.  The user selects the "Add Transaction" button and chooses "Transfer".
2.  A form appears, prompting for:
    *   **From Account**: The source account.
    *   **To Account**: The destination account.
    *   **Amount**: The amount of money to transfer.
    *   **Converted Amount (if currencies differ)**: If the two accounts have different currencies, the user must specify the final amount that arrived in the destination account.
    *   **Date & Time**: When the transfer occurred.
    *   **Notes (Optional)**.
3.  The user saves the transfer.
4.  The system creates a `BalanceFlow` record of type `TRANSFER`. It deducts the `amount` from the "From Account" and adds the `convertedAmount` to the "To Account".

### Journey 3: Adjusting Account Balance

This is a special flow used to correct the balance of an account without recording a typical income or expense. For example, to set the initial balance or correct a bank error.

**User Flow:**
1.  The user navigates to a specific account's details.
2.  They select an "Adjust Balance" option.
3.  A form prompts for the **New Balance**.
4.  The user saves the adjustment.
5.  The system directly updates the `Account`'s balance to the new value.
6.  To maintain a record of this change, a new `BalanceFlow` of type `ADJUST` is created. The `amount` of this flow record is the difference between the new and old balances.

## 2. Detailed Object-Level Data Structures

The core data structure for this journey is the `BalanceFlow` entity, which is supported by several other entities and forms.

### `BalanceFlow` Entity (`t_user_balance_flow` table)

This entity represents a single financial transaction.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `book` | `Book` | (FK) The ledger this transaction belongs to. |
| `type` | `FlowType` | Enum: `EXPENSE`, `INCOME`, `TRANSFER`, `ADJUST`. |
| `amount` | `BigDecimal` | The primary amount of the transaction. For transfers, this is the source amount. |
| `convertedAmount` | `BigDecimal` | The amount converted to the book's default currency. For transfers, this is the destination amount. |
| `account` | `Account` | (FK) The primary account involved (source for expense/transfer, destination for income). |
| `to` | `Account` | (FK) The destination account, used only for `TRANSFER` type. |
| `createTime` | `Long` | The timestamp of the transaction, provided by the user. |
| `title` | `String` | An optional title for the transaction. |
| `notes` | `String` | Optional descriptive notes. |
| `creator` | `User` | (FK) The user who created the transaction. |
| `group` | `Group` | (FK) The group this transaction belongs to. |
| `payee` | `Payee` | (FK, Optional) The payee associated with the transaction. |
| `confirm` | `Boolean` | If `true`, the transaction affects account balances. |
| `include` | `Boolean` | If `true`, the transaction is included in reports. |
| `categories` | `Set<CategoryRelation>` | (Relation) Links to categories and the amount for each. |
| `tags` | `Set<TagRelation>` | (Relation) Links to descriptive tags. |
| `files` | `Set<FlowFile>` | (Relation) Links to file attachments. |

### `BalanceFlowAddForm` Data Structure

This is the Data Transfer Object (DTO) used for creating a new transaction via the API.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `book` | `Integer` | ID of the book. |
| `type` | `FlowType` | The type of transaction. |
| `title` | `String` | Optional title. |
| `createTime` | `Long` | Transaction timestamp. |
| `account` | `Integer` | ID of the source/primary account. |
| `categories` | `List<CategoryRelationForm>` | A list of categories and their respective amounts. Required for Expense/Income. |
| `payee` | `Integer` | ID of the payee. |
| `tags` | `Set<Integer>` | Set of tag IDs. |
| `to` | `Integer` | ID of the destination account for transfers. |
| `amount` | `BigDecimal` | Used for `TRANSFER` and `ADJUST` types. |
| `convertedAmount` | `BigDecimal` | Used for transfers with different currencies. |
| `notes` | `String` | Optional notes. |
| `confirm` | `Boolean` | Whether the transaction should be confirmed immediately. |
| `include` | `Boolean` | Whether to include the transaction in reports. |

## 3. Database Tables to be Updated

-   **`t_user_balance_flow`**: A new record is **inserted** for every new transaction (expense, income, transfer, or adjustment).
-   **`t_user_account`**: The `balance` column is **updated** for the affected account(s).
    -   For `EXPENSE`, the balance is decreased.
    -   For `INCOME`, the balance is increased.
    -   For `TRANSFER`, the source account balance is decreased and the destination account balance is increased.
    -   For `ADJUST`, the balance is set to the new value.
-   **`t_user_category_relation`**: Records are **inserted** to link the `BalanceFlow` to its `Category` or categories.
-   **`t_user_tag_relation`**: Records are **inserted** to link the `BalanceFlow` to its `Tag`(s).

## 4. API Calls

The interactions are handled by the `BalanceFlowController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/balance-flows` | Creates a new transaction (expense, income, or transfer). |
| `GET` | `/balance-flows` | Queries and lists existing transactions with pagination and filtering. |
| `GET` | `/balance-flows/{id}` | Retrieves the details of a single transaction. |
| `PUT` | `/balance-flows/{id}` | Updates an existing transaction. |
| `DELETE` | `/balance-flows/{id}` | Deletes a transaction. |
| `PATCH` | `/balance-flows/{id}/confirm` | Marks a previously unconfirmed transaction as confirmed, triggering balance updates. |
| `POST` | `/accounts/{id}/adjust` | (In `AccountController`) Adjusts the balance of a specific account. |

## 5. Business Rules and Functionality

The `BalanceFlowService` and `AccountService` contain the core business logic.

-   **Account Balance Update**: The system ensures that account balances are only modified for transactions that are marked as `confirmed`. The logic is encapsulated in private methods `confirmBalance` and `refundBalance` within `BalanceFlowService`.

    ```java
    // In BalanceFlowService.java
    private void confirmBalance(BalanceFlow flow) {
        if (flow.getConfirm() && flow.getAccount() != null) {
            Account account = flow.getAccount();
            if (flow.getType() == FlowType.EXPENSE) {
                account.setBalance(account.getBalance().subtract(flow.getAmount()));
            } else if (flow.getType() == FlowType.INCOME) {
                account.setBalance(account.getBalance().add(flow.getAmount()));
            } else if (flow.getType() == FlowType.TRANSFER) {
                Account toAccount = flow.getTo();
                BigDecimal amount = flow.getAmount();
                BigDecimal convertedAmount = flow.getConvertedAmount();
                account.setBalance(account.getBalance().subtract(amount));
                toAccount.setBalance(toAccount.getBalance().add(convertedAmount));
                accountRepository.save(toAccount);
            }
            accountRepository.save(account);
        }
    }
    ```

-   **Transaction Update Logic**: Updating a transaction is not a simple `UPDATE` statement. To ensure financial integrity, the system atomically deletes the old transaction (which refunds the balance) and creates a brand new one with the updated information. This simplifies logic and prevents calculation errors.

    ```java
    // In BalanceFlowService.java
    public Integer update(Integer id, BalanceFlowAddForm form) {
        BalanceFlow oldBalanceFlow = baseService.findFlowById(id);
        // book type confirm cannot be changed
        form.setBook(oldBalanceFlow.getBook().getId());
        form.setType(oldBalanceFlow.getType());
        form.setConfirm(oldBalanceFlow.getConfirm());
        BalanceFlow newBalanceFlow = add(form);
        // Handle file attachments
        Set<FlowFile> files = oldBalanceFlow.getFiles();
        files.forEach(file -> {
            file.setFlow(newBalanceFlow);
            flowFileRepository.save(file);
        });
        remove(oldBalanceFlow.getId());
        return newBalanceFlow.getId();
    }
    ```

-   **Validation**:
    *   Expense and Income transactions **must** have at least one category.
    *   Categories within a single transaction cannot be duplicated.
    *   Transfers **must** specify a `from` account, a `to` account, and an `amount`.
    *   If a transfer occurs between accounts with different currencies, the `convertedAmount` is mandatory.

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-ADD-01** | Add a valid `EXPENSE` transaction of $50 from an account with a balance of $100. | A new `BalanceFlow` record is created. The account's final balance is $50. |
| **TC-ADD-02** | Add a valid `INCOME` transaction of $200 to an account with a balance of $100. | A new `BalanceFlow` record is created. The account's final balance is $300. |
| **TC-ADD-03** | Add a valid `TRANSFER` of $100 from Account A (balance $500) to Account B (balance $200), same currency. | A `TRANSFER` record is created. Account A balance becomes $400. Account B balance becomes $300. |
| **TC-ADD-04** | Add a `TRANSFER` of 100 EUR from Account A (EUR) to Account B (USD), with a converted amount of 108 USD. | A `TRANSFER` record is created. Account A balance decreases by 100 EUR. Account B balance increases by 108 USD. |
| **TC-ADD-05** | Attempt to add an `EXPENSE` transaction with no categories. | The API should return a validation error (e.g., 400 Bad Request) and no records should be created. |
| **TC-DEL-01** | Delete a confirmed `EXPENSE` transaction of $50 from an account. | The `BalanceFlow` record is deleted. The account's balance is increased by $50. |
| **TC-DEL-02** | Delete a confirmed `TRANSFER` of $100 from Account A to Account B. | The `BalanceFlow` record is deleted. Account A's balance increases by $100. Account B's balance decreases by $100. |
| **TC-UPD-01** | Update the amount of an `EXPENSE` transaction from $50 to $60. | The old record is removed, and a new one is created. The associated account's balance is correctly debited by an additional $10 compared to its pre-update state. |
| **TC-ADJ-01** | Adjust the balance of an account from $150 to $200. | The account's balance is set to $200. A new `ADJUST` `BalanceFlow` record is created with an amount of $50. |
| **TC-CONF-01**| Create an unconfirmed expense of $30. Then, confirm it. | Initially, the account balance is unchanged. After confirmation, the account balance decreases by $30. |

## 7. State any Assumptions

*   The user is authenticated and has a valid session, including their current `User`, `Group`, and `Book` context.
*   The frontend client is responsible for providing valid entity IDs (e.g., `book`, `account`, `category`). The backend validates that the user has permission to access these entities but assumes the IDs themselves exist.
*   For multi-currency transactions, the frontend is assumed to assist in calculating or fetching the `convertedAmount`, although the user can override it. The backend only validates its presence when required.
*   The integrity of financial calculations relies on the transactional nature of the service methods (`@Transactional`). It is assumed the database supports ACID transactions.
