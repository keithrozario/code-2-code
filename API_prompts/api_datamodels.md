
Of course. Here is a detailed breakdown of the database schema based on my analysis of the JPA entities in the repository.

### `t_user_account`

This table stores information about user accounts.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the account. |
| `name` | VARCHAR(255) | NOT NULL | The name of the account. |
| `group_id` | Integer | FOREIGN KEY to `t_user_group(id)` | The group this account belongs to. |
| `type` | Integer | NOT NULL | The type of account (1: Debit, 2: Credit, 3: Loan, 4: Asset). |
| `notes` | VARCHAR(1024) | | Notes for the account. |
| `enable` | Boolean | NOT NULL | Whether the account is enabled. |
| `no` | VARCHAR(32) | | The account number. |
| `balance` | BigDecimal | NOT NULL | The current balance of the account. |
| `include` | Boolean | NOT NULL | Whether to include this account in the total balance. |
| `can_expense` | Boolean | NOT NULL | Whether this account can be used for expenses. |
| `can_income` | Boolean | NOT NULL | Whether this account can be used for income. |
| `can_transfer_from` | Boolean | NOT NULL | Whether this account can be used as a source for transfers. |
| `can_transfer_to` | Boolean | NOT NULL | Whether this account can be used as a destination for transfers. |
| `currency_code` | VARCHAR(8) | NOT NULL | The currency code for the account. |
| `initial_balance` | BigDecimal | | The initial balance of the account. |
| `credit_limit` | BigDecimal | | The credit limit for the account. |
| `bill_day` | Integer | | The day of the month when the bill is generated. |
| `apr` | BigDecimal(4,4) | | The annual percentage rate for the account. |
| `ranking` | Integer | | The sort order of the account. |

### `t_user_balance_flow`

This table records all financial transactions (balance flows).

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the balance flow. |
| `book_id` | Integer | FOREIGN KEY to `t_user_book(id)`, NOT NULL | The book this balance flow belongs to. |
| `type` | Integer | NOT NULL | The type of flow (1: Expense, 2: Income, 3: Transfer, 4: Adjust Balance). |
| `amount` | BigDecimal | NOT NULL | The amount of the flow. |
| `converted_amount` | BigDecimal | | The converted amount of the flow. |
| `account_id` | Integer | FOREIGN KEY to `t_user_account(id)` | The account associated with the flow. |
| `create_time` | Long | NOT NULL | The creation time of the flow. |
| `title` | VARCHAR(32) | | The title of the flow. |
| `notes` | VARCHAR(1024) | | Notes for the flow. |
| `creator_id` | Integer | FOREIGN KEY to `t_user_user(id)`, NOT NULL | The user who created the flow. |
| `group_id` | Integer | FOREIGN KEY to `t_user_group(id)`, NOT NULL | The group this flow belongs to. |
| `to_id` | Integer | FOREIGN KEY to `t_user_account(id)` | The destination account for transfers. |
| `payee_id` | Integer | FOREIGN KEY to `t_user_payee(id)` | The payee of the flow. |
| `confirm` | Boolean | NOT NULL | Whether the flow is confirmed. |
| `include` | Boolean | | Whether to include this flow in calculations. |
| `insert_at` | Long | NOT NULL | The insertion time of the flow. |

### `t_user_book`

This table represents a collection of accounts, categories, etc., forming a "book" for financial records.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the book. |
| `name` | VARCHAR(255) | NOT NULL | The name of the book. |
| `group_id` | Integer | FOREIGN KEY to `t_user_group(id)`, NOT NULL | The group this book belongs to. |
| `notes` | VARCHAR(1024) | | Notes for the book. |
| `enable` | Boolean | NOT NULL | Whether the book is enabled. |
| `default_expense_account_id` | Integer | FOREIGN KEY to `t_user_account(id)` | The default expense account for the book. |
| `default_income_account_id` | Integer | FOREIGN KEY to `t_user_account(id)` | The default income account for the book. |
| `default_transfer_from_account_id` | Integer | FOREIGN KEY to `t_user_account(id)` | The default transfer from account for the book. |
| `default_transfer_to_account_id` | Integer | FOREIGN KEY to `t_user_account(id)` | The default transfer to account for the book. |
| `default_expense_category_id` | Integer | FOREIGN KEY to `t_user_category(id)` | The default expense category for the book. |
| `default_income_category_id` | Integer | FOREIGN KEY to `t_user_category(id)` | The default income category for the book. |
| `default_currency_code` | VARCHAR(8) | NOT NULL | The default currency code for the book. |
| `export_at` | Long | | The last export time. |
| `ranking` | Integer | | The sort order of the book. |

### `t_user_category`

This table defines categories for income and expenses.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the category. |
| `name` | VARCHAR(255) | NOT NULL | The name of the category. |
| `book_id` | Integer | FOREIGN KEY to `t_user_book(id)`, NOT NULL | The book this category belongs to. |
| `notes` | VARCHAR(4096) | | Notes for the category. |
| `enable` | Boolean | NOT NULL | Whether the category is enabled. |
| `type` | Integer | NOT NULL | The type of category (100: Expense, 200: Income). |
| `parent_id` | Integer | FOREIGN KEY to `t_user_category(id)` | The parent category. |
| `level` | Integer | | The level of the category in the hierarchy. |
| `ranking` | Integer | | The sort order of the category. |

### `t_user_category_relation`

This table links balance flows to categories.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the category relation. |
| `category_id` | Integer | FOREIGN KEY to `t_user_category(id)`, NOT NULL | The category. |
| `balance_flow_id` | Integer | FOREIGN KEY to `t_user_balance_flow(id)`, NOT NULL | The balance flow. |
| `amount` | BigDecimal | NOT NULL | The amount. |
| `converted_amount` | BigDecimal | | The converted amount. |

