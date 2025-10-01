# Business Requirement Document: Tracking Incomes & Expenses

## 1.0 Summary
This document outlines the business requirements for the "Tracking Incomes & Expenses" feature of the MoneyNote application. The core purpose of this feature is to provide users with the ability to accurately record, modify, and delete their financial transactions (incomes and expenses). Each transaction affects the balance of a user-specified financial account, ensuring that users have an up-to-date and accurate view of their financial situation. The system ensures data integrity by requiring categorization for all transactions and handling financial updates within atomic, transactional operations.

---

## 2.0 Project Scope
### 2.1 In-Scope
*   **Create Income/Expense Records:** Users can create new financial transactions, specifying details such as type (income/expense), amount, account, categories, and confirmation status.
*   **View Income/Expense Records:** Users can retrieve and view the details of previously created transactions.
*   **Update Income/Expense Records:** Users can modify the details of existing transactions.
*   **Delete Income/Expense Records:** Users can permanently remove transactions from their records.
*   **Balance Adjustment:** Account balances are automatically updated when a transaction is confirmed, modified, or deleted.
*   **Transaction Categorization:** All income and expense transactions must be assigned to one or more categories.

### 2.2 Out-of-Scope
*   **Management of Core Entities:** The creation, management, and deletion of `Books`, `Accounts`, `Categories`, `Tags`, and `Payees` are not covered by this document.
*   **User and Group Management:** User registration, authentication, and management of collaborative `Groups` are out-of-scope.
*   **Financial Reporting:** The generation of analytical reports based on transaction data is a separate feature.
*   **Currency Exchange Rate Management:** The logic for fetching and managing currency conversion rates is out-of-scope.
*   **Transfer and Adjustment Flows:** This document focuses specifically on `EXPENSE` and `INCOME` type transactions (`FlowType`), not `TRANSFER` or `ADJUST` types.

---

## 3.0 Business Requirements

**BR-001:** The system must provide a reliable and accurate mechanism for users to record all financial incomes and expenses, ensuring that the balance of their financial accounts is maintained in real-time upon transaction confirmation. This is critical for the core value proposition of personal financial monitoring.

### 3.1 Functional Requirements
**FR-001: Create Financial Transaction**
*   The system must allow an authenticated user to create a new income or expense transaction by submitting a valid transaction form (`BalanceFlowAddForm`). The new transaction record (`BalanceFlow`) must be successfully persisted in the `t_user_balance_flow` table within 500 milliseconds of the request. Success will be measured by a 99.9% success rate for valid submissions during load testing. This functionality is implemented in the `BalanceFlowService::add` method, triggered by the `POST /balance-flows` endpoint.

**FR-002: Update Account Balance on Confirmation**
*   When a transaction is created with the `confirm` flag set to `true`, or when an existing unconfirmed transaction is confirmed via the `PATCH /balance-flows/{id}/confirm` endpoint, the system must atomically update the `balance` of the associated `Account` in the `t_user_account` table. For an `INCOME`, the amount is added; for an `EXPENSE`, it is subtracted. This operation must occur within the same database transaction as the flow creation/update to ensure data consistency. This is achievable with the existing `@Transactional` implementation in `BalanceFlowService::confirmBalance`.

**FR-003: Enforce Transaction Categorization**
*   The system must enforce the rule that all `EXPENSE` and `INCOME` type transactions are associated with at least one financial category. The system must reject any transaction creation or update attempt that does not have at least one item in its `categories` list, returning a "add.flow.category.empty" error message within 400ms. This validation is implemented in the `BalanceFlowService::add` method and is realistic given the existing validation framework.

**FR-004: Modify Financial Transaction**
*   The system must allow a user to modify an existing income or expense transaction via the `PUT /balance-flows/{id}` endpoint. The update process must be atomic: it must first reverse the financial impact of the original transaction (`refundBalance`), then delete the original `BalanceFlow` record, and finally create a new `BalanceFlow` record with the updated details. This entire operation, implemented in `BalanceFlowService::update`, must complete successfully within 750 milliseconds and result in a new transaction ID, ensuring the user's account balance accurately reflects the new transaction details.

**FR-005: Delete Financial Transaction**
*   The system must allow a user to permanently delete an income or expense transaction via the `DELETE /balance-flows/{id}` endpoint. The deletion process, handled by `BalanceFlowService::remove`, must first reverse the transaction's financial impact on the associated account's balance (`refundBalance`) and then permanently remove the `BalanceFlow` record and all its associated relations (categories, tags, files) from the database. This ensures that no orphaned data remains and financial records are consistent.

---
## 4.0 Assumptions, Constraints, and Dependencies
### 4.1 Assumptions
*   **User Context:** It is assumed that the user is authenticated and a valid session context (`CurrentSession`) is available, providing the necessary `User`, `Group`, and `Book` information for all operations.
*   **Entity Existence:** The system assumes that the front-end provides valid, existing IDs for associated entities like `book`, `account`, `category`, and `payee`. The back-end will throw an exception if these entities are not found.
*   **Foreign Currency:** It is assumed that if a transaction involves a foreign currency, the client is responsible for providing the correct `convertedAmount` in the payload, as the core transaction logic does not perform currency conversion.

### 4.2 Constraints
*   **Update Operation ID Change:** The current implementation of the update functionality (delete and re-create) results in the modified transaction being assigned a new unique identifier (`id`). Client applications must be aware that a transaction's ID is not stable across edits.
*   **Database Technology:** The entire implementation is tightly coupled with a relational database (MySQL) and the Spring Data JPA framework.

### 4.3 Dependencies
*   **Core Entity Management:** This functionality is dependent on the pre-existence of `User`, `Group`, `Book`, and `Account` entities, which are managed by other modules.
*   **Authentication & Authorization:** The entire journey depends on the system's security module (`AuthInterceptor`, `JwtUtils`) to authenticate the user and scope data access to the correct user and group.
