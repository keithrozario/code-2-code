
# Database Schema Definition

This document outlines the database schema for the moneynote-api application.

## Table: t_user_account

This table stores user account information.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the account. | Integer | INTEGER | Primary Key |
| name | The name of the account. | String | TEXT | |
| group_id | The ID of the group this account belongs to. | Integer | INTEGER | Foreign Key |
| type | The type of account (e.g., checking, savings, credit). | Integer | INTEGER | |
| notes | Additional notes about the account. | String | TEXT | |
| enable | Flag indicating if the account is active. | Boolean | INTEGER | |
| no | The account number. | String | TEXT | |
| balance | The current balance of the account. | BigDecimal | REAL | |
| include | Flag indicating if the account should be included in calculations. | Boolean | INTEGER | |
| canExpense | Flag indicating if the account can be used for expenses. | Boolean | INTEGER | |
| canIncome | Flag indicating if the account can be used for income. | Boolean | INTEGER | |
| canTransferFrom | Flag indicating if transfers can be made from this account. | Boolean | INTEGER | |
| canTransferTo | Flag indicating if transfers can be made to this account. | Boolean | INTEGER | |
| currencyCode | The currency code for the account. | String | TEXT | |
| initialBalance | The initial balance of the account. | BigDecimal | REAL | |
| creditLimit | The credit limit for the account. | BigDecimal | REAL | |
| billDay | The day of the month the bill is due. | Integer | INTEGER | |
| apr | The annual percentage rate. | BigDecimal | REAL | |
| sort | The sort order of the account. | Integer | INTEGER | |

## Table: t_user_balance_flow

This table stores the balance flow information, representing transactions.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the balance flow. | Integer | INTEGER | Primary Key |
| book_id | The ID of the book this flow belongs to. | Integer | INTEGER | Foreign Key |
| type | The type of flow (e.g., expense, income, transfer). | Integer | INTEGER | |
| amount | The amount of the transaction. | BigDecimal | REAL | |
| convertedAmount | The converted amount of the transaction. | BigDecimal | REAL | |
| account_id | The ID of the account associated with this flow. | Integer | INTEGER | Foreign Key |
| createTime | The timestamp when the flow was created. | Long | INTEGER | |
| title | The title of the transaction. | String | TEXT | |
| notes | Additional notes about the transaction. | String | TEXT | |
| creator_id | The ID of the user who created this flow. | Integer | INTEGER | Foreign Key |
| group_id | The ID of the group this flow belongs to. | Integer | INTEGER | Foreign Key |
| to_id | The ID of the destination account for transfers. | Integer | INTEGER | Foreign Key |
| payee_id | The ID of the payee. | Integer | INTEGER | Foreign Key |
| confirm | Flag indicating if the transaction is confirmed. | Boolean | INTEGER | |
| include | Flag indicating if the transaction should be included in calculations. | Boolean | INTEGER | |
| insertAt | The timestamp when the record was inserted. | Long | INTEGER | |

## Table: t_user_book

This table stores user-created books for managing finances.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the book. | Integer | INTEGER | Primary Key |
| name | The name of the book. | String | TEXT | |
| group_id | The ID of the group this book belongs to. | Integer | INTEGER | Foreign Key |
| notes | Additional notes about the book. | String | TEXT | |
| enable | Flag indicating if the book is active. | Boolean | INTEGER | |
| defaultExpenseAccount_id | The ID of the default expense account. | Integer | INTEGER | Foreign Key |
| defaultIncomeAccount_id | The ID of the default income account. | Integer | INTEGER | Foreign Key |
| defaultTransferFromAccount_id | The ID of the default transfer-from account. | Integer | INTEGER | Foreign Key |
| defaultTransferToAccount_id | The ID of the default transfer-to account. | Integer | INTEGER | Foreign Key |
| defaultExpenseCategory_id | The ID of the default expense category. | Integer | INTEGER | Foreign Key |
| defaultIncomeCategory_id | The ID of the default income category. | Integer | INTEGER | Foreign Key |
| defaultCurrencyCode | The default currency code for the book. | String | TEXT | |
| exportAt | The timestamp of the last export. | Long | INTEGER | |
| sort | The sort order of the book. | Integer | INTEGER | |

## Table: t_user_category

