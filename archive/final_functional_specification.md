# Functional Specification: MoneyNote API

## 1. Introduction

### 1.1 Purpose of the Document

This document provides a detailed functional specification for the MoneyNote API, a comprehensive personal and small business bookkeeping system. Its purpose is to establish a clear and common understanding of the system's features, behaviors, and capabilities among all stakeholders, including developers, quality assurance teams, and project managers. This specification will serve as the definitive guide for the development, testing, and future enhancement of the application, ensuring that the final product aligns with the intended business requirements and user needs.

### 1.2 Goals and Objectives

The primary goal of the MoneyNote system is to provide users with a secure, private, and powerful platform for independent financial management. It empowers users to take full control of their financial data without relying on third-party services.

The key objectives are:

*   **Provide Comprehensive Financial Tracking:** To enable users to meticulously track all financial activities, including incomes, expenses, transfers, and account balance adjustments.
*   **Deliver Actionable Financial Insights:** To offer robust reporting and overview features that give users a clear, consolidated understanding of their financial health, including net worth, asset distribution, and spending patterns.
*   **Support Complex Use Cases:** To provide advanced features such as multi-book accounting for segregating finances (e.g., personal vs. business) and multi-currency support for managing international transactions seamlessly.
*   **Ensure Data Integrity and Privacy:** To build a self-hostable solution that prioritizes user data ownership and provides features for complete and verifiable record-keeping, such as file attachments for transactions.
*   **Facilitate Collaboration:** To allow multiple users to collaborate on shared financial accounts and books through a secure group and role-based access control system.

### 1.3 Scope

This document defines the functional scope of the MoneyNote API backend.

#### 1.3.1 In Scope

The following features and functionalities are within the scope of this specification:

*   **Financial Monitoring:** Calculation and reporting of total assets, debts, and net worth. Visual reporting on the composition of assets and liabilities.
*   **Transaction Management:** Full CRUD (Create, Read, Update, Delete) operations for financial transactions, including expenses, incomes, transfers, and balance adjustments.
*   **Data Classification:** Hierarchical categorization and tagging of transactions for granular analysis.
*   **Multi-Book Accounting:** Creation and management of multiple, independent financial ledgers ("Books"), each with its own set of categories, tags, and payees.
*   **Multi-Currency Support:**
    *   Assignment of specific currencies to financial accounts.
    *   Handling of transactions involving different currencies, including the storage of original and converted amounts.
    *   Consolidated reporting in a single, user-defined default currency.
*   **File Attachments:** Uploading, viewing, and deleting files (e.g., receipts, invoices) associated with specific transactions.
*   **User and Group Management:** User registration, authentication, and the ability to manage collaborative groups with different user roles.

#### 1.3.2 Out of Scope

The following functionalities are considered out of scope for this version of the specification:

*   **Direct Bank Synchronization:** The system does not automatically import transaction data from financial institutions. All data entry is manual.
*   **Automated Budgeting and Forecasting:** The system provides reporting on past activity but does not include features for creating budgets, setting spending goals, or forecasting future financial states.
*   **Investment Portfolio Management:** The system can track the balance of an investment account as a simple asset but does not manage individual stocks, bonds, or performance tracking.
*   **Client Applications:** This document specifies the API backend only. The design and implementation of any web, mobile, or desktop client applications are not covered.
*   **Advanced Tax Preparation:** The system does not generate tax forms or provide features specifically for tax compliance.
## Key Data Entities 

The application's data model revolves around several core entities that represent users, their financial structure, and their transactions.

| Entity | Purpose | Key Relationships |
| :--- | :--- | :--- |
| **User** | Represents an application user, holding their credentials and default preferences. | - Has a default `Group` and `Book`.<br>- Linked to multiple `Group`s via `UserGroupRelation`. |
| **Group** | A container for collaborative bookkeeping, enabling multiple users to share financial data. | - Created by a `User`.<br>- Contains `Book`s and `Account`s.<br>- Manages user roles and permissions via `UserGroupRelation`. |
| **Book** | A ledger for recording transactions. Each book has its own set of categories, tags, and payees. | - Belongs to a `Group`.<br>- Contains `Category`, `Tag`, and `Payee` entities.<br>- Is the primary scope for `BalanceFlow` entries. |
| **Account** | Represents a real-world financial account (e.g., bank account, credit card, asset). | - Belongs to a `Group`.<br>- Holds a `balance` and has attributes defining its capabilities (e.g., `canExpense`, `canIncome`).<br>- Is the source or destination for `BalanceFlow` transactions. |
| **BalanceFlow** | The central transaction entity, recording all financial movements like expenses, incomes, transfers, and adjustments. | - Belongs to a `Book` and `Group`.<br>- Links to `Account`(s), `Category`(ies), `Tag`(s), `Payee`, and `FlowFile`(s). |
| **Category, Tag** | Hierarchical entities used to classify and organize transactions. Both extend `TreeEntity` to support parent-child relationships. | - Belong to a `Book`.<br>- Linked to `BalanceFlow` via `CategoryRelation` and `TagRelation`. |
| **Payee** | Represents the other party in a transaction (e.g., a store, a person). | - Belongs to a `Book`.<br>- Can be associated with an `EXPENSE` or `INCOME` type `BalanceFlow`. |

