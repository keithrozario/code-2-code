# MoneyNote Database Schema

This document outlines the database schema for the MoneyNote application. The schema is composed of several tables that store user data, financial records, and application settings.

## Table of Contents

*   [t_user_account](#t_user_account)
*   [t_user_balance_flow](#t_user_balance_flow)
*   [t_user_book](#t_user_book)
*   [t_user_category](#t_user_category)
*   [t_user_category_relation](#t_user_category_relation)
*   [t_flow_file](#t_flow_file)
*   [t_user_group](#t_user_group)
*   [t_user_note_day](#t_user_note_day)
*   [t_user_payee](#t_user_payee)
*   [t_user_tag](#t_user_tag)
*   [t_user_tag_relation](#t_user_tag_relation)
*   [t_user_user](#t_user_user)
*   [t_user_user_group_relation](#t_user_user_group_relation)

---

## t_user_account

Represents a financial account, such as a bank account, credit card, or loan.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the account. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `name` | The name of the account. | `TEXT` - A string of characters. | |
| `group_id` | The identifier of the group this account belongs to. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_group` |
| `type` | The type of account (e.g., checking, savings, credit card). | `INTEGER` - A 64-bit signed integer. | |
| `notes` | User-provided notes for the account. | `TEXT` - A string of characters. | |
| `enable` | A boolean indicating if the account is active. | `INTEGER` - A boolean value (0 or 1). | |
| `no` | The account number or card number. | `TEXT` - A string of characters. | |
| `balance` | The current balance of the account. | `REAL` - A floating-point value. | |
| `include` | A boolean indicating if the account should be included in financial summaries. | `INTEGER` - A boolean value (0 or 1). | |
| `canExpense` | A boolean indicating if the account can be used for expenses. | `INTEGER` - A boolean value (0 or 1). | |
| `canIncome` | A boolean indicating if the account can receive income. | `INTEGER` - A boolean value (0 or 1). | |
| `canTransferFrom` | A boolean indicating if funds can be transferred from this account. | `INTEGER` - A boolean value (0 or 1). | |
| `canTransferTo` | A boolean indicating if funds can be transferred to this account. | `INTEGER` - A boolean value (0 or 1). | |
| `currencyCode` | The currency code for the account (e.g., "USD"). | `TEXT` - A string of characters. | |
| `initialBalance` | The starting balance of the account. | `REAL` - A floating-point value. | |
| `creditLimit` | The credit limit for credit card accounts. | `REAL` - A floating-point value. | |
| `billDay` | The day of the month when the bill is generated for credit accounts. | `INTEGER` - A 64-bit signed integer. | |
| `apr` | The annual percentage rate for credit or loan accounts. | `REAL` - A floating-point value. | |
| `sort` | A number used for sorting accounts. | `INTEGER` - A 64-bit signed integer. | |

---

## t_user_balance_flow

Represents a single financial transaction, such as an expense, income, or transfer.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the transaction. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `book_id` | The identifier of the book this transaction belongs to. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_book` |
| `type` | The type of transaction (e.g., expense, income, transfer). | `INTEGER` - A 64-bit signed integer. | |
| `amount` | The amount of the transaction. | `REAL` - A floating-point value. | |
| `convertedAmount` | The transaction amount after currency conversion. | `REAL` - A floating-point value. | |
| `account_id` | The identifier of the account involved in the transaction. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_account` |
| `createTime` | The timestamp when the transaction was created. | `INTEGER` - A 64-bit signed integer. | |
| `title` | A title for the transaction. | `TEXT` - A string of characters. | |
| `notes` | User-provided notes for the transaction. | `TEXT` - A string of characters. | |
| `creator_id` | The identifier of the user who created the transaction. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_user` |
| `group_id` | The identifier of the group this transaction belongs to. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_group` |
| `to_id` | The identifier of the destination account in a transfer. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_account` |
| `payee_id` | The identifier of the payee for the transaction. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_payee` |
| `confirm` | A boolean indicating if the transaction is confirmed. | `INTEGER` - A boolean value (0 or 1). | |
| `include` | A boolean indicating if the transaction should be included in financial summaries. | `INTEGER` - A boolean value (0 or 1). | |
| `insertAt` | The timestamp when the transaction was inserted into the database. | `INTEGER` - A 64-bit signed integer. | |

---

## t_user_book

Represents a collection of financial records, acting as a ledger.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the book. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `name` | The name of the book. | `TEXT` - A string of characters. | |
| `group_id` | The identifier of the group this book belongs to. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_group` |
| `notes` | User-provided notes for the book. | `TEXT` - A string of characters. | |
| `enable` | A boolean indicating if the book is active. | `INTEGER` - A boolean value (0 or 1). | |
| `defaultExpenseAccount_id` | The identifier of the default account for expenses. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_account` |
| `defaultIncomeAccount_id` | The identifier of the default account for income. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_account` |
| `defaultTransferFromAccount_id` | The identifier of the default account for outgoing transfers. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_account` |
| `defaultTransferToAccount_id` | The identifier of the default account for incoming transfers. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_account` |
| `defaultExpenseCategory_id` | The identifier of the default category for expenses. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_category` |
| `defaultIncomeCategory_id` | The identifier of the default category for income. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_category` |
| `defaultCurrencyCode` | The default currency code for the book. | `TEXT` - A string of characters. | |
| `exportAt` | The timestamp of the last data export. | `INTEGER` - A 64-bit signed integer. | |
| `sort` | A number used for sorting books. | `INTEGER` - A 64-bit signed integer. | |

---

## t_user_category

Represents a category for classifying transactions.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the category. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `name` | The name of the category. | `TEXT` - A string of characters. | |
| `book_id` | The identifier of the book this category belongs to. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_book` |
| `notes` | User-provided notes for the category. | `TEXT` - A string of characters. | |
| `enable` | A boolean indicating if the category is active. | `INTEGER` - A boolean value (0 or 1). | |
| `type` | The type of category (e.g., expense, income). | `INTEGER` - A 64-bit signed integer. | |
| `sort` | A number used for sorting categories. | `INTEGER` - A 64-bit signed integer. | |
| `parent_id` | The identifier of the parent category for hierarchical structures. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_category` |

---

## t_user_category_relation

Links transactions to categories.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the relation. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `category_id` | The identifier of the category. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_category` |
| `balanceFlow_id` | The identifier of the transaction. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_balance_flow` |
| `amount` | The amount of the transaction associated with this category. | `REAL` - A floating-point value. | |
| `convertedAmount` | The amount after currency conversion. | `REAL` - A floating-point value. | |

---

## t_flow_file

Stores file attachments for transactions.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the file. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `data` | The binary data of the file. | `BLOB` - A blob of binary data. | |
| `user_id` | The identifier of the user who uploaded the file. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_user` |
| `flow_id` | The identifier of the transaction this file is attached to. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_balance_flow` |
| `createTime` | The timestamp when the file was uploaded. | `INTEGER` - A 64-bit signed integer. | |
| `contentType` | The MIME type of the file. | `TEXT` - A string of characters. | |
| `size` | The size of the file in bytes. | `INTEGER` - A 64-bit signed integer. | |
| `originalName` | The original name of the file. | `TEXT` - A string of characters. | |

---

## t_user_group

Represents a group of users who share financial data.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the group. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `name` | The name of the group. | `TEXT` - A string of characters. | |
| `notes` | User-provided notes for the group. | `TEXT` - A string of characters. | |
| `enable` | A boolean indicating if the group is active. | `INTEGER` - A boolean value (0 or 1). | |
| `creator_id` | The identifier of the user who created the group. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_user` |
| `defaultBook_id` | The identifier of the default book for the group. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_book` |
| `defaultCurrencyCode` | The default currency code for the group. | `TEXT` - A string of characters. | |

---

## t_user_note_day

Represents a note or reminder for a specific day.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the note. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `user_id` | The identifier of the user who created the note. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_user` |
| `title` | The title of the note. | `TEXT` - A string of characters. | |
| `notes` | The content of the note. | `TEXT` - A string of characters. | |
| `startDate` | The start date of the note or event. | `INTEGER` - A 64-bit signed integer. | |
| `endDate` | The end date of the note or event. | `INTEGER` - A 64-bit signed integer. | |
| `nextDate` | The next occurrence date for repeating notes. | `INTEGER` - A 64-bit signed integer. | |
| `repeatType` | The type of repetition (e.g., daily, weekly, monthly). | `INTEGER` - A 64-bit signed integer. | |
| `interval` | The interval for repetition. | `INTEGER` - A 64-bit signed integer. | |
| `totalCount` | The total number of times the note should repeat. | `INTEGER` - A 64-bit signed integer. | |
| `runCount` | The number of times the note has already repeated. | `INTEGER` - A 64-bit signed integer. | |

---

## t_user_payee

Represents a person or entity involved in a transaction.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the payee. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `name` | The name of the payee. | `TEXT` - A string of characters. | |
| `book_id` | The identifier of the book this payee belongs to. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_book` |
| `notes` | User-provided notes for the payee. | `TEXT` - A string of characters. | |
| `enable` | A boolean indicating if the payee is active. | `INTEGER` - A boolean value (0 or 1). | |
| `canExpense` | A boolean indicating if the payee can be used in expenses. | `INTEGER` - A boolean value (0 or 1). | |
| `canIncome` | A boolean indicating if the payee can be used in income transactions. | `INTEGER` - A boolean value (0 or 1). | |
| `sort` | A number used for sorting payees. | `INTEGER` - A 64-bit signed integer. | |

---

## t_user_tag

Represents a tag for labeling transactions.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the tag. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `name` | The name of the tag. | `TEXT` - A string of characters. | |
| `book_id` | The identifier of the book this tag belongs to. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_book` |
| `notes` | User-provided notes for the tag. | `TEXT` - A string of characters. | |
| `enable` | A boolean indicating if the tag is active. | `INTEGER` - A boolean value (0 or 1). | |
| `canExpense` | A boolean indicating if the tag can be used for expenses. | `INTEGER` - A boolean value (0 or 1). | |
| `canIncome` | A boolean indicating if the tag can be used for income. | `INTEGER` - A boolean value (0 or 1). | |
| `canTransfer` | A boolean indicating if the tag can be used for transfers. | `INTEGER` - A boolean value (0 or 1). | |
| `sort` | A number used for sorting tags. | `INTEGER` - A 64-bit signed integer. | |
| `parent_id` | The identifier of the parent tag for hierarchical structures. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_tag` |

---

## t_user_tag_relation

Links transactions to tags.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the relation. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `tag_id` | The identifier of the tag. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_tag` |
| `balanceFlow_id` | The identifier of the transaction. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_balance_flow` |
| `amount` | The amount of the transaction associated with this tag. | `REAL` - A floating-point value. | |
| `convertedAmount` | The amount after currency conversion. | `REAL` - A floating-point value. | |

---

## t_user_user

Represents a user of the application.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the user. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `username` | The user's username. | `TEXT` - A string of characters. | |
| `nickName` | The user's nickname. | `TEXT` - A string of characters. | |
| `password` | The user's hashed password. | `TEXT` - A string of characters. | |
| `telephone` | The user's telephone number. | `TEXT` - A string of characters. | |
| `email` | The user's email address. | `TEXT` - A string of characters. | |
| `registerIp` | The IP address used for registration. | `TEXT` - A string of characters. | |
| `defaultGroup_id` | The identifier of the user's default group. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_group` |
| `defaultBook_id` | The identifier of the user's default book. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_book` |
| `enable` | A boolean indicating if the user account is active. | `INTEGER` - A boolean value (0 or 1). | |
| `registerTime` | The timestamp of user registration. | `INTEGER` - A 64-bit signed integer. | |
| `headimgurl` | A URL to the user's profile picture. | `TEXT` - A string of characters. | |

---

## t_user_user_group_relation

Defines the relationship between users and groups, including roles.

| Name | Description | Data type | Key Type |
| :--- | :--- | :--- | :--- |
| `id` | The unique identifier for the relation. | `INTEGER` - A 64-bit signed integer. | Primary Key |
| `user_id` | The identifier of the user. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_user` |
| `group_id` | The identifier of the group. | `INTEGER` - A 64-bit signed integer. | Foreign Key to `t_user_group` |
| `role` | The role of the user in the group (e.g., owner, member). | `INTEGER` - A 64-bit signed integer. | |