This table stores categories for classifying transactions.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the category. | Integer | INTEGER | Primary Key |
| name | The name of the category. | String | TEXT | |
| parent_id | The ID of the parent category for creating a hierarchy. | Integer | INTEGER | Foreign Key |
| book_id | The ID of the book this category belongs to. | Integer | INTEGER | Foreign Key |
| notes | Additional notes about the category. | String | TEXT | |
| enable | Flag indicating if the category is active. | Boolean | INTEGER | |
| type | The type of category (e.g., expense, income). | Integer | INTEGER | |
| sort | The sort order of the category. | Integer | INTEGER | |

## Table: t_user_category_relation

This table links categories to balance flows.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the relation. | Integer | INTEGER | Primary Key |
| category_id | The ID of the category. | Integer | INTEGER | Foreign Key |
| balanceFlow_id | The ID of the balance flow. | Integer | INTEGER | Foreign Key |
| amount | The amount associated with this category for the transaction. | BigDecimal | REAL | |
| convertedAmount | The converted amount. | BigDecimal | REAL | |

## Table: t_flow_file

This table stores files associated with balance flows.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the file. | Integer | INTEGER | Primary Key |
| data | The binary data of the file. | byte[] | BLOB | |
| creator_id | The ID of the user who uploaded the file. | Integer | INTEGER | Foreign Key |
| flow_id | The ID of the balance flow this file is associated with. | Integer | INTEGER | Foreign Key |
| createTime | The timestamp when the file was uploaded. | Long | INTEGER | |
| contentType | The content type of the file. | String | TEXT | |
| size | The size of the file in bytes. | Long | INTEGER | |
| originalName | The original name of the file. | String | TEXT | |

## Table: t_user_payee

This table stores payee information.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the payee. | Integer | INTEGER | Primary Key |
| name | The name of the payee. | String | TEXT | |
| book_id | The ID of the book this payee belongs to. | Integer | INTEGER | Foreign Key |
| notes | Additional notes about the payee. | String | TEXT | |
| enable | Flag indicating if the payee is active. | Boolean | INTEGER | |
| canExpense | Flag indicating if the payee can be used for expenses. | Boolean | INTEGER | |
| canIncome | Flag indicating if the payee can be used for income. | Boolean | INTEGER | |
| sort | The sort order of the payee. | Integer | INTEGER | |

## Table: t_user_tag

This table stores tags for classifying transactions.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the tag. | Integer | INTEGER | Primary Key |
| name | The name of the tag. | String | TEXT | |
| parent_id | The ID of the parent tag for creating a hierarchy. | Integer | INTEGER | Foreign Key |
| book_id | The ID of the book this tag belongs to. | Integer | INTEGER | Foreign Key |
| notes | Additional notes about the tag. | String | TEXT | |
| enable | Flag indicating if the tag is active. | Boolean | INTEGER | |
| canExpense | Flag indicating if the tag can be used for expenses. | Boolean | INTEGER | |
| canIncome | Flag indicating if the tag can be used for income. | Boolean | INTEGER | |
| canTransfer | Flag indicating if the tag can be used for transfers. | Boolean | INTEGER | |
| sort | The sort order of the tag. | Integer | INTEGER | |

## Table: t_user_tag_relation

This table links tags to balance flows.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the relation. | Integer | INTEGER | Primary Key |
| tag_id | The ID of the tag. | Integer | INTEGER | Foreign Key |
| balanceFlow_id | The ID of the balance flow. | Integer | INTEGER | Foreign Key |
| amount | The amount associated with this tag for the transaction. | BigDecimal | REAL | |
| convertedAmount | The converted amount. | BigDecimal | REAL | |

## Table: t_user_user

This table stores user information.

| Name | Description | Current Data Type | SQLite Data Type | Key Type |
|---|---|---|---|---|
| id | The unique identifier for the user. | Integer | INTEGER | Primary Key |
| username | The username of the user. | String | TEXT | |
| nickName | The nickname of the user. | String | TEXT | |
| password | The hashed password of the user. | String | TEXT | |
| telephone | The telephone number of the user. | String | TEXT | |
| email | The email address of the user. | String | TEXT | |
| registerIp | The IP address used for registration. | String | TEXT | |
| defaultGroup_id | The ID of the user's default group. | Integer | INTEGER | Foreign Key |
| defaultBook_id | The ID of the user's default book. | Integer | INTEGER | Foreign Key |
| enable | Flag indicating if the user account is active. | Boolean | INTEGER | |
| registerTime | The timestamp of user registration. | Long | INTEGER | |
| headimgurl | The URL of the user's profile picture. | String | TEXT | |