[^1]: build.gradle: `querydsl-jpa` - Dependency for using QueryDSL for type-safe database queries.
[^2]: src/main/resources/application.properties: `spring.datasource.url` - Defines the JDBC connection string for the MySQL database.
[^3]: src/main/java/cn/biq/mn/SqlScriptRunner.java: `run` - Executes the `1.sql` script at application startup to handle manual database migrations.
[^4]: src/main/resources/hibernate.properties: `hibernate.dialect.storage_engine=myisam` - Specifies MyISAM as the desired storage engine for Hibernate.
[^5]: notes/data_backup.txt: `要把存储引擎改为 MyISAM。` - A note indicating a preference or requirement for the MyISAM storage engine.
[^6]: src/main/java/cn/biq/mn/flowfile/FlowFile.java: `data` - A `byte[]` field annotated with `@Lob` to store file data directly in the database.
[^7]: src/main/resources/application.properties: `spring.servlet.multipart.max-file-size=100MB` - Configuration property setting the maximum size for uploaded files.
[^8]: src/main/java/cn/biq/mn/bean/ApplicationScopeBean.java: `@ApplicationScope` - A Spring bean that holds application-wide data, acting as an in-memory cache.
[^9]: src/main/java/cn/biq/mn/currency/CurrencyDataLoader.java: `run` - Loads currency information from a JSON file into the `ApplicationScopeBean` on startup.
[^10]: src/main/java/cn/biq/mn/currency/CurrencyRemoteDataLoader.java: `run` - Refreshes currency exchange rates from a remote API after startup.
[^11]: src/main/java/cn/biq/mn/book/tpl/BookTplDataLoader.java: `run` - Loads book templates from a JSON file into the `ApplicationScopeBean` on startup.
[^12]: src/main/java/cn/biq/mn/report/ReportService.java: `reportCategory` - A method that aggregates financial data from `BalanceFlow` entities to generate reports.

### Data Model 

The application employs a relational data model to structure its bookkeeping data. Core entities are interconnected to represent users, groups, financial accounts, and transactions.

| Entity (Table Name) | Description | Key Relationships |
| :--- | :--- | :--- |
| `User` (`t_user_user`) | Represents an application user with credentials and personal information. | One-to-Many with `UserGroupRelation`. Has a default `Group` and `Book`. |
| `Group` (`t_user_group`) | A container for collaborative bookkeeping, allowing multiple users. | Many-to-One with `User` (creator). One-to-Many with `UserGroupRelation`. Has a default `Book`. |
| `UserGroupRelation` (`t_user_user_group_relation`) | A join table defining a `User`'s role within a `Group` (e.g., owner, operator). | Many-to-One with `User` and `Group`. |
| `Book` (`t_user_book`) | Represents a ledger or a set of books, belonging to a `Group`. | Many-to-One with `Group`. Holds default accounts and categories. One-to-Many with `Category`, `Tag`, and `Payee`. |
| `Account` (`t_user_account`) | Represents a financial account (e.g., checking, credit card), belonging to a `Group`. | Many-to-One with `Group`. Tracks `balance`, `creditLimit`, and other attributes. |
| `BalanceFlow` (`t_user_balance_flow`) | The central transaction entity, recording expenses, incomes, and transfers. | Many-to-One with `Book`, `Account` (from), `Account` (to), `Payee`, and `User` (creator). Links to categories and tags via relation tables. |
| `Category` (`t_user_category`) | A hierarchical structure (`TreeEntity`) for classifying transactions. Belongs to a `Book`. | Many-to-One with `Book`. Can have a parent `Category`. |
| `Tag` (`t_user_tag`) | A hierarchical structure (`TreeEntity`) for adding metadata to transactions. Belongs to a `Book`. | Many-to-One with `Book`. Can have a parent `Tag`. |
| `CategoryRelation` (`t_user_category_relation`) | Join table linking a `BalanceFlow` to a `Category` and storing the amount for that category. | Many-to-One with `Category` and `BalanceFlow`. |
| `TagRelation` (`t_user_tag_relation`) | Join table linking a `BalanceFlow` to a `Tag`. | Many-to-One with `Tag` and `BalanceFlow`. |
| `FlowFile` (`t_flow_file`) | Stores file attachments (e.g., receipts) for a `BalanceFlow` as a `LONGBLOB`. | Many-to-One with `BalanceFlow`. |
### Data Flow 

Data moves bidirectionally between the API layer and the MySQL database, facilitated by the service and repository layers.

| Source | Destination | Operation | Description |
| :--- | :--- | :--- | :--- |
| API: `POST /accounts` (`AccountController`) | Database: `t_user_account` table | **Write (Insert)** | A new account is created via the API. The `AccountService` maps the request form to an `Account` entity and persists it using `AccountRepository.save()` [^8]. |
| API: `GET /balance-flows` (`BalanceFlowController`) | API: `GET /balance-flows` | **Read** | Transaction data is queried from the `t_user_balance_flow` table via `BalanceFlowRepository.findAll()`. The service layer then maps the entities to `BalanceFlowDetails` DTOs for the API response, handling pagination [^9]. |
| API: `PATCH /balance-flows/{id}/confirm` (`BalanceFlowController`) | Database: `t_user_account`, `t_user_balance_flow` tables | **Read-Modify-Write** | Confirming a transaction reads the `BalanceFlow` and associated `Account` entities. It updates the account balance based on the flow type (e.g., expense, income) and saves the modified account. The `confirm` status of the `BalanceFlow` is also updated [^10]. |
| Code: `SqlScriptRunner` | Database: Multiple tables | **Write (Update/Alter)** | On application startup, the `SqlScriptRunner` executes the `1.sql` script to apply database schema changes and data migrations, ensuring the database aligns with the current application version [^6]. |
| Database: `t_user_category` and related tables | API: `GET /reports/expense-category` (`ReportController`) | **Read (Aggregate)** | The reporting endpoint triggers complex aggregations. The `ReportService` queries multiple tables, including `t_user_category_relation`, filters by various criteria, and calculates sums to generate category-based financial reports [^11]. |
# Journey 1: Monitoring Financial Situation

This document details the user journey for monitoring a user's overall financial health by using the system's overview and reporting features.

## 1. Detailed User Journey and Flows

This journey encompasses viewing high-level financial summaries and drilling down into detailed reports.

### Journey 1: Viewing Financial Overview

