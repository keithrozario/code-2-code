# Database Schema

This document outlines the database schema for the Money-note application, designed for SQLite3.

## Table of Contents
- [t_user](#t_user)
- [t_user_group](#t_user_group)
- [t_user_book](#t_user_book)
- [t_user_account](#t_user_account)
- [t_user_category](#t_user_category)
- [t_user_payee](#t_user_payee)
- [t_tag](#t_tag)
- [t_user_balance_flow](#t_user_balance_flow)
- [t_category_relation](#t_category_relation)
- [t_tag_relation](#t_tag_relation)
- [t_flow_file](#t_flow_file)

---

### `t_user`
Stores user information. This table is inferred from foreign key relationships in other tables.

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the user. |
| `name` | `TEXT` | The user's name. |

---

### `t_user_group`
Stores information about user groups, which encapsulate a user's entire data set. This table is inferred from foreign key relationships.

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the group. |
| `name` | `TEXT` | The name of the group. |
| `defaultCurrencyCode` | `TEXT` | The default currency for the group (e.g., "USD"). |

---

### `t_user_book`
Stores user-created books to segregate financial records (e.g., "Personal", "Business").

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the book. |
| `name` | `TEXT` | The name of the book. Must be unique within a group. |
| `group_id` | `INTEGER` | Foreign key to `t_user_group`. |
| `notes` | `TEXT` | Optional descriptive notes for the book. |
| `enable` | `INTEGER` | Boolean (0 or 1) indicating if the book is active. |
| `defaultExpenseAccount_id` | `INTEGER` | Foreign key to `t_user_account` for default expense transactions. |
| `defaultIncomeAccount_id` | `INTEGER` | Foreign key to `t_user_account` for default income transactions. |
| `defaultTransferFromAccount_id` | `INTEGER` | Foreign key to `t_user_account` for default transfer source. |
| `defaultTransferToAccount_id` | `INTEGER` | Foreign key to `t_user_account` for default transfer destination. |
| `defaultCurrencyCode` | `TEXT` | The default currency for the book (e.g., "USD", "EUR"). |
| `sort` | `INTEGER` | An integer used for sorting the list of books. |

---

### `t_user_account`
Represents a single financial account, such as a bank account, credit card, or loan.

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the account. |
| `name` | `TEXT` | User-defined name for the account (e.g., "Chase Checking"). |
| `group_id` | `INTEGER` | Foreign key to `t_user_group`. |
| `type` | `TEXT` | The account type (`CHECKING`, `CREDIT`, `ASSET`, `DEBT`). |
| `notes` | `TEXT` | Optional descriptive notes. |
| `enable` | `INTEGER` | Boolean (0 or 1) indicating if the account is active. |
| `no` | `TEXT` | Optional account number or card number. |
| `balance` | `REAL` | The current balance of the account in its native currency. |
| `include` | `INTEGER` | Boolean (0 or 1) to include in net worth calculations. |
| `currencyCode` | `TEXT` | The currency code for the account (e.g., "USD"). |
| `initialBalance` | `REAL` | The starting balance of the account. |
| `creditLimit` | `REAL` | The credit limit for `CREDIT` type accounts. |

---

### `t_user_category`
Stores categories used to classify income and expense transactions.

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the category. |
| `name` | `TEXT` | Name of the category (e.g., "Groceries", "Salary"). |
| `book_id` | `INTEGER` | Foreign key to `t_user_book`. |
| `type` | `TEXT` | Type of category: `EXPENSE` or `INCOME`. |
| `parent_id` | `INTEGER` | Foreign key to `t_user_category` for creating a hierarchy. |
| `enable` | `INTEGER` | Boolean (0 or 1) indicating if the category is active. |

---

### `t_user_payee`
Stores information about payees (people or organizations) involved in transactions.

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the payee. |
| `name` | `TEXT` | The name of the payee. |
| `book_id` | `INTEGER` | Foreign key to `t_user_book`. |
| `enable` | `INTEGER` | Boolean (0 or 1) indicating if the payee is active. |

---

### `t_tag`
Stores tags that can be associated with transactions for flexible labeling.

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the tag. |
| `name` | `TEXT` | The name of the tag. |
| `book_id` | `INTEGER` | Foreign key to `t_user_book`. |
| `enable` | `INTEGER` | Boolean (0 or 1) indicating if the tag is active. |

---

### `t_user_balance_flow`
This is the central table for all transactions (income, expenses, transfers).

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the balance flow. |
| `book_id` | `INTEGER` | Foreign key to `t_user_book`. |
| `type` | `TEXT` | Type of flow: `EXPENSE`, `INCOME`, `TRANSFER`, `ADJUST`. |
| `amount` | `REAL` | The total amount in the account's currency. |
| `convertedAmount` | `REAL` | The amount converted to the book's default currency. |
| `account_id` | `INTEGER` | Foreign key to the source `t_user_account`. |
| `to_account_id` | `INTEGER` | Foreign key to the destination `t_user_account` (for transfers). |
| `createTime` | `INTEGER` | The timestamp (Unix epoch) when the transaction occurred. |
| `title` | `TEXT` | An optional title for the transaction. |
| `notes` | `TEXT` | Optional user-provided notes. |
| `creator_id` | `INTEGER` | Foreign key to `t_user`. |
| `group_id` | `INTEGER` | Foreign key to `t_user_group`. |
| `payee_id` | `INTEGER` | Foreign key to `t_user_payee`. |
| `confirm` | `INTEGER` | Boolean (0 or 1) if the transaction is confirmed and affects balance. |
| `include` | `INTEGER` | Boolean (0 or 1) if the transaction is included in statistics. |
| `insertAt` | `INTEGER` | The timestamp (Unix epoch) when the record was inserted. |

---

### `t_category_relation`
A linking table to support many-to-many relationships between transactions (`t_user_balance_flow`) and categories (`t_user_category`). A single transaction can be split into multiple categories.

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the relation. |
| `flow_id` | `INTEGER` | Foreign key to `t_user_balance_flow`. |
| `category_id` | `INTEGER` | Foreign key to `t_user_category`. |
| `amount` | `REAL` | The portion of the transaction amount allocated to this category. |
| `convertedAmount` | `REAL` | The converted portion of the amount. |

---

### `t_tag_relation`
A linking table to support many-to-many relationships between transactions (`t_user_balance_flow`) and tags (`t_tag`).

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the relation. |
| `flow_id` | `INTEGER` | Foreign key to `t_user_balance_flow`. |
| `tag_id` | `INTEGER` | Foreign key to `t_tag`. |

---

### `t_flow_file`
Stores files (e.g., receipts, invoices) attached to transactions.

| Element Name | SQLite3 Type | Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | Primary key for the file record. |
| `data` | `BLOB` | The binary content of the file. |
| `creator_id` | `INTEGER` | Foreign key to `t_user` who uploaded the file. |
| `flow_id` | `INTEGER` | Foreign key to the `t_user_balance_flow` transaction. |
| `createTime` | `INTEGER` | The timestamp (Unix epoch) when the file was uploaded. |
| `contentType` | `TEXT` | The MIME type of the file (e.g., "image/png"). |
| `size` | `INTEGER` | The size of the file in bytes. |
| `originalName` | `TEXT` | The original name of the file as uploaded by the user. |
