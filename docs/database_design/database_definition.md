# Database Schema Definition

This document outlines the database schema for the moneynote application. The schema is derived from the Java entity classes in the `moneynote-api` source code.

## Table: t_user_account

Represents user accounts.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the account. | Integer | INTEGER | Primary Key |
| name | The name of the account. | String | TEXT | |
| group_id | The ID of the group this account belongs to. | Group | INTEGER | Foreign Key |
| type | The type of the account (e.g., checking, savings, credit card). | AccountType | INTEGER | |
| notes | Additional notes about the account. | String | TEXT | |
| enable | Whether the account is active. | Boolean | INTEGER | |
| no | The account number. | String | TEXT | |
| balance | The current balance of the account. | BigDecimal | TEXT | |
| include | Whether to include this account in total balance calculations. | Boolean | INTEGER | |
| canExpense | Whether this account can be used for expenses. | Boolean | INTEGER | |
| canIncome | Whether this account can be used for income. | Boolean | INTEGER | |
| canTransferFrom | Whether this account can be used as a source for transfers. | Boolean | INTEGER | |
| canTransferTo | Whether this account can be used as a destination for transfers. | Boolean | INTEGER | |
| currencyCode | The currency code for the account (e.g., "USD"). | String | TEXT | |
| initialBalance | The initial balance of the account. | BigDecimal | TEXT | |
| creditLimit | The credit limit for credit accounts. | BigDecimal | TEXT | |
| billDay | The day of the month when the bill is generated. | Integer | INTEGER | |
| apr | The annual percentage rate for credit accounts. | BigDecimal | REAL | |
| sort | The sort order of the account. | Integer | INTEGER | |

## Table: t_user_balance_flow

Represents financial transactions (balance flows).

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the balance flow. | Integer | INTEGER | Primary Key |
| book_id | The ID of the book this flow belongs to. | Book | INTEGER | Foreign Key |
| type | The type of flow (e.g., expense, income, transfer). | FlowType | INTEGER | |
| amount | The amount of the transaction. | BigDecimal | TEXT | |
| convertedAmount | The amount after currency conversion. | BigDecimal | TEXT | |
| account_id | The ID of the account for this flow. | Account | INTEGER | Foreign Key |
| createTime | The timestamp when the flow was created. | Long | INTEGER | |
| title | A title for the transaction. | String | TEXT | |
| notes | Additional notes about the transaction. | String | TEXT | |
| creator_id | The ID of the user who created this flow. | User | INTEGER | Foreign Key |
| group_id | The ID of the group this flow belongs to. | Group | INTEGER | Foreign Key |
| to_id | The destination account for transfer flows. | Account | INTEGER | Foreign Key |
| payee_id | The ID of the payee for this flow. | Payee | INTEGER | Foreign Key |
| confirm | Whether the transaction is confirmed. | Boolean | INTEGER | |
| include | Whether to include this transaction in calculations. | Boolean | INTEGER | |
| insertAt | The timestamp when the record was inserted. | Long | INTEGER | |

## Table: t_user_book

Represents a collection of accounts and transactions (a book).

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the book. | Integer | INTEGER | Primary Key |
| name | The name of the book. | String | TEXT | |
| group_id | The ID of the group this book belongs to. | Group | INTEGER | Foreign Key |
| notes | Additional notes about the book. | String | TEXT | |
| enable | Whether the book is active. | Boolean | INTEGER | |
| defaultExpenseAccount_id | The default account for expenses in this book. | Account | INTEGER | Foreign Key |
| defaultIncomeAccount_id | The default account for income in this book. | Account | INTEGER | Foreign Key |
| defaultTransferFromAccount_id | The default source account for transfers in this book. | Account | INTEGER | Foreign Key |
| defaultTransferToAccount_id | The default destination account for transfers in this book. | Account | INTEGER | Foreign Key |
| defaultExpenseCategory_id | The default category for expenses in this book. | Category | INTEGER | Foreign Key |
| defaultIncomeCategory_id | The default category for income in this book. | Category | INTEGER | Foreign Key |
| defaultCurrencyCode | The default currency code for this book. | String | TEXT | |
| exportAt | The timestamp of the last export. | Long | INTEGER | |
| sort | The sort order of the book. | Integer | INTEGER | |

## Table: t_user_category

Represents transaction categories.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the category. | Integer | INTEGER | Primary Key |
| parent_id | The ID of the parent category for hierarchical categories. | Category | INTEGER | Foreign Key |
| name | The name of the category. | String | TEXT | |
| book_id | The ID of the book this category belongs to. | Book | INTEGER | Foreign Key |
| notes | Additional notes about the category. | String | TEXT | |
| enable | Whether the category is active. | Boolean | INTEGER | |
| type | The type of category (e.g., expense, income). | CategoryType | INTEGER | |
| sort | The sort order of the category. | Integer | INTEGER | |

## Table: t_user_category_relation

Represents the many-to-many relationship between balance flows and categories.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the relation. | Integer | INTEGER | Primary Key |
| category_id | The ID of the category. | Category | INTEGER | Foreign Key |
| balanceFlow_id | The ID of the balance flow. | BalanceFlow | INTEGER | Foreign Key |
| amount | The amount associated with this category for the transaction. | BigDecimal | TEXT | |
| convertedAmount | The converted amount for this category. | BigDecimal | TEXT | |