This is the user's primary entry point for understanding their financial position. It provides a snapshot of their net worth.

**User Flow:**
1.  The user logs into the application and lands on the main dashboard or "Overview" page.
2.  The system automatically fetches data from all of the user's financial accounts.
3.  The UI displays three key metrics:
    *   **Total Assets**: The sum of all money and assets the user owns.
    *   **Total Debts**: The sum of all money the user owes (e.g., credit card balances, loans).
    *   **Net Worth**: The result of Total Assets minus Total Debts.
4.  All values are presented in the user's default currency, regardless of the currency of the individual accounts.

### Journey 2: Analyzing Asset and Debt Composition

This flow allows the user to understand the breakdown of their assets and debts.

**User Flow:**
1.  From the overview page, the user examines visual charts (e.g., pie charts) that represent their assets and debts.
2.  The "Assets" chart shows how their total assets are distributed across different accounts (e.g., 60% in "Savings Account", 40% in "Investment Portfolio").
3.  The "Debts" chart shows a similar breakdown for liabilities (e.g., 70% on "Visa Credit Card", 30% on "Student Loan").
4.  This allows the user to quickly identify where their wealth is concentrated and which debts are the largest.

### Journey 3: Analyzing Spending and Income by Category

This flow enables the user to analyze their financial activities over a specific period.

**User Flow:**
1.  The user navigates to the "Reports" section.
2.  They select a report type, such as "Expense by Category".
3.  They specify a date range (e.g., "Last Month") and may filter by a specific book or account.
4.  The system generates a chart and a table showing the total amount spent in each category (e.g., "Food", "Transportation").
5.  The user can click on a category (e.g., "Food") to drill down and see a report of its sub-categories (e.g., "Groceries", "Restaurants").

## 2. Detailed Object-Level Data Structures

### `Account` Entity (`t_user_account` table)

Represents a single financial account.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `group` | `Group` | (FK) The group this account belongs to. |
| `type` | `AccountType` | Enum: `CHECKING`, `CREDIT`, `DEBT`, `ASSET`. |
| `name` | `String` | The name of the account. |
| `balance` | `BigDecimal` | The current balance of the account. |
| `currencyCode` | `String` | The currency of the account (e.g., "USD", "EUR"). |
| `include` | `Boolean` | If `true`, this account is included in net worth calculations. |
| `enable` | `Boolean` | If `true`, the account is active. |

### `ChartVO` Data Structure

This DTO is used to structure data for sending to the frontend for chart rendering.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `x` | `String` | The label for a data point (e.g., a category name like "Food"). |
| `y` | `BigDecimal` | The value for a data point (e.g., the total amount spent). |
| `percent` | `BigDecimal` | The percentage this data point represents out of the total. |

### `CategoryReportQueryForm` Data Structure

This DTO is used to pass filter criteria for generating category-based reports.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `book` | `Integer` | ID of the book to filter by. |
| `minTime` | `Long` | The start of the date range (timestamp). |
| `maxTime` | `Long` | The end of the date range (timestamp). |
| `accounts` | `Set<Integer>` | Set of account IDs to filter by. |
| `categories` | `Set<Integer>` | Set of category IDs to filter by (for drill-down). |

## 3. Database Tables to be Updated

This user journey is **read-only**. No database tables are updated when a user monitors their financial situation. The system only performs `SELECT` queries to fetch and aggregate data.

## 4. API Calls

The primary API endpoints for this journey are in `AccountController` and `ReportController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/accounts/overview` | Retrieves the three main financial overview metrics: total assets, total debts, and net worth. |
| `GET` | `/reports/balance` | Retrieves data structured for visualizing the breakdown of assets and debts by account. |
| `GET` | `/reports/expense-category` | Generates a report of expenses aggregated by category for a given period. |
| `GET` | `/reports/income-category` | Generates a report of income aggregated by category for a given period. |
| `GET` | `/reports/expense-tag` | Generates a report of expenses aggregated by tag. |
| `GET` | `/accounts` | Retrieves a filterable, paginated list of all financial accounts. |

## 5. Business Rules and Functionality

The core logic is handled by `AccountService` and `ReportService`.

-   **Net Worth Calculation**: The system strictly defines how assets and debts are calculated. The `AccountService.overview()` method orchestrates this by calling helper methods and performing currency conversion.

    ```java
    // In AccountService.java
    @Transactional(readOnly = true)
    public BigDecimal[] overview() {
        var result = new BigDecimal[3];
        Group group = sessionUtil.getCurrentGroup();
        List<Account> assetAccounts = getAssets();
        BigDecimal assetBalance = BigDecimal.ZERO;
        for (Account account : assetAccounts) {
            assetBalance = assetBalance.add(currencyService.convert(account.getBalance(), account.getCurrencyCode(), group.getDefaultCurrencyCode()));
        }
        result[0] = assetBalance;

        List<Account> debtAccounts = getDebts();
        BigDecimal debtBalance = BigDecimal.ZERO;
        for (Account account : debtAccounts) {
            debtBalance = debtBalance.add(currencyService.convert(account.getBalance(), account.getCurrencyCode(), group.getDefaultCurrencyCode()));
        }
        result[1] = debtBalance.negate();
        result[2] = result[0].subtract(result[1]);
        return result;
    }
    ```

-   **Asset and Debt Definition**: The system defines assets and debts based on the `AccountType` enum. Only accounts that are `enabled` and marked to be `included` are used in these calculations.

    ```java
    // In AccountService.java
    public List<Account> getAssets() {
        Group group = sessionUtil.getCurrentGroup();
        List<Account> assetAccounts = new ArrayList<>();
        assetAccounts.addAll(accountRepository.findAllByGroupAndTypeAndEnableAndInclude(group, AccountType.CHECKING, true, true));
        assetAccounts.addAll(accountRepository.findAllByGroupAndTypeAndEnableAndInclude(group, AccountType.ASSET, true, true));
        return assetAccounts;
    }
    ```