### `t_flow_file`

This table stores files associated with balance flows.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the flow file. |
| `data` | LONGBLOB | NOT NULL | The file data. |
| `user_id` | Integer | FOREIGN KEY to `t_user_user(id)`, NOT NULL | The user who uploaded the file. |
| `flow_id` | Integer | FOREIGN KEY to `t_user_balance_flow(id)` | The balance flow this file is associated with. |
| `create_time` | Long | NOT NULL | The creation time of the file. |
| `content_type` | VARCHAR(32) | NOT NULL | The content type of the file. |
| `size` | Long | NOT NULL | The size of the file. |
| `original_name` | VARCHAR(512) | NOT NULL | The original name of the file. |

### `t_user_group`

This table defines groups of users who can share books.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the group. |
| `name` | VARCHAR(255) | NOT NULL | The name of the group. |
| `notes` | VARCHAR(1024) | | Notes for the group. |
| `enable` | Boolean | NOT NULL | Whether the group is enabled. |
| `creator_id` | Integer | FOREIGN KEY to `t_user_user(id)` | The user who created the group. |
| `default_book_id` | Integer | FOREIGN KEY to `t_user_book(id)` | The default book for the group. |
| `default_currency_code` | VARCHAR(8) | NOT NULL | The default currency code for the group. |

### `t_user_note_day`

This table is for daily notes or reminders.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the note day. |
| `user_id` | Integer | FOREIGN KEY to `t_user_user(id)`, NOT NULL | The user this note day belongs to. |
| `title` | VARCHAR(16) | NOT NULL | The title of the note day. |
| `notes` | VARCHAR(1024) | | Notes for the note day. |
| `start_date` | Long | NOT NULL | The start date. |
| `end_date` | Long | NOT NULL | The end date. |
| `next_date` | Long | | The next execution date. |
| `repeat_type` | Integer | NOT NULL | The repeat type (0: Once, 1: Daily, 2: Monthly, 3: Yearly). |
| `c_interval` | Integer | | The interval. |
| `total_count` | Integer | NOT NULL | The total number of executions. |
| `run_count` | Integer | NOT NULL | The number of executions that have already run. |

### `t_user_payee`

This table stores information about payees.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the payee. |
| `name` | VARCHAR(255) | NOT NULL | The name of the payee. |
| `book_id` | Integer | FOREIGN KEY to `t_user_book(id)`, NOT NULL | The book this payee belongs to. |
| `notes` | VARCHAR(1024) | | Notes for the payee. |
| `enable` | Boolean | NOT NULL | Whether the payee is enabled. |
| `can_expense` | Boolean | NOT NULL | Whether the payee can be used for expenses. |
| `can_income` | Boolean | NOT NULL | Whether the payee can be used for income. |
| `ranking` | Integer | | The sort order of the payee. |

### `t_user_tag`

This table defines tags that can be applied to transactions.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the tag. |
| `name` | VARCHAR(255) | NOT NULL | The name of the tag. |
| `book_id` | Integer | FOREIGN KEY to `t_user_book(id)`, NOT NULL | The book this tag belongs to. |
| `notes` | VARCHAR(4096) | | Notes for the tag. |
| `enable` | Boolean | NOT NULL | Whether the tag is enabled. |
| `can_expense` | Boolean | NOT NULL | Whether the tag can be used for expenses. |
| `can_income` | Boolean | NOT NULL | Whether the tag can be used for income. |
| `can_transfer` | Boolean | NOT NULL | Whether the tag can be used for transfers. |
| `parent_id` | Integer | FOREIGN KEY to `t_user_tag(id)` | The parent tag. |
| `level` | Integer | | The level of the tag in the hierarchy. |
| `ranking` | Integer | | The sort order of the tag. |

### `t_user_tag_relation`

This table links balance flows to tags.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the tag relation. |
| `tag_id` | Integer | FOREIGN KEY to `t_user_tag(id)`, NOT NULL | The tag. |
| `balance_flow_id` | Integer | FOREIGN KEY to `t_user_balance_flow(id)`, NOT NULL | The balance flow. |
| `amount` | BigDecimal | NOT NULL | The amount. |
| `converted_amount` | BigDecimal | | The converted amount. |

### `t_user_user`

This table stores user information.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the user. |
| `username` | VARCHAR(16) | UNIQUE | The username. |
| `nick_name` | VARCHAR(16) | | The nickname of the user. |
| `password` | VARCHAR(64) | | The password of the user. |
| `telephone` | VARCHAR(16) | | The telephone number of the user. |
| `email` | VARCHAR(32) | | The email of the user. |
| `register_ip` | VARCHAR(128) | | The IP address used for registration. |
| `default_group_id` | Integer | FOREIGN KEY to `t_user_group(id)` | The default group for the user. |
| `default_book_id` | Integer | FOREIGN KEY to `t_user_book(id)` | The default book for the user. |
| `enable` | Boolean | NOT NULL | Whether the user is enabled. |
| `register_time` | Long | | The registration time of the user. |
| `headimgurl` | VARCHAR(256) | | The URL of the user's head image. |

### `t_user_user_group_relation`

This table manages the relationship between users and groups, including their roles.

| Column Name | Data Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | PRIMARY KEY | The unique identifier for the user-group relation. |
| `user_id` | Integer | FOREIGN KEY to `t_user_user(id)`, NOT NULL | The user. |
| `group_id` | Integer | FOREIGN KEY to `t_user_group(id)`, NOT NULL | The group. |
| `role` | Integer | NOT NULL | The role of the user in the group (1: Owner, 2: Maintainer, 3: Guest, 4: Invited). |
| | | UNIQUE (`user_id`, `group_id`) | |