## Table: t_flow_file

Represents files attached to transactions.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the file. | Integer | INTEGER | Primary Key |
| data | The binary data of the file. | byte[] | BLOB | |
| user_id | The ID of the user who uploaded the file. | User | INTEGER | Foreign Key |
| flow_id | The ID of the balance flow this file is attached to. | BalanceFlow | INTEGER | Foreign Key |
| createTime | The timestamp when the file was uploaded. | Long | INTEGER | |
| contentType | The MIME type of the file. | String | TEXT | |
| size | The size of the file in bytes. | Long | INTEGER | |
| originalName | The original name of the file. | String | TEXT | |

## Table: t_user_group

Represents a group of users who share books.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the group. | Integer | INTEGER | Primary Key |
| name | The name of the group. | String | TEXT | |
| notes | Additional notes about the group. | String | TEXT | |
| enable | Whether the group is active. | Boolean | INTEGER | |
| creator_id | The ID of the user who created the group. | User | INTEGER | Foreign Key |
| defaultBook_id | The default book for this group. | Book | INTEGER | Foreign Key |
| defaultCurrencyCode | The default currency for this group. | String | TEXT | |

## Table: t_user_note_day

Represents daily notes or reminders.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the note. | Integer | INTEGER | Primary Key |
| user_id | The ID of the user who created the note. | User | INTEGER | Foreign Key |
| title | The title of the note. | String | TEXT | |
| notes | The content of the note. | String | TEXT | |
| startDate | The start date for the note/reminder. | Long | INTEGER | |
| endDate | The end date for the note/reminder. | Long | INTEGER | |
| nextDate | The next occurrence date for repeating notes. | Long | INTEGER | |
| repeatType | The repeat type (e.g., daily, weekly). | Integer | INTEGER | |
| interval | The interval for repeating notes. | Integer | INTEGER | |
| totalCount | The total number of occurrences for repeating notes. | Integer | INTEGER | |
| runCount | The number of times the note has already occurred. | Integer | INTEGER | |

## Table: t_user_payee

Represents payees for transactions.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the payee. | Integer | INTEGER | Primary Key |
| name | The name of the payee. | String | TEXT | |
| book_id | The ID of the book this payee belongs to. | Book | INTEGER | Foreign Key |
| notes | Additional notes about the payee. | String | TEXT | |
| enable | Whether the payee is active. | Boolean | INTEGER | |
| canExpense | Whether this payee can be used for expenses. | Boolean | INTEGER | |
| canIncome | Whether this payee can be used for income. | Boolean | INTEGER | |
| sort | The sort order of the payee. | Integer | INTEGER | |

## Table: t_user_tag

Represents tags for transactions.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the tag. | Integer | INTEGER | Primary Key |
| parent_id | The ID of the parent tag for hierarchical tags. | Tag | INTEGER | Foreign Key |
| name | The name of the tag. | String | TEXT | |
| book_id | The ID of the book this tag belongs to. | Book | INTEGER | Foreign Key |
| notes | Additional notes about the tag. | String | TEXT | |
| enable | Whether the tag is active. | Boolean | INTEGER | |
| canExpense | Whether this tag can be used for expenses. | Boolean | INTEGER | |
| canIncome | Whether this tag can be used for income. | Boolean | INTEGER | |
| canTransfer | Whether this tag can be used for transfers. | Boolean | INTEGER | |
| sort | The sort order of the tag. | Integer | INTEGER | |

## Table: t_user_tag_relation

Represents the many-to-many relationship between balance flows and tags.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the relation. | Integer | INTEGER | Primary Key |
| tag_id | The ID of the tag. | Tag | INTEGER | Foreign Key |
| balanceFlow_id | The ID of the balance flow. | BalanceFlow | INTEGER | Foreign Key |
| amount | The amount associated with this tag for the transaction. | BigDecimal | TEXT | |
| convertedAmount | The converted amount for this tag. | BigDecimal | TEXT | |

## Table: t_user_user

Represents application users.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the user. | Integer | INTEGER | Primary Key |
| username | The username for login. | String | TEXT | |
| nickName | The user's nickname. | String | TEXT | |
| password | The user's hashed password. | String | TEXT | |
| telephone | The user's telephone number. | String | TEXT | |
| email | The user's email address. | String | TEXT | |
| registerIp | The IP address used for registration. | String | TEXT | |
| defaultGroup_id | The user's default group. | Group | INTEGER | Foreign Key |
| defaultBook_id | The user's default book. | Book | INTEGER | Foreign Key |
| enable | Whether the user account is active. | Boolean | INTEGER | |
| registerTime | The timestamp of user registration. | Long | INTEGER | |
| headimgurl | The URL of the user's profile picture. | String | TEXT | |

## Table: t_user_user_group_relation

Represents the many-to-many relationship between users and groups.

| Name | Description | Current Data type | SQLite Data type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the relation. | Integer | INTEGER | Primary Key |
| user_id | The ID of the user. | User | INTEGER | Foreign Key |
| group_id | The ID of the group. | Group | INTEGER | Foreign Key |
| role | The user's role in the group (e.g., owner, member). | Integer | INTEGER | |