-   **Currency Conversion**: A crucial rule is that all financial aggregation **must** happen in a single, consistent currency. The `CurrencyService.convert()` method is used throughout the `AccountService` and `ReportService` to normalize all values to the user's group default currency before they are summed up.

-   **Report Aggregation**: The `ReportService` fetches raw transaction data (`CategoryRelation` records) based on filters and then processes it in-memory to build the hierarchical report structure. It calculates the total for each root category (including all its children) and then computes the percentage of the grand total.

    ```java
    // In ReportService.java (simplified logic)
    public List<ChartVO> reportCategory(CategoryReportQueryForm form, CategoryType type) {
        // ... fetch rootCategories and all relevant categoryRelations
        for (Category i : rootCategories) {
            ChartVO vo = new ChartVO();
            vo.setX(i.getName());
            List<Category> offSpringCategory = TreeUtils.getOffspring(i, categories);
            List<Integer> offSpringCategoryIds = offSpringCategory.stream().map(j->j.getId()).collect(Collectors.toList());
            offSpringCategoryIds.add(i.getId());
            // Sum up amounts for the category and all its descendants
            vo.setY(categoryRelations.stream().filter(j -> offSpringCategoryIds.contains(j.getCategory().getId())).map(CategoryRelation::getConvertedAmount).reduce(BigDecimal.ZERO, BigDecimal::add));
            result.add(vo);
        }
        // ... sort, calculate total, and compute percentages
        return result;
    }
    ```

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-MON-01** | User has one asset account (Checking, $1000 USD) and one debt account (Credit Card, -$500 USD). Group currency is USD. | `overview()` returns `[1000, 500, 500]`. (Assets: 1000, Debts: 500, Net Worth: 500). |
| **TC-MON-02** | User has two asset accounts: Checking ($1000 USD) and Savings (€500 EUR). Exchange rate is 1 EUR = 1.10 USD. Group currency is USD. | `overview()` returns `[1550, 0, 1550]`. (Assets: 1000 + (500*1.10) = 1550). |
| **TC-MON-03** | An asset account of $2000 has its `include` flag set to `false`. | The $2000 from this account is excluded from the Total Assets and Net Worth calculation. |
| **TC-MON-04** | Generate an expense report for a period with $100 spent on "Food" and $50 on "Transport". | `reportCategory()` returns a list of two `ChartVO` objects: {x:"Food", y:100, percent:66.67}, {x:"Transport", y:50, percent:33.33}. |
| **TC-MON-05** | Generate a balance report. User has one asset account (Checking, $1000) and one debt account (Credit Card, -$500). | `reportBalance()` returns two lists. The asset list contains one item for $1000. The debt list contains one item for $500 (value is negated to be positive for the report). |
| **TC-MON-06** | Filter the expense report to a specific account that has no expenses in the period. | The report returns an empty list. |

## 7. State any Assumptions

*   The user is authenticated and their session correctly holds their active `Group` and `Book` context.
*   The currency exchange rates are loaded and available in the `ApplicationScopeBean`. The accuracy of financial reports depends on the accuracy of these rates.
*   The user's group has a `defaultCurrencyCode` set, which is the basis for all conversions.
*   The frontend client is responsible for rendering the `ChartVO` data into visual charts (e.g., using a library like Chart.js or D3.js).
*   Debt account balances are stored as negative numbers in the database, and the reporting layer is responsible for negating them to positive values for display where appropriate (e.g., in the `overview` and `balance` reports).

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
# Journey 3: Managing Finance Record Files

This document details the user journey for attaching, viewing, and managing digital files (like receipts or invoices) associated with financial transactions.

## 1. Detailed User Journey and Flows

This journey focuses on the lifecycle of a file attachment linked to a `BalanceFlow` (transaction).

### Journey 1: Attaching a File to a Transaction

This is the primary flow where a user uploads a document and links it to an existing transaction record.

**User Flow:**
1.  The user is viewing the details of an existing transaction.
2.  They click an "Add Attachment" or "Upload File" button.
3.  A file picker dialog appears, allowing them to select a file from their local device.
4.  The user selects a file (e.g., `receipt.pdf`, `invoice.jpg`).
5.  The file is uploaded to the server.
6.  The UI updates to show the newly uploaded file in a list of attachments for that transaction.

### Journey 2: Viewing and Downloading an Attachment

This flow describes how a user accesses a previously uploaded file.

**User Flow:**
1.  The user is viewing the details of a transaction that has one or more files attached.
2.  They see a list of attachment filenames.
3.  The user clicks on the filename they wish to view.
4.  The system serves the file, which either opens in a new browser tab (for supported types like PDF and images) or downloads to the user's device.

### Journey 3: Deleting an Attachment

This flow allows a user to remove a file that was previously attached to a transaction.

**User Flow:**
1.  The user is viewing the list of attachments for a transaction.
2.  Next to each filename, there is a "Delete" or "Remove" icon/button.
3.  The user clicks the delete button for the file they want to remove.
4.  The system prompts for confirmation.
5.  Upon confirmation, the file is permanently deleted from the system, and the attachment list on the UI is updated.

## 2. Detailed Object-Level Data Structures

The core data structure for this journey is the `FlowFile` entity.

### `FlowFile` Entity (`t_flow_file` table)

This entity represents a single file attached to a transaction.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `data` | `byte[]` | The binary content of the file, stored as a `LONGBLOB`. |
| `creator` | `User` | (FK) The user who uploaded the file. |
| `flow` | `BalanceFlow` | (FK) The transaction this file is attached to. |
| `createTime` | `Long` | The timestamp (in milliseconds) when the file was uploaded. |
| `contentType` | `String` | The MIME type of the file (e.g., "application/pdf"). |
| `size` | `Long` | The size of the file in bytes. |
| `originalName` | `String` | The original filename on the user's device. |

### `FlowFileDetails` Data Structure

This DTO is used to send file metadata to the client, excluding the large binary `data`.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `createTime` | `Long` | Upload timestamp. |
| `contentType` | `String` | File MIME type. |
| `size` | `Long` | File size. |
| `originalName` | `String` | Original filename. |

### `FlowFileViewForm` Data Structure

This DTO is used for securely requesting a file's content.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | The ID of the file to view. |
| `createTime` | `Long` | The creation timestamp of the file, used as a security check. |

## 3. Database Tables to be Updated

-   **`t_flow_file`**:
    -   A new record is **inserted** when a file is uploaded.
    -   A record is **deleted** when a user removes an attachment.
    -   When a `BalanceFlow` record is deleted, all associated records in this table are also **deleted** (cascading delete).

## 4. API Calls

The interactions are handled by `BalanceFlowController` and `FlowFileController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/balance-flows/{id}/addFile` | Uploads a new file and attaches it to the `BalanceFlow` with the given `id`. |
| `GET` | `/balance-flows/{id}/files` | Retrieves a list of `FlowFileDetails` for a specific transaction. |
| `GET` | `/flow-files/view` | Securely serves the binary content of a file for viewing or downloading. |
| `DELETE` | `/flow-files/{id}` | Deletes a specific file attachment. |

## 5. Business Rules and Functionality

The logic is primarily managed by `BalanceFlowService` and `FlowFileService`.

-   **File Upload and Storage**: The `BalanceFlowService.addFile` method handles the `MultipartFile` upload. It reads the file's bytes and metadata, populates a `FlowFile` entity, and saves it to the database.

    ```java
    // In BalanceFlowService.java
    public FlowFileDetails addFile(Integer id, MultipartFile file) {
        FlowFile flowFile = new FlowFile();
        try {
            flowFile.setData(file.getBytes());
        } catch (IOException e) {
            throw new FailureMessageException("add.flow.file.fail");
        }
        flowFile.setCreator(sessionUtil.getCurrentUser());
        flowFile.setFlow(baseService.findFlowById(id));
        flowFile.setCreateTime(System.currentTimeMillis());
        flowFile.setSize(file.getSize());
        flowFile.setContentType(file.getContentType());
        flowFile.setOriginalName(file.getOriginalFilename());
        flowFileRepository.save(flowFile);
        return FlowFileMapper.toDetails(flowFile);
    }
    ```

-   **File Validation**: The system uses a custom validator (`@ValidFile`) that checks the content type of the uploaded file. Only specific MIME types are allowed.

    ```java
    // In FileValidator.java
    private boolean isSupportedContentType(String contentType) {
        return contentType.equals("application/pdf")
                || contentType.equals("image/png")
                || contentType.equals("image/jpg")
                || contentType.equals("image/jpeg");
    }
    ```

-   **File Size Limit**: The maximum allowed size for an uploaded file and the overall request is configured in `application.properties` to be 100MB.

    ```properties
    # In application.properties
    spring.servlet.multipart.max-request-size=100MB
    spring.servlet.multipart.max-file-size=100MB
    ```

-   **Secure Viewing**: To prevent unauthorized access or enumeration of files, the `/flow-files/view` endpoint requires both the file's `id` and its `createTime`. The service layer validates that both parameters match the record in the database before returning the file data.

    ```java
    // In FlowFileService.java
    public FlowFile getFile(FlowFileViewForm form) {
        FlowFile flowFile =  flowFileRepository.getReferenceById(form.getId());
        if (!flowFile.getCreateTime().equals(form.getCreateTime())) {
            throw new FailureMessageException();
        }
        return flowFile;
    }
    ```

-   **Cascading Deletes**: When a `BalanceFlow` transaction is deleted, the `BalanceFlowService.remove()` method explicitly deletes all associated `FlowFile` records to prevent orphaned files in the database.

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-FILE-01** | Upload a valid file (`.pdf`, 1MB) to an existing transaction. | The API returns a 200 OK with the file details. A new record is created in the `t_flow_file` table. |
| **TC-FILE-02** | Attempt to upload an unsupported file type (e.g., `.exe`, `.zip`). | The API should return a validation error (400 Bad Request). No file record is created. |
| **TC-FILE-03** | Attempt to upload a file larger than the 100MB limit. | The API should return an error indicating the file size exceeds the limit. No file is saved. |
| **TC-FILE-04** | Request to view a file with the correct `id` and `createTime`. | The API returns a 200 OK with the file's binary data and the correct `Content-Type` header. |
| **TC-FILE-05** | Request to view a file with a correct `id` but an incorrect `createTime`. | The API should return an error (e.g., 400 Bad Request or 404 Not Found) and not serve the file. |
| **TC-FILE-06** | Delete an existing file attachment. | The API returns a 200 OK. The corresponding record in `t_flow_file` is deleted. |
| **TC-FILE-07** | Delete a `BalanceFlow` transaction that has two file attachments. | The `BalanceFlow` record and both associated `FlowFile` records are deleted from the database. |

## 7. State any Assumptions

*   The user is authenticated and has the necessary permissions to view and modify the transaction they are attaching files to.
*   Storing file binaries directly in the database (`LONGBLOB`) is an accepted design decision, though it may have performance and scalability implications compared to storing files in a dedicated object store like S3 or Google Cloud Storage.
*   The 4-second `Thread.sleep(4000)` in the `BalanceFlowController.handleAddFile` method is assumed to be a temporary debugging or testing artifact and not an intentional business requirement.
*   The security model for file viewing (requiring `id` and `createTime`) is considered sufficient for the application's needs.

# Journey 4: Supporting Multiple Books

This document details the user journey for managing separate financial ledgers, called "Books," to segregate different areas of a user's financial life.

## 1. Detailed User Journey and Flows

This journey covers the creation, management, and use of multiple Books.

### Journey 1: Creating a New Book

A user can create a new Book in one of three ways to start a new, independent ledger.

**User Flow (From Scratch):**
1.  The user navigates to the "Manage Books" section.
2.  They select "Add Book" and choose to create a new, empty book.
3.  A form prompts for a **Name** and a **Default Currency**.
4.  The user fills in the details and saves. A new, blank Book is created.

**User Flow (From Template):**
1.  In the "Add Book" section, the user chooses "Create from Template".
2.  They are presented with a list of predefined templates (e.g., "Daily Life", "Restaurant Business").
3.  The user selects a template, provides a new **Name** for their book, and confirms.
4.  A new Book is created, pre-populated with all the categories, tags, and payees defined in the chosen template.

**User Flow (By Copying):**
1.  In the "Add Book" section, the user chooses "Copy Existing Book".
2.  They select one of their existing Books as a source.
3.  They provide a new **Name** for the copied book.
4.  A new Book is created with an identical structure (all categories, tags, and payees) as the source book, but with no transaction data.

### Journey 2: Switching Between Books

This flow describes how a user changes their active context from one Book to another.

**User Flow:**
1.  The user clicks on a dropdown menu or navigation element that lists all their available Books.
2.  They select the Book they wish to work with (e.g., switching from "Personal Finances" to "Business").
3.  The application reloads, and the entire view (dashboard, transaction lists, reports) is now scoped to the newly selected Book. All subsequent actions will be recorded in this active Book.

### Journey 3: Exporting Book Data

This flow allows a user to get a full data dump of a specific Book's transactions.

**User Flow:**
1.  The user navigates to the settings for a specific Book.
2.  They click the "Export" button.
3.  The system generates an Excel (`.xlsx`) file containing all the transaction data for that Book.
4.  The file is downloaded to the user's device.

## 2. Detailed Object-Level Data Structures

### `Book` Entity (`t_user_book` table)

Represents a single, self-contained financial ledger.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `group` | `Group` | (FK) The group this book belongs to. |
| `name` | `String` | The name of the book. |
| `notes` | `String` | Optional descriptive notes. |
| `enable` | `Boolean` | Flag to enable or disable the book. |
| `defaultExpenseAccount` | `Account` | (FK) Default account for new expenses. |
| `defaultIncomeAccount` | `Account` | (FK) Default account for new incomes. |
| `defaultTransferFromAccount` | `Account` | (FK) Default source account for new transfers. |
| `defaultTransferToAccount` | `Account` | (FK) Default destination account for new transfers. |
| `defaultExpenseCategory` | `Category` | (FK) Default category for new expenses. |
| `defaultIncomeCategory` | `Category` | (FK) Default category for new incomes. |
| `defaultCurrencyCode` | `String` | The default currency for reporting within this book. |
| `sort` | `Integer` | A number used for sorting the list of books. |
| `tags` | `List<Tag>` | (Relation) All tags belonging to this book. |
| `categories` | `List<Category>` | (Relation) All categories belonging to this book. |
| `payees` | `List<Payee>` | (Relation) All payees belonging to this book. |

### `BookAddForm` Data Structure

DTO for creating a new Book from scratch.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `name` | `String` | The name for the new book. |
| `defaultCurrencyCode` | `String` | The default currency for the new book. |
| `notes` | `String` | Optional notes. |
| `sort` | `Integer` | Optional sort order. |

### `BookAddByTemplateForm` Data Structure

DTO for creating a new Book from a template.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `templateId` | `Integer` | The ID of the `BookTemplate` to use. |
| `book` | `BookAddForm` | The basic details (name, currency) for the new book. |

### `BookAddByBookForm` Data Structure

DTO for creating a new Book by copying an existing one.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `bookId` | `Integer` | The ID of the source Book to copy from. |
| `book` | `BookAddForm` | The basic details (name, currency) for the new book. |

## 3. Database Tables to be Updated

-   **`t_user_book`**: A new record is **inserted** when any new book is created. Records are **updated** when a book's details are changed, and **deleted** when a book is removed.
-   **`t_user_category`**: Records are **inserted** when a book is created from a template or by copying.
-   **`t_user_tag`**: Records are **inserted** when a book is created from a template or by copying.
-   **`t_user_payee`**: Records are **inserted** when a book is created from a template or by copying.
-   **`t_user_user`**: The `default_book_id` column is **updated** when a user changes their active book.

## 4. API Calls

The primary API endpoints for this journey are in `BookController` and `UserController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/books` | Creates a new, empty book from scratch. |
| `POST` | `/books/template` | Creates a new book from a predefined template. |
| `POST` | `/books/copy` | Creates a new book by copying an existing book's structure. |
| `GET` | `/books` | Retrieves a paginated list of all books for the current user's group. |
| `GET` | `/books/all` | Retrieves a non-paginated list of all enabled books (for dropdowns). |
| `PUT` | `/books/{id}` | Updates the details of a specific book. |
| `DELETE` | `/books/{id}` | Deletes a book. |
| `PATCH` | `/users/setDefaultBook/{id}` | Sets the specified book as the user's active book for the session. |
| `GET` | `/books/{id}/export` | Exports all transaction data for a specific book to an Excel file. |

## 5. Business Rules and Functionality

The core logic is handled by `BookService`.

-   **Data Isolation**: The `Book` is the primary container for financial data. `Category`, `Tag`, and `Payee` entities have a direct, non-nullable relationship to a `Book`, ensuring that data from one book does not leak into another.

-   **Creation from Template**: The `addByTemplate` method loads a `BookTemplate` object from a list that was initialized at startup from `book_tpl.json`. It then recursively traverses the template's categories and tags to create new database entities for the new book.

    ```java
    // In BookService.java
    public boolean addByTemplate(BookAddByTemplateForm form) {
        // ... find bookTemplate from a list loaded at startup
        Book book = add(form.getBook());
        setBookByBookTemplate(bookTemplate, group, book);
        // ... 
    }

    public void setBookByBookTemplate(BookTemplate bookTemplate, Group group, Book book) {
        // ... saves book details
        saveTag(TreeUtils.buildTree(bookTemplate.getTags()), book);
        saveCategory(TreeUtils.buildTree(bookTemplate.getCategories()), book);
        // ... saves payees
    }
    ```

-   **Creation by Copying**: The `addByBook` method works similarly. It first creates the new book, then fetches all categories, tags, and payees from the source book and creates new entities for the destination book.

    ```java
    // In BookService.java
    public boolean addByBook(BookAddByBookForm form) {
        Book book = add(form.getBook());
        Book bookSrc = baseService.getBookInGroup(form.getBookId());
        // ... copy tags, categories, and payees from bookSrc to book
        return true;
    }
    ```

-   **Deletion Constraint**: A book cannot be deleted if it has any associated `BalanceFlow` (transaction) records. This is a critical data integrity rule to prevent orphaned transactions and accidental data loss.

    ```java
    // In BookService.java
    public boolean remove(Integer id) {
        Book entity = baseService.getBookInGroup(id);
        if (balanceFlowRepository.existsByBook(entity)) {
            throw new FailureMessageException("book.delete.has.flow");
        }
        // ... proceed with deletion of book and its categories, etc.
        return true;
    }
    ```

-   **Switching Active Book**: When a user sets a new default book via the `/users/setDefaultBook/{id}` endpoint, the `UserService` updates the `defaultBook` foreign key on the `User` entity and also updates the book object stored in the current session.

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-BOOK-01** | Create a new book from scratch named "Test Book". | A new record is created in `t_user_book`. The book has no categories, tags, or payees. |
| **TC-BOOK-02** | Create a new book from the "Daily Life" template. | A new book is created. It is populated with all the categories and tags defined in the "Daily Life" template in `book_tpl.json`. |
| **TC-BOOK-03** | Create a new book by copying an existing book "Book A" which has 10 categories. | A new book is created. It has its own 10 category records that are identical in name and structure to those in "Book A". |
| **TC-BOOK-04** | Attempt to delete a book that has at least one transaction record. | The API should return an error with the message "book.delete.has.flow". The book should not be deleted. |
| **TC-BOOK-05** | Delete an empty book (no transactions). | The API should return a success response. The book and all its associated categories, tags, and payees are deleted from the database. |
| **TC-BOOK-06** | User's active book is "Book A". User calls the API to set "Book B" as the default. | The `default_book_id` on the user's record in `t_user_user` is updated to the ID of "Book B". Subsequent API calls are scoped to "Book B". |
| **TC-BOOK-07** | Attempt to create a book with a name that already exists within the same group. | The API should return an `ItemExistsException`. |

## 7. State any Assumptions

*   The user is authenticated and has a valid session, which provides the necessary `Group` context for all operations.
*   The `book_tpl.json` file is present in the application's resources, is well-formed, and is successfully loaded into the `ApplicationScopeBean` at startup.
*   The frontend is responsible for managing the user's active book context and sending the correct book ID in transaction-related API calls.
*   When a book is created, it is associated with the user's currently active `Group`.

# Journey 5: Supporting Multiple Currencies

This document details the user journey for managing accounts and transactions in multiple currencies, and how the system provides consolidated reporting.

## 1. Detailed User Journey and Flows

This journey enables users who deal with foreign currencies to track their finances accurately.

### Journey 1: Setting Up a Foreign Currency Account

Before recording foreign currency transactions, the user must set up an account with the correct currency.

**User Flow:**
1.  The user navigates to the "Accounts" section and clicks "Add Account".
2.  In the account creation form, they provide a name (e.g., "European Bank Account").
3.  They select a **Currency** from a dropdown list of world currencies (e.g., "EUR").
4.  They fill in the other account details and save. The account is now ready to be used for EUR transactions.

### Journey 2: Recording an Expense/Income in a Foreign Currency

This flow covers recording a transaction in an account whose currency is different from the Book's default currency.

**User Flow:**
1.  The user initiates a new "Expense" transaction.
2.  They select their foreign currency account (e.g., "European Bank Account (EUR)").
3.  They enter the transaction details, including the amount in the foreign currency (e.g., €50 for dinner).
4.  The system detects that the account's currency (EUR) is different from the Book's default currency (e.g., USD).
5.  The UI presents an additional field, **Converted Amount**, often pre-filled with a calculated estimate based on the system's current exchange rate. The user can adjust this value to match their bank statement exactly.
6.  The user saves the transaction. The balance of the EUR account is debited by €50, and the system stores both the original amount (€50) and the converted amount (e.g., $54.50) for reporting.

### Journey 3: Transferring Funds Between Different Currencies

This flow covers moving money between two accounts with different currencies.

**User Flow:**
1.  The user initiates a new "Transfer" transaction.
2.  For the "From Account", they select their local currency account (e.g., "US Checking (USD)").
3.  For the "To Account", they select their foreign currency account (e.g., "European Bank Account (EUR)").
4.  They enter the **Amount** to be sent from the source account (e.g., $1000).
5.  A mandatory **Converted Amount** field appears, prompting the user to enter the final amount that was received in the destination account (e.g., €920), as per their bank's transaction record.
6.  The user saves the transfer. The system debits $1000 from the USD account and credits €920 to the EUR account.

## 2. Detailed Object-Level Data Structures

### `Account` Entity (`t_user_account` table)

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `currencyCode` | `String` | A string (e.g., "USD", "EUR") representing the currency of this account. It is mandatory. |

### `Book` Entity (`t_user_book` table)

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `defaultCurrencyCode` | `String` | The base currency for all reporting within this Book. It is mandatory. |

### `BalanceFlow` Entity (`t_user_balance_flow` table)

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `amount` | `BigDecimal` | The amount of the transaction in the original currency of the source account. |
| `convertedAmount` | `BigDecimal` | The equivalent amount in the Book's default currency. For cross-currency transfers, it's the amount in the destination account's currency. |

### `CurrencyDetails` Data Structure

This DTO, loaded from `currency.json`, holds the information for each currency.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | An internal identifier. |
| `name` | `String` | The 3-letter currency code (e.g., "USD"). |
| `description` | `String` | The full name of the currency. |
| `rate` | `Double` | The exchange rate relative to a base currency (USD). |

## 3. Database Tables to be Updated

This journey primarily affects how data is written; it does not introduce new tables.

-   **`t_user_account`**: The `currency_code` column is populated when an account is created.
-   **`t_user_book`**: The `default_currency_code` column is populated when a book is created.
-   **`t_user_balance_flow`**: Both the `amount` and `converted_amount` columns are populated for transactions involving currency conversion.

## 4. API Calls

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/accounts` | Creates a new account, specifying its `currencyCode`. |
| `POST` | `/balance-flows` | Creates a new transaction. The payload must include `convertedAmount` if a currency conversion is involved. |
| `GET` | `/currencies/all` | Retrieves a list of all supported currencies. |
| `GET` | `/currencies/rate` | Calculates the exchange rate between a `from` and `to` currency. |
| `GET` | `/currencies/calc` | Calculates the converted value for a specific amount between two currencies. |
| `POST` | `/currencies/refresh` | Triggers a refresh of exchange rates from the external API. |
| `GET` | `/accounts/overview` | All endpoints for reporting and overviews perform currency conversion implicitly. |
| `GET` | `/reports/*` | All endpoints for reporting and overviews perform currency conversion implicitly. |

## 5. Business Rules and Functionality

-   **Currency Rate Management**: At startup, `CurrencyDataLoader` loads a list of currencies and their base rates against USD from `currency.json`. Immediately after, `CurrencyRemoteDataLoader` attempts to call `CurrencyService.refreshCurrency()` to fetch the latest rates from `api.exchangerate-api.com`.

-   **Conversion Calculation**: The core conversion logic resides in `CurrencyService`. It calculates the rate between any two currencies by using their stored rates relative to USD. This means all rates are pivoted through USD.

    ```java
    // In CurrencyService.java
    public BigDecimal convert(String fromCode, String toCode) {
        List<CurrencyDetails> currencyList = applicationScopeBean.getCurrencyDetailsList();
        CurrencyDetails fromCurrency = //... find fromCurrency in list
        CurrencyDetails toCurrency = //... find toCurrency in list
        BigDecimal fromRate = BigDecimal.valueOf(fromCurrency.getRate());
        BigDecimal toRate = BigDecimal.valueOf(toCurrency.getRate());
        // All rates are vs USD, so to go from A to B, we do (A->USD) / (B->USD) which is B/A
        return toRate.divide(fromRate, 20, RoundingMode.CEILING);
    }
    ```

-   **Transaction Validation**: `BalanceFlowService` enforces that a `convertedAmount` is provided when necessary.
    -   For **Expenses/Incomes** in a foreign currency account, every category split must have a `convertedAmount`.
    -   For **Transfers** between accounts with different currencies, the main `convertedAmount` field on the form is mandatory.

    ```java
    // In BalanceFlowService.java (checkBeforeAdd method)
    if (!account.getCurrencyCode().equals(toAccount.getCurrencyCode())) {
        if (form.getConvertedAmount() == null) {
            throw new FailureMessageException("valid.fail");
        }
    }
    ```

-   **Consolidated Reporting**: All services that perform financial aggregation (`AccountService`, `ReportService`) systematically use `currencyService.convert()` to normalize every amount to the group's default currency before summing them. This ensures reports are accurate and consistent.

    ```java
    // In AccountService.java (overview method)
    for (Account account : assetAccounts) {
        assetBalance = assetBalance.add(currencyService.convert(account.getBalance(), account.getCurrencyCode(), group.getDefaultCurrencyCode()));
    }
    ```

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-CUR-01** | Create a new account with currency "EUR". | The account is created successfully with `currency_code` = "EUR". |
| **TC-CUR-02** | Record a €100 expense in the EUR account (Book default is USD). The user provides a converted amount of $108. | A `BalanceFlow` is created with `amount` = 100 and `convertedAmount` = 108. The EUR account balance decreases by 100. |
| **TC-CUR-03** | Transfer $200 from a USD account to a EUR account, providing a `convertedAmount` of €185. | The USD account balance decreases by 200. The EUR account balance increases by 185. |
| **TC-CUR-04** | Attempt a transfer between a USD and EUR account without providing a `convertedAmount`. | The API should return a validation error (400 Bad Request). |
| **TC-CUR-05** | View the financial overview with a $1000 USD account and a €500 EUR account (rate 1 EUR = 1.10 USD). | The total assets should be reported as $1550 (1000 + 500 * 1.10). |
| **TC-CUR-06** | Call the `/currencies/calc` endpoint with from=EUR, to=JPY, amount=100. | The API should return the correctly calculated amount in JPY. |

## 7. State any Assumptions

*   All exchange rates loaded from `currency.json` and the external API are relative to **USD** as the base currency.
*   The application relies on an active internet connection at startup to attempt to refresh exchange rates. If this fails, it will proceed with potentially stale data from `currency.json`.
*   For transactions, the user is the source of truth for the `convertedAmount`. The system may provide a calculated suggestion, but the user-provided value is what gets saved, as this reflects the actual rate applied by their financial institution.
*   The user's active `Group` has a `defaultCurrencyCode` which is used as the target for all reporting and overview conversions.

