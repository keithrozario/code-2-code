# Functional Specification: MoneyNote API

## 1. Introduction

This document provides a comprehensive functional specification for the MoneyNote API, a self-hosted, open-source bookkeeping application. It details the system's features, user journeys, business rules, and technical architecture.

### 1.1. Purpose of the Document

The purpose of this functional specification is to serve as the definitive guide and single source of truth for the MoneyNote application. It is intended for a wide audience, including developers, quality assurance testers, product managers, and business stakeholders.

This document will:
- **Define Scope:** Clearly articulate the capabilities and limitations of the system.
- **Guide Development:** Provide detailed requirements and user flows to guide the implementation of new features and modifications to existing ones.
- **Ensure Quality:** Establish a clear set of testable requirements for quality assurance and user acceptance testing.
- **Facilitate Communication:** Create a shared understanding of the system's functionality across all teams and stakeholders.
- **Serve as a Reference:** Act as a technical and functional reference for future maintenance, support, and strategic planning.

### 1.2. Goals and Objectives

The primary goal of the MoneyNote application is to empower individuals and small businesses with a private, secure, and comprehensive tool for managing their finances. The system is designed to be self-hostable, ensuring users retain full control and ownership of their sensitive financial data.

The key objectives of the system are:

- **Provide Financial Clarity:** To offer users a clear, consolidated, and accurate overview of their financial health, including their net worth, assets, and liabilities.
- **Enable Detailed Tracking:** To provide robust and intuitive tools for tracking daily incomes, expenses, and transfers with detailed categorization and tagging.
- **Support Diverse Financial Scenarios:** To deliver flexible features that accommodate real-world complexity, including support for managing accounts in multiple currencies and maintaining separate ledgers ("Books") for different financial contexts (e.g., personal vs. business).
- **Ensure Data Integrity and Completeness:** To allow users to attach digital records (e.g., receipts, invoices) to transactions, creating a complete and verifiable financial history.
- **Facilitate Collaboration:** To support multi-user collaboration through a secure group system with role-based access controls, allowing families or small teams to manage finances together.

### 1.3. Scope

The scope of this document covers the core functionalities of the MoneyNote API. The features detailed herein define the boundaries of the current system.

#### In Scope

The following features and capabilities are within the scope of the MoneyNote application:

- **Core Transaction Management:** Full CRUD (Create, Read, Update, Delete) operations for financial transactions, including Expenses, Incomes, Transfers between accounts, and Balance Adjustments.
- **Account Management:** Creation and management of various financial account types, including Checking, Credit, Assets, and Debts.
- **Financial Overview and Reporting:**
    - Calculation and display of Net Worth, Total Assets, and Total Debts.
    - Generation of analytical reports on income and expenses, aggregated by category, tag, and payee.
- **Data Organization:**
    - A hierarchical system for creating and managing categories and tags.
    - Management of a list of payees for transactions.
- **Multi-Book Functionality:** The ability to create and manage multiple, independent financial ledgers ("Books"), each with its own set of categories, tags, payees, and default currency. This includes creating books from templates or by cloning existing ones.
- **Multi-Currency Support:**
    - Assignment of a specific currency to each financial account.
    - Recording of transactions in their original currency, with functionality to store a converted amount in the book's default currency.
    - Consolidation of all financial reports into a single, user-defined default currency.
- **File Attachments:** The ability to upload, attach, view, and delete digital files (e.g., PDFs, images) to transaction records.
- **User and Group Management:** User registration, authentication, and a collaborative "Group" system that allows multiple users to share financial data with defined roles (Owner, Operator, Guest).

#### Out of Scope

The following features and capabilities are considered out of scope for the current version of the MoneyNote application:

- **Automated Budgeting:** The system does not include features for creating spending budgets, setting limits for categories, or tracking performance against a budget.
- **Advanced Investment Tracking:** While asset accounts can be created, the system does not track investment performance, stock portfolios, capital gains, or dividends.
- **Invoicing and Bill Payment:** The application is designed for bookkeeping and does not include functionality to generate or send client invoices, nor does it integrate with services to pay bills directly.
- **Financial Forecasting:** All reporting is based on historical data. The system does not provide tools for forecasting future financial positions or cash flow.
- **Direct Bank Integration:** The system does not automatically import transactions from financial institutions via open banking APIs (e.g., Plaid). All transaction data entry is manual.## Key Data Entities 

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

This document details the user journey for monitoring one's overall financial health using the MoneyNote application's reporting and overview features.

## 1. Detailed User Journey and Flows

This journey focuses on providing users with high-level summaries and detailed, filterable reports to understand their financial standing. There are two primary flows.

### Journey 1: Viewing Financial Overview

This flow allows the user to see a snapshot of their net worth at any time.

**User Flow:**
1.  The user logs into the application.
2.  They navigate to the main dashboard or an "Overview" page.
3.  The system automatically calculates and displays three key metrics:
    *   **Total Assets**: The sum of all positive-balance accounts (Checking, Assets).
    *   **Total Debts**: The sum of all negative-balance accounts (Credit Cards, Debts).
    *   **Net Worth**: The difference between Total Assets and Total Debts.
4.  All calculations are performed in the user's default currency, with automatic conversion for accounts in foreign currencies.
5.  The user can also view charts that break down the composition of their assets and debts by account.

### Journey 2: Analyzing Financial Reports

This flow allows the user to dive deeper into their spending and income habits.

**User Flow:**
1.  The user navigates to the "Reports" section of the application.
2.  They select a report type, such as "Expense by Category", "Income by Tag", or "Expense by Payee".
3.  A form appears, allowing the user to filter the report data by:
    *   **Date Range** (`minTime`, `maxTime`)
    *   **Book**
    *   **Account**
    *   **Categories**, **Tags**, or **Payees**
4.  The user submits the form.
5.  The system generates and displays a visual report (e.g., a pie chart or bar chart) showing the aggregated data, with amounts and percentage breakdowns.
6.  The user can interact with the report, for example, by clicking on a category to see a drill-down report of its sub-categories.

## 2. Detailed Object-Level Data Structures

This journey primarily involves reading and aggregating data. The key data structures are the `Account` entity and the DTOs used for reporting.

### `Account` Entity (`t_user_account` table)

Represents a single financial account.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `group` | `Group` | (FK) The group this account belongs to. |
| `type` | `AccountType` | Enum: `CHECKING`, `CREDIT`, `ASSET`, `DEBT`. |
| `balance` | `BigDecimal` | The current balance of the account. |
| `include` | `Boolean` | If `true`, this account is included in net worth calculations. |
| `currencyCode` | `String` | The currency of the account (e.g., "USD", "EUR"). |
| `enable` | `Boolean` | If `true`, the account is active. |
| `name` | `String` | The name of the account. |
| `notes` | `String` | Optional notes. |
| `creditLimit`| `BigDecimal`| The credit limit for credit accounts. |

### `ChartVO` Data Structure

This is the DTO used to structure data for chart visualizations in reports.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `x` | `String` | The label for a data point (e.g., a category name like "Food"). |
| `y` | `BigDecimal` | The value for a data point (e.g., the total amount spent on "Food"). |
| `percent` | `BigDecimal` | The percentage this data point represents out of the total. |

### `CategoryReportQueryForm` Data Structure

This DTO is used to capture user input for filtering financial reports.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `book` | `Integer` | ID of the book to report on. |
| `minTime` | `Long` | The start of the date range for the report (timestamp). |
| `maxTime` | `Long` | The end of the date range for the report (timestamp). |
| `payees` | `Set<Integer>` | Set of Payee IDs to filter by. |
| `categories`| `Set<Integer>` | Set of Category IDs to filter by. |
| `tags` | `Set<Integer>` | Set of Tag IDs to filter by. |
| `account` | `Integer` | ID of a specific account to filter by. |

## 3. Database Tables to be Updated

This user journey is **read-only**. No database tables are updated. It exclusively involves querying and aggregating data from existing records in tables such as `t_user_account`, `t_user_balance_flow`, and `t_user_category_relation`.

## 4. API Calls

The monitoring and reporting functionalities are exposed through several REST endpoints.

| Method | Endpoint | Controller | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/accounts/overview` | `AccountController` | Retrieves the user's total assets, debts, and net worth. |
| `GET` | `/reports/balance` | `ReportController` | Retrieves data for generating asset and debt breakdown charts. |
| `GET` | `/reports/expense-category`| `ReportController` | Generates a report of expenses aggregated by category. |
| `GET` | `/reports/income-category` | `ReportController` | Generates a report of income aggregated by category. |
| `GET` | `/reports/expense-tag` | `ReportController` | Generates a report of expenses aggregated by tag. |
| `GET` | `/reports/income-tag` | `ReportController` | Generates a report of income aggregated by tag. |
| `GET` | `/reports/expense-payee` | `ReportController` | Generates a report of expenses aggregated by payee. |
| `GET` | `/reports/income-payee` | `ReportController` | Generates a report of income aggregated by payee. |

## 5. Business Rules and Functionality

The core logic for this journey resides in `AccountService` and `ReportService`.

-   **Net Worth Calculation**: The `AccountService.overview()` method calculates the total assets and debts. It fetches all accounts, filters them by type (`CHECKING`/`ASSET` for assets, `CREDIT`/`DEBT` for debts), and ensures they are `enabled` and `included` in reports. Crucially, it converts the balance of each account to the group's default currency before summing them up.

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

-   **Category Report Generation**: The `ReportService.reportCategory()` method generates data for category-based reports. It finds all transaction relations (`CategoryRelation`) that match the user's filter criteria. It then aggregates the `convertedAmount` for each top-level category and their children to build a list of `ChartVO` objects.

    ```java
    // In ReportService.java
    public List<ChartVO> reportCategory(CategoryReportQueryForm form, CategoryType type) {
        // ... filtering logic to get rootCategories and categoryRelations ...
        
        for (Category i : rootCategories) {
            ChartVO vo = new ChartVO();
            vo.setX(i.getName());
            List<Category> offSpringCategory = TreeUtils.getOffspring(i, categories);
            List<Integer> offSpringCategoryIds = offSpringCategory.stream().map(j->j.getId()).collect(Collectors.toList());
            offSpringCategoryIds.add(i.getId());
            // Sums up the convertedAmount for the category and all its children
            vo.setY(categoryRelations.stream().filter(j -> offSpringCategoryIds.contains(j.getCategory().getId())).map(CategoryRelation::getConvertedAmount).reduce(BigDecimal.ZERO, BigDecimal::add));
            if (vo.getY().signum() != 0) {
                result.add(vo);
            }
        }
        
        // ... logic to calculate percentages and sort the results ...
        return result;
    }
    ```

-   **Balance Report Generation**: The `ReportService.reportBalance()` method provides the data for asset vs. debt visualization. It fetches all asset and debt accounts, converts their balances to the default currency, and structures them into two lists of `ChartVO` objects. Debt balances are negated to represent them as positive values in the report.

    ```java
    // In ReportService.java
    public List<List<ChartVO>> reportBalance() {
        // ...
        List<ChartVO> debtChart = new ArrayList<>();
        List<Account> debtAccounts = accountService.getDebts();
        for (Account account : debtAccounts) {
            if (account.getBalance().signum() != 0) {
                ChartVO vo = new ChartVO();
                vo.setX(account.getName());
                // Negate the balance to show debt as a positive value in the chart
                vo.setY(currencyService.convert(account.getBalance(), account.getCurrencyCode(), group.getDefaultCurrencyCode()).negate());
                debtChart.add(vo);
            }
        }
        // ...
        result.add(assetChart);
        result.add(debtChart);
        return result;
    }
    ```

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-MON-01** | User has one checking account (USD) with $1000 and one asset account (USD) with $2000. No debts. | `/accounts/overview` should return: Assets: $3000, Debts: $0, Net Worth: $3000. |
| **TC-MON-02** | User has one checking account (USD) with $1000 and one credit card (USD) with a balance of -$500. | `/accounts/overview` should return: Assets: $1000, Debts: $500, Net Worth: $500. |
| **TC-MON-03** | User has a USD account with $100 and a EUR account with €200. Default currency is USD, and 1 EUR = 1.10 USD. | `/accounts/overview` should calculate total assets as $100 + (€200 * 1.10) = $320. |
| **TC-MON-04** | An account is marked with `include=false`. | The balance of this account should be ignored in all `/accounts/overview` and `/reports/balance` calculations. |
| **TC-REP-01** | Generate an "Expense by Category" report for a period with $100 on "Food" and $50 on "Transport". | The report should return two `ChartVO` items: {x:"Food", y:100, percent:66.67} and {x:"Transport", y:50, percent:33.33}. |
| **TC-REP-02** | Generate a category report filtered by a specific account. | The report should only include transaction amounts from the selected account. |
| **TC-REP-03** | Generate a category report for a parent category "Food" which has sub-categories "Groceries" ($80) and "Restaurants" ($120). | The report for "Food" should show a total of $200. |
| **TC-REP-04** | Generate a report for a time range where there are no transactions. | The API should return an empty list. |
| **TC-REP-05** | Generate a balance report. | The API should return two lists of `ChartVO`s, one for assets and one for debts, with correct amounts and percentages. |

## 7. State any Assumptions

*   The user is authenticated and has a valid session context (`CurrentSession`) containing their active `Group` and `Book`.
*   Currency exchange rates are available in the `ApplicationScopeBean`. If rates are missing or the external API fails, conversions may use stale or default data.
*   The frontend is responsible for rendering the `ChartVO` data into appropriate visual charts.
*   The integrity of the hierarchical category and tag data (`parent_id`, `level`) is correctly maintained by the application.
*   All financial calculations rely on `BigDecimal` for precision, assuming this correctly avoids floating-point errors.
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

This document details the user journey for attaching, viewing, and managing digital files associated with financial transactions.

## 1. Detailed User Journey and Flows

This journey allows users to upload, view, and delete file attachments (e.g., receipts, invoices) for their transaction records.

### Journey: Attaching, Viewing, and Deleting a File

**User Flow:**
1.  The user is viewing the details of a specific transaction (`BalanceFlow`).
2.  They click an "Add Attachment" or "Upload File" button.
3.  A file selection dialog opens on their device. The user selects a file (e.g., a PDF, PNG, or JPG).
4.  The file is uploaded to the server. The system validates the file type and size.
5.  Upon successful upload, the file appears in a list of attachments for that transaction.
6.  The user can later click on the file's name to view it in the browser or download it.
7.  The user can also choose to delete an attachment, which removes the file from the system permanently.

## 2. Detailed Object-Level Data Structures

The primary data structure for this journey is the `FlowFile` entity.

### `FlowFile` Entity (`t_flow_file` table)

This entity represents a single file attached to a transaction.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `data` | `byte[]` | The binary content of the file, stored as a `LONGBLOB` in the database. It is lazily fetched for performance. |
| `creator` | `User` | (FK) The user who uploaded the file. |
| `flow` | `BalanceFlow` | (FK) The transaction this file is attached to. |
| `createTime` | `Long` | The timestamp when the file was uploaded. |
| `contentType` | `String` | The MIME type of the file (e.g., "application/pdf"). |
| `size` | `Long` | The size of the file in bytes. |
| `originalName` | `String` | The original filename from the user's device. |

### `FlowFileDetails` Data Structure

This is the DTO used for sending file metadata to the client. It omits the large `data` field.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | File ID. |
| `createTime` | `Long` | Upload timestamp. |
| `contentType` | `String` | File MIME type. |
| `size` | `Long` | File size. |
| `originalName` | `String` | Original filename. |

## 3. Database Tables to be Updated

-   **`t_flow_file`**:
    -   A new record is **inserted** when a file is uploaded.
    -   A record is **deleted** when a file is removed.
-   **`t_user_balance_flow`**: When a transaction is updated, the associated `FlowFile` records are re-linked to the new transaction record. When a transaction is deleted, all its associated `FlowFile` records are also deleted.

## 4. API Calls

The interactions are handled by `BalanceFlowController` and `FlowFileController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/balance-flows/{id}/addFile` | Uploads a file and attaches it to the transaction with the specified `id`. |
| `GET` | `/balance-flows/{id}/files` | Retrieves a list of all file attachments for the specified transaction. |
| `GET` | `/flow-files/view` | Serves the binary content of a file for viewing or downloading. Requires `id` and `createTime` for access. |
| `DELETE` | `/flow-files/{id}` | Deletes a specific file attachment. |

## 5. Business Rules and Functionality

The core logic is handled by `BalanceFlowService` and `FlowFileService`.

-   **File Upload and Association**: The `BalanceFlowService.addFile` method handles the `MultipartFile` upload. It creates a `FlowFile` entity, populates it with the file's binary data and metadata, and associates it with the correct `BalanceFlow` record.

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

-   **File Validation**: The system uses a custom validator (`@ValidFile`) that checks the `Content-Type` of the uploaded file. It only permits `application/pdf`, `image/png`, `image/jpg`, and `image/jpeg`. This is enforced at the controller level.

    ```java
    // In FileValidator.java
    private boolean isSupportedContentType(String contentType) {
        return contentType.equals("application/pdf")
                || contentType.equals("image/png")
                || contentType.equals("image/jpg")
                || contentType.equals("image/jpeg");
    }
    ```

-   **Secure File Viewing**: To prevent unauthorized access or simple enumeration of file URLs, the `/flow-files/view` endpoint requires both the file `id` and its `createTime` timestamp as parameters. The service layer validates that both match the record in the database before serving the file content.

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

-   **Cascading Deletes**: When a `BalanceFlow` transaction is deleted, the system explicitly deletes all associated `FlowFile` records to prevent orphaned files in the database.

    ```java
    // In BalanceFlowService.java
    public boolean remove(int id) {
        BalanceFlow entity = baseService.findFlowById(id);
        refundBalance(entity);
        // 要先删除文件 (Translation: Must delete files first)
        flowFileRepository.deleteByFlow(entity);
        balanceFlowRepository.delete(entity);
        return true;
    }
    ```

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-FILE-01** | Upload a valid PDF file (`< 100MB`) to a transaction. | The API returns a 200 OK status. A new `FlowFile` record is created and linked to the transaction. |
| **TC-FILE-02** | Attempt to upload an unsupported file type (e.g., `.zip`, `.exe`). | The API should return a validation error (400 Bad Request). No file record is created. |
| **TC-FILE-03** | Attempt to upload a file larger than the configured limit (100MB). | The request should be rejected by the server, likely with a `MaxUploadSizeExceededException`. |
| **TC-FILE-04** | Retrieve the list of files for a transaction with two attachments. | The API returns a JSON array with two `FlowFileDetails` objects. |
| **TC-FILE-05** | View an attached file using the correct `id` and `createTime`. | The API returns the file's binary data with the correct `Content-Type` header. |
| **TC-FILE-06** | Attempt to view a file with the correct `id` but an incorrect `createTime`. | The API should return an error (e.g., 400 Bad Request or 404 Not Found). |
| **TC-FILE-07** | Delete a file attachment. | The `FlowFile` record is deleted from the database. The associated `BalanceFlow` transaction remains untouched. |
| **TC-FILE-08** | Delete a transaction that has file attachments. | The `BalanceFlow` record and all associated `FlowFile` records are deleted from the database. |

## 7. State any Assumptions

*   The user is authenticated and has permission to view and modify the transaction they are attaching files to.
*   The maximum file size is configured in `application.properties` (`spring.servlet.multipart.max-file-size=100MB`).
*   The frontend is responsible for constructing the correct URL for the `/flow-files/view` endpoint, including both the `id` and `createTime` parameters.
*   Storing binary files directly in the database (`LONGBLOB`) is an acceptable storage strategy for the scale of this application, though it can impact database performance and backup size.
# Journey 4: Supporting Multiple Books

This document details the user journey for managing multiple books within the MoneyNote application. A "Book" acts as a separate ledger, allowing users to segregate different financial areas (e.g., "Personal Finances," "Business," "Vacation Fund").

## 1. Detailed User Journey and Flows

This journey covers the creation, management, and utilization of multiple books.

### Journey 1: Creating a New Book

Users can create a new, empty book, create one from a predefined template, or clone the structure of an existing book.

**User Flow (Create from Template):**
1.  The user navigates to the "Settings" or "Manage Books" section.
2.  They click "Add Book" and choose the "From Template" option.
3.  The UI displays a list of available templates (e.g., "Default Personal Finance," "Small Business").
4.  The user selects a template and provides a **Name** for the new book. They can also add optional **Notes**.
5.  Upon saving, the system creates a new `Book` record.
6.  Crucially, the system also populates the new book with a default set of `Categories`, `Tags`, and `Payees` as defined in the selected `BookTemplate`.

**User Flow (Clone Existing Book):**
1.  The user follows steps 1-2 above but chooses the "Clone Existing Book" option.
2.  They select one of their existing books as the source.
3.  They provide a new **Name** for the cloned book.
4.  The system creates the new `Book` and copies over all `Categories`, `Tags`, and `Payees` from the source book. Financial transactions (`BalanceFlow` records) are **not** copied.

### Journey 2: Switching the Active Book

The application has a concept of a "current" or "active" book. All new transactions and data entries are recorded in the currently active book.

**User Flow:**
1.  The user clicks on a book switcher UI element, which might be a dropdown in the header or a dedicated menu.
2.  A list of all their available books is displayed.
3.  The user selects a different book from the list.
4.  The application's session is updated to set the selected book as the new "current book".
5.  The UI refreshes, displaying the dashboard, accounts, and transactions associated with the newly selected book. The user's `defaultBook` is also updated.

### Journey 3: Managing and Updating a Book

Users can modify the details of a book or disable it.

**User Flow:**
1.  The user navigates to the "Manage Books" section, which lists all their books.
2.  They select a book to edit.
3.  A form appears, allowing them to change:
    *   **Name**
    *   **Notes**
    *   **Default Currency**
    *   **Default accounts** for expenses, incomes, and transfers.
    *   **Default categories** for expenses and incomes.
    *   **Enable/Disable** status.
4.  The user saves the changes. The system updates the corresponding `Book` record in the database.

### Journey 4: Deleting a Book

A book can only be deleted if it contains no financial transactions.

**User Flow:**
1.  From the "Manage Books" list, the user selects the "Delete" option for a book.
2.  The system checks if any `BalanceFlow` records are associated with the book.
3.  **If transactions exist**, the API returns an error message (e.g., "Cannot delete a book with existing transactions").
4.  **If no transactions exist**, the system proceeds to delete all related `Categories`, `Tags`, and `Payees` for that book, and finally deletes the `Book` record itself.
5.  If the deleted book was the default for the user or group, the system intelligently resets the default to another available book.

## 2. Detailed Object-Level Data Structures

### `Book` Entity (`t_user_book` table)

This is the central entity for this journey.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `group` | `Group` | (FK) The group this book belongs to. |
| `name` | `String` | The name of the book (e.g., "Personal Finances"). |
| `notes` | `String` | Optional descriptive notes. |
| `enable` | `Boolean` | Whether the book is active and can be used. |
| `defaultCurrencyCode` | `String` | The default currency for this book (e.g., "USD"). |
| `defaultExpenseAccount` | `Account` | (FK, Optional) Default account for new expenses. |
| `defaultIncomeAccount` | `Account` | (FK, Optional) Default account for new incomes. |
| `defaultTransferFromAccount`| `Account` | (FK, Optional) Default source account for transfers. |
| `defaultTransferToAccount` | `Account` | (FK, Optional) Default destination account for transfers. |
| `defaultExpenseCategory` | `Category`| (FK, Optional) Default category for new expenses. |
| `defaultIncomeCategory` | `Category`| (FK, Optional) Default category for new incomes. |
| `exportAt` | `Long` | Timestamp of the last transaction export. |
| `sort` | `Integer` | A number for sorting the list of books. |
| `tags` | `List<Tag>` | (Relation) All tags belonging to this book. |
| `categories`| `List<Category>`| (Relation) All categories belonging to this book. |
| `payees` | `List<Payee>` | (Relation) All payees belonging to this book. |

### `BookAddForm` Data Structure

This DTO is used when creating a new book.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `name` | `String` | The name for the new book. |
| `notes` | `String` | Optional notes. |
| `defaultCurrencyCode` | `String` | The currency code (e.g., "USD"). |
| `sort` | `Integer` | Sort order. |

### `BookUpdateForm` Data Structure

This DTO is used when updating an existing book's settings.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `name` | `String` | The new name for the book. |
| `notes` | `String` | New notes. |
| `defaultCurrencyCode` | `String` | New default currency. |
| `defaultExpenseAccountId` | `Integer` | ID of the default expense account. |
| `defaultIncomeAccountId` | `Integer` | ID of the default income account. |
| `defaultTransferFromAccountId`| `Integer` | ID of the default transfer-from account. |
| `defaultTransferToAccountId` | `Integer` | ID of the default transfer-to account. |
| `defaultExpenseCategoryId` | `Integer` | ID of the default expense category. |
| `defaultIncomeCategoryId` | `Integer` | ID of the default income category. |
| `sort` | `Integer` | New sort order. |

## 3. Database Tables to be Updated

-   **`t_user_book`**: A new record is **inserted** when a book is created. The record is **updated** when its details are changed, and **deleted** upon removal.
-   **`t_user`**: The `default_book_id` column is **updated** when a user switches their active book or when their default book is deleted.
-   **`t_user_group`**: The `default_book_id` column is **updated** if the deleted book was the group's default.
-   **`t_user_category`**, **`t_user_tag`**, **`t_user_payee`**: Records are **inserted** when a book is created from a template or cloned. Records are **deleted** when a book is deleted.

## 4. API Calls

The primary controller for these operations is `BookController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/books` | Creates a new, empty book using `BookAddForm`. |
| `POST` | `/books/add-by-template` | Creates a new book from a `BookTemplate`. |
| `POST` | `/books/add-by-book` | Creates a new book by cloning an existing one. |
| `GET` | `/books` | Queries and lists all books for the current user's group. |
| `GET` | `/books/{id}` | Retrieves the details of a single book. |
| `PUT` | `/books/{id}` | Updates an existing book using `BookUpdateForm`. |
| `DELETE`| `/books/{id}` | Deletes a book. |
| `PATCH` | `/books/{id}/toggle` | Enables or disables a book. |
| `PATCH` | `/users/setDefaultBook/{id}` | (In `UserController`) Sets the user's active/default book. |

## 5. Business Rules and Functionality

The core logic resides in `BookService`.

-   **Deletion Constraint**: A book cannot be deleted if it has associated financial transactions. This is a critical data integrity rule.

    ```java
    // In BookService.java
    public boolean remove(Integer id) {
        // ... (permission checks)
        Book entity = baseService.getBookInGroup(id);
        if (balanceFlowRepository.existsByBook(entity)) {
            throw new FailureMessageException("book.delete.has.flow");
        }
        // ... (deletion logic for categories, tags, etc.)
        bookRepository.delete(entity);
        return true;
    }
    ```

-   **Creation from Template**: When creating from a template, the service iterates through the template's items and creates new entities associated with the new book.

    ```java
    // In BookService.java
    public void setBookByBookTemplate(BookTemplate bookTemplate, Group group, Book book) {
        // ... (set book properties)
        bookRepository.save(book);
        saveTag(TreeUtils.buildTree(bookTemplate.getTags()), book);
        saveCategory(TreeUtils.buildTree(bookTemplate.getCategories()), book);
        bookTemplate.getPayees().forEach(i -> {
            Payee payee = new Payee();
            payee.setName(i.getName());
            payee.setBook(book);
            payeeRepository.save(payee);
        });
    }
    ```

-   **Default Book Management**: When a book is deleted, the system checks if it was the default for any users and, if so, reassigns their default to the group's default book.

    ```java
    // In BookService.java (within the disable logic, which is related to deletion)
    private void checkDefault(Integer id) {
        Group group = sessionUtil.getCurrentGroup();
        if (group.getDefaultBook().getId().equals(id)) {
            throw new FailureMessageException("book.disable.is.group.default");
        }
        Book entity = baseService.getBookInGroup(id);
        List<User> users = userRepository.findByDefaultBook(entity);
        users.forEach(user -> {
            user.setDefaultBook(group.getDefaultBook());
            userRepository.save(user);
        });
    }
    ```

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-BOOK-ADD-01**| Create a new book named "Business" from a template. | A new `Book` record is created. The book is populated with categories, tags, and payees from the template. |
| **TC-BOOK-ADD-02**| Clone an existing book "Personal" to a new book "Archive". | A new `Book` record "Archive" is created. It has the same categories, tags, and payees as "Personal". No transactions are copied. |
| **TC-BOOK-ADD-03**| Attempt to create a book with a name that already exists in the group. | The API should return a validation error (e.g., 400 Bad Request). |
| **TC-BOOK-SWITCH-01**| User switches the active book from "Personal" to "Business". | The user's session is updated. Subsequent API calls for transactions are scoped to the "Business" book. The user's `default_book_id` is updated. |
| **TC-BOOK-UPD-01**| Update a book's name and default currency. | The corresponding `t_user_book` record is updated with the new values. |
| **TC-BOOK-DEL-01**| Attempt to delete a book that contains transactions. | The API returns an error, and the book is not deleted. |
| **TC-BOOK-DEL-02**| Delete a book that has no transactions. | The `Book` record and all its associated categories, tags, and payees are deleted from the database. |
| **TC-BOOK-DEL-03**| Delete a book that is set as the user's default. | The book is deleted. The user's default book is reset to the group's default book. |

## 7. State any Assumptions

*   The user is authenticated and belongs to a `Group`. All book operations are scoped within that group.
*   The frontend is responsible for providing valid IDs for templates, source books, and other entities when creating or updating books.
*   The application maintains a "current book" in the user's session (`CurrentSession`), which is used as the default context for most financial operations.
*   The `book_tpl.json` file, which contains the book templates, is a static resource available in the application's classpath.
# Journey 5: Supporting Multiple Currencies

This document details the user journey for managing accounts and transactions in multiple currencies.

## 1. Detailed User Journey and Flows

This journey enables users to handle finances across different countries and currencies, with the system providing conversion and consolidation for reporting.

### Journey 1: Managing Foreign Currency Accounts and Transactions

This flow covers how a user sets up accounts in different currencies and records transactions with them.

**User Flow:**
1.  **Account Creation**: The user creates a new `Account` (e.g., "European Bank Account"). In the creation form, they select a currency from a list of world currencies (e.g., "EUR").
2.  **Recording a Transaction**: The user records an `EXPENSE` or `INCOME` transaction in the "European Bank Account".
3.  **Automatic Conversion**: The system detects that the account's currency ("EUR") is different from the Book's default currency (e.g., "USD").
4.  The UI prompts the user for the **Converted Amount**. It may suggest a value based on the latest exchange rate, but the user can override it to match their bank statement.
5.  The user saves the transaction. The system stores both the original amount (in EUR) and the converted amount (in USD).
6.  The balance of the "European Bank Account" is updated in its native currency (EUR).

### Journey 2: Transferring Funds Between Currencies

This flow is for when a user moves money between two of their accounts that have different currencies.

**User Flow:**
1.  The user initiates a `TRANSFER` transaction.
2.  They select a "From Account" (e.g., "US Checking" in USD) and a "To Account" (e.g., "European Bank Account" in EUR).
3.  They enter the `amount` being sent from the source account (e.g., 110 USD).
4.  A mandatory `convertedAmount` field appears, where the user must enter the final amount that was received in the destination account (e.g., 100 EUR). This captures the exact exchange rate of the transfer.
5.  The user saves the transfer. The system deducts the `amount` from the source account and adds the `convertedAmount` to the destination account.

### Journey 3: Viewing Consolidated Reports

This flow describes how the system presents a unified view of finances, regardless of the currencies involved.

**User Flow:**
1.  The user navigates to a report, such as the "Net Worth Overview" or "Expense by Category" report.
2.  The system gathers all relevant accounts and transactions.
3.  For any account or transaction that is not in the user's default currency, the system uses the stored `convertedAmount` or calculates the converted value on the fly.
4.  All figures in the report are presented in the user's single, default currency, providing a clear and accurate consolidated picture of their financial situation.

## 2. Detailed Object-Level Data Structures

The multi-currency feature relies on in-memory data structures and fields within core entities.

### `CurrencyDetails` Data Structure

This is the in-memory representation of a currency, loaded from `currency.json`. There is no corresponding database table.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | An identifier from the JSON file. |
| `name` | `String` | The 3-letter ISO currency code (e.g., "USD", "EUR"). This is the primary identifier. |
| `description`| `String` | The full name of the currency (e.g., "United States Dollar"). |
| `rate` | `Double` | The exchange rate of this currency against the base currency (USD). |
| `rate2` | `Double` | A transient field used for displaying rates against a user-selected base currency in the UI. |

### `Account` Entity (`t_user_account` table)

The `Account` entity is extended to support multiple currencies.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `currencyCode` | `String` | `NOT NULL`. The 3-letter ISO code for the currency of this account (e.g., "USD", "JPY"). |

### `BalanceFlow` Entity (`t_user_balance_flow` table)

The transaction entity stores both original and converted amounts.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `amount` | `BigDecimal` | The amount of the transaction in the currency of the source `account`. |
| `convertedAmount` | `BigDecimal` | The equivalent amount in the Book's default currency. This is mandatory if the source account's currency differs from the book's currency. For transfers, this is the amount in the destination account's currency. |

### `Book` Entity (`t_user_book` table)

Each book has its own base currency for reporting.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `defaultCurrencyCode` | `String` | `NOT NULL`. The default 3-letter ISO currency code for all reporting within this book. |

## 3. Database Tables to be Updated

The multi-currency feature does not introduce new tables. Instead, it utilizes specific columns within existing tables:

-   **`t_user_account`**: The `currency_code` column is populated when an account is created.
-   **`t_user_book`**: The `default_currency_code` column is set for each book.
-   **`t_user_balance_flow`**: The `amount` and `converted_amount` columns are populated for each transaction.

There is **no `currency` table** in the database. All currency definitions and rates are managed in application memory.

## 4. API Calls

The `CurrencyController` provides endpoints for currency-related operations.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/currencies/all` | Returns the complete list of all supported currencies from the in-memory cache. |
| `GET` | `/currencies` | Returns a paginated and filterable list of currencies. Can also show rates relative to a specified base currency. |
| `POST` | `/currencies/refresh` | Triggers a refresh of the exchange rates from the external API (`exchangerate-api.com`). |
| `GET` | `/currencies/rate` | Calculates and returns the exchange rate between a `from` and `to` currency. |
| `GET` | `/currencies/calc` | Calculates and returns the converted value for a given `amount` between a `from` and `to` currency. |
| `PUT` | `/currencies/{id}/rate` | Manually updates the exchange rate of a specific currency relative to a chosen base. |

## 5. Business Rules and Functionality

The core logic is managed by the `CurrencyService`.

-   **In-Memory Currency Management**: The application loads all currency data from `currency.json` into an `ApplicationScopeBean` at startup. This bean acts as a global, in-memory cache for currency information.

    ```java
    // In CurrencyDataLoader.java
    public void run(ApplicationArguments args) {
        // ... loads currency.json into a List<CurrencyDetails>
        applicationScopeBean.setCurrencyDetailsList(currencyDetailsList);
    }
    ```

-   **Exchange Rate Conversion**: The system assumes **USD as the ultimate base currency**. All rates loaded from `currency.json` and the external API are relative to USD. The conversion between any two non-USD currencies is calculated by first converting from the source currency to USD, and then from USD to the target currency.

    ```java
    // In CurrencyService.java
    public BigDecimal convert(String fromCode, String toCode) {
        // ... finds fromCurrency and toCurrency from the in-memory list
        BigDecimal fromRate = BigDecimal.valueOf(fromCurrency.getRate()); // Rate vs USD
        BigDecimal toRate = BigDecimal.valueOf(toCurrency.getRate());   // Rate vs USD
        // (toRate / fromRate) gives the conversion rate
        return toRate.divide(fromRate, 20, RoundingMode.CEILING);
    }
    ```

-   **Rate Refreshing**: On startup and when the `/currencies/refresh` endpoint is called, the application fetches the latest rates from `https://api.exchangerate-api.com/v4/latest/USD` and updates the `rate` property of the `CurrencyDetails` objects in the in-memory list.

    ```java
    // In CurrencyService.java
    public boolean refreshCurrency() {
        try {
            HashMap<String, Object> resMap =  webUtils.get("https://api.exchangerate-api.com/v4/latest/USD");
            var ratesMap = (Map<String, Number>) resMap.get("rates");
            List<CurrencyDetails> currencyDetailsList = applicationScopeBean.getCurrencyDetailsList();
            ratesMap.forEach((key, value) -> {
                // ... updates the rate for the matching currency in the list
            });
        } catch (Exception e) {
            return false;
        }
        return true;
    }
    ```

-   **Mandatory Converted Amount**: The `BalanceFlowService` enforces that `convertedAmount` must be provided whenever a transaction's account currency does not match the book's default currency, or for any cross-currency transfer.

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-CUR-01** | Create a new account and set its currency to "EUR". | The `Account` is created successfully with `currency_code` set to "EUR". |
| **TC-CUR-02** | Create an `EXPENSE` of 100 EUR in a EUR account, within a book whose default currency is USD. Provide a `convertedAmount` of 108 USD. | The transaction is saved. The `amount` is 100, `convertedAmount` is 108. The EUR account balance decreases by 100. Reports show an expense of 108 USD. |
| **TC-CUR-03** | Attempt to create the same transaction as TC-CUR-02 but without providing a `convertedAmount`. | The API should return a validation error (400 Bad Request). |
| **TC-CUR-04** | Transfer 100 USD from a USD account to a JPY account. Provide a `convertedAmount` of 13500 JPY. | The USD account balance decreases by 100. The JPY account balance increases by 13500. |
| **TC-CUR-05** | Call the `GET /currencies/rate?from=EUR&to=JPY` endpoint. Assume EUR rate is 0.9 and JPY rate is 135 vs USD. | The API should return `150` (135 / 0.9). |
| **TC-CUR-06** | Call the `POST /currencies/refresh` endpoint. | The in-memory currency rates are updated with the latest values from the external API. Subsequent conversions use the new rates. |
| **TC-CUR-07** | View a net worth report with one account of 1000 USD and one account of 2000 EUR. The book's default is USD and the EUR->USD rate is 1.08. | The report should show a total net worth of 3160 USD (1000 + 2000 * 1.08). |

## 7. State any Assumptions

*   The application requires an internet connection at startup to refresh currency exchange rates. If the external API is unavailable, it will proceed with the potentially stale rates from `currency.json`.
*   The base currency for all rate calculations is hardcoded to **USD**. The external API URL is also hardcoded to fetch rates against USD.
*   The system trusts the user to provide the correct `convertedAmount` when prompted. While it can suggest a value, the user's input is the source of truth for the transaction record.
*   There is no historical tracking of exchange rates. All conversions for reporting are done using the current in-memory exchange rates, which may not reflect the historical rate at the time of the transaction. The `convertedAmount` stored with the transaction is the only historical record.
*   The list of currencies is managed by the `currency.json` file. There is no UI for adding or removing currencies from the system.
Look at the customized_report_money_note_detailed_journeys.md file, and the customized_report_money_note_data_layer.md file. These files represent a report for code in moneynote-api directory. As a senior business analyst Document "Journey 4: Supporting Multiple Books" functionality. Create a new supporting_multiple_books.md file, and in it populate the following:

* Detailed user journey and flows
* Detailed object level data structures
* Database tables to be updated
* API Calls that are made
* Any business rules and functionality required
* State any assumptions

# Project Modernization Report

# Table of Contents

1. [Report Metadata](#report-metadata)
1. [Summary](#summary)
1. [About this Project](#about-this-project)
    1. [Assessment Overview](#assessment-overview)
    1. [Architecture](#architecture)
    1. [Technology Stack](#technology-stack)
    1. [APIs and Endpoints](#apis-and-endpoints)
    1. [Data Layer](#data-layer)
1. [Assessment Findings](#assessment-findings)
    1. [Security and Compliance](#security-and-compliance)
    1. [Modernization Challenges](#modernization-challenges)
    1. [Modernization Opportunities](#modernization-opportunities)
1. [Cloud Migration](#cloud-migration)
    1. [Migration Overview](#migration-overview)
    1. [Shift to Compute Engine](#shift-to-compute-engine)
    1. [Modernize to Kubernetes Engine](#modernize-to-kubernetes-engine)
    1. [Modernize to Cloud Run](#modernize-to-cloud-run)


## Report Metadata

**Project:** moneynote-api

**Report ID:** CM-20250911-134104

**Generated:** Sep 11, 2025, 1:41 PM

## Summary
#### Executive Summary

The MoneyNote system is a self-hosted, open-source bookkeeping application designed for individuals and small businesses to manage their finances privately. Built as a layered monolith using Java and the Spring Boot framework, it provides core functionalities such as multi-currency transaction tracking, account management, hierarchical categorization, and collaborative finance management through user groups. The architecture consists of distinct presentation, business, and data access layers communicating with a MySQL database.

#### Key Findings

Analysis of the codebase and architecture reveals several critical challenges and limitations that impact the system's scalability, maintainability, and readiness for the cloud:

*   **Monolithic Architecture**: The application's single-unit design leads to tight coupling between components. This slows down development cycles, complicates deployments, and prevents the independent scaling of specific features.
*   **Stateful Session Management**: The use of a session-scoped bean (`CurrentSession`) to hold user state makes the backend stateful. This requires "sticky sessions" for horizontal scaling, adding complexity to the infrastructure and hindering modern, stateless deployment patterns.
*   **Inefficient File Storage**: Transaction attachments (e.g., receipts) are stored as `LONGBLOB` data directly within the MySQL database. This approach is inefficient, increases database size and load, complicates backups, and does not scale effectively.
*   **Single Points of Failure**: The system relies on a single MySQL database, creating a potential performance bottleneck and a critical point of failure. Additionally, the external currency exchange rate API is only called at application startup, making the system vulnerable to API outages and causing rate data to become stale.

#### Strategic Recommendations

To address these findings and prepare the application for a successful future on Google Cloud, the following strategic actions are recommended:

*   **Adopt a Phased Modernization Approach**: While a low-effort "lift-and-shift" to Compute Engine is possible for an initial cloud entry, a higher-benefit modernization strategy is strongly advised for long-term success. This involves refactoring the application to align with cloud-native principles.
*   **Refactor to a Stateless, Microservices Architecture**: Decompose the monolith into smaller, independent services (e.g., user management, transaction processing). Critically, this includes eliminating the stateful session bean to enable stateless scaling. This architecture is better suited for deployment on modern platforms like **Cloud Run** for serverless execution or **Google Kubernetes Engine** for robust orchestration.
*   **Leverage Managed Google Cloud Services**: Offload operational burdens by migrating from self-managed components to fully managed Google Cloud services. Key migrations include:
    *   **Database**: Migrate the MySQL database to **Cloud SQL for MySQL** to gain automated scalability, backups, and high availability.
    *   **File Storage**: Rearchitect the file attachment feature to use **Cloud Storage**. This involves storing files in a dedicated object storage bucket and only saving a reference ID in the database, a more scalable and cost-effective solution.
    *   **Container Registry and CI/CD**: Centralize container image management in **Artifact Registry** and enhance the CI/CD pipeline using **Cloud Build** for seamless, automated deployments to Google Cloud.
    *   **Security**: Store all sensitive credentials, such as database passwords and API keys, securely in **Secret Manager**.

#### Report Information

##### Estimated Application Metrics (AI-generated)

| Metric | Value |
| :--- | :--- |
| Scanned Lines of Code (LOC) | 13,559 |
| Scanned Files | 242 |
| API Endpoints | 19 |
| Database Tables | 13 |

##### AI-Identified Security Findings

| Metric | Value |
| :--- | :--- |
| Known Vulnerabilities | 3 |
| Critical/High Security Findings | 0% |

##### AI-Analyzed Technical Debt & Legacy

| Metric | Value |
| :--- | :--- |
| Detected technologies stacks | 15 |
| EOL/Unsupported Technologies | 20% |

#### Generation Details

 - **Tool**: Google Cloud Code Modernization Assessment Tool v0.9.0
 - **Modelset**: gemini-2.5-pro
 - **Generated By**: keith_krozario_altostrat_com

#### Command Line Options

The report was generated using the following CLI command:

 ```plaintext
codmod create full \
    -c moneynote-api/ \
    --format markdown \
    -o customized_report_money_note_detailed_journeys.md \
    --context-file context-file.md
 ```

#### User Provided Context

```plaintext
This code runs on Java, and is deployed via Docker.

I want to extract the User Journeys and Features of the code, and build out a requirements document that might have been used to create the code. Focus over the following sections:

1. Monitor of your financial situation.
2. Track your incomes & expenses.
3. Finance Record File
4. Support Multiple Book
5. Support Multiple Currency

Create a section called "User Journeys" in the final report, and populate the section with the following details of each journey. Be as detailed as possible, as you are a senior business analyst analyzing this code base.

### Core Interactions

Describes the Core interactions from the user with the journey, describing each stage from where the user came from.

### Business requirements

Detailed requirements that the program implements in it's functionality.

### Example user flow

An Example user flow that the user goes through. Include at least 1 user flow in this section.



```

#### Notice Regarding AI-Generated Assessment

 - This report leverages advanced AI for analysis, providing rapid, evidence-based insights. Please note that results are AI-derived estimates and may vary between assessments, even for the same codebase. Human review and validation are crucial for all findings and recommendations.

## About this Project
### Assessment Overview
#### Purpose of the System

The MoneyNote system is a comprehensive, open-source bookkeeping solution designed for personal and small business financial management. Its primary purpose is to provide users with a self-hosted, independent platform to track their financial activities without relying on third-party services, ensuring data privacy and control.

The system solves the problem of fragmented and insecure financial tracking by offering a centralized application for managing income, expenses, assets, and liabilities. The value it provides is a clear, detailed, and consolidated view of one's financial health, enabling better decision-making, budgeting, and financial planning.

#### Primary Users

The application is designed for a few distinct user groups, each with specific goals.

| User Group | Description | Goals & Interactions |
| :--- | :--- | :--- |
| **Individual Users** | Individuals managing their personal or household finances. | - Track daily expenses and income. <br> - Monitor account balances (bank accounts, credit cards). <br> - Analyze spending habits through reports. <br> - Manage personal assets and debts. |
| **Self-Employed / Small Business Owners** | Freelancers or owners of small businesses (e.g., retail shops, restaurants) needing a simple bookkeeping tool. | - Separate business finances from personal ones using multiple books. <br> - Record business-related income and expenditures. <br> - Track transactions with specific payees (suppliers, customers). <br> - Export transaction data for accounting purposes. [^1] |
| **Group Collaborators** | Users sharing financial responsibilities, such as families or small teams, within a "Group". [^2] | - Collaboratively manage a shared set of books and accounts. <br> - Have different access levels (Owner, Operator, Guest) to control permissions. [^3] <br> - View and contribute to shared financial records. |

#### Core Functionality

The system offers a robust set of features for comprehensive financial management. The core capabilities are summarized below.

| Feature | High-Level Description |
| :--- | :--- |
| **Account Management** | Create and manage various types of financial accounts, including checking, credit, assets, and debts. Each account tracks a real-time balance. [^4] |
| **Transaction Tracking** | Record detailed financial flows, including expenses, income, transfers between accounts, and balance adjustments. [^5] |
| **Multi-Book System** | Maintain separate "books" to isolate different financial contexts, such as personal vs. business, each with its own categories, tags, and payees. [^6] |
| **Multi-Currency Support** | Manage accounts and transactions in different currencies, with automatic and manual exchange rate handling for accurate reporting. [^7] |
| **Categorization & Tagging** | Organize transactions using a hierarchical system of categories and tags for granular analysis and reporting. [^8] |
| **Reporting & Analytics** | Generate visual reports and statistics on expenses, income, and account balances to gain insights into financial health and spending patterns. [^9] |
| **File Attachments** | Attach files, such as receipts or invoices, to transaction records for complete and verifiable bookkeeping. [^10] |
| **User & Group Management** | Supports multi-user collaboration through a "Group" system, allowing users to be invited and assigned roles for shared financial management. [^2] |

#### User Journeys

The following section outlines the primary user journeys, detailing the interactions, business requirements, and a typical user flow for each.

##### Journey 1: Monitoring Financial Situation

This journey describes how a user assesses their overall financial health by using the system's reporting and dashboard features.

###### Core Interactions

The user logs into the application and navigates to the main dashboard or a dedicated "Reports" section. From here, they can view high-level summaries of their net worth, assets, and liabilities. They can interact with various charts and tables, applying filters for date ranges, specific accounts, or books to drill down into specific areas of interest.

###### Business Requirements

| Requirement ID | Description |
| :--- | :--- |
| **BR-MON-01** | The system must display a high-level overview of the user's total assets, total liabilities, and calculated net worth. [^11] |
| **BR-MON-02** | Reports must be available to visualize expenses and income broken down by category, tag, and payee. [^9] |
| **BR-MON-03** | All report data must be aggregated into the user's default currency, applying the correct exchange rates for multi-currency accounts. [^12] |
| **BR-MON-04** | Users must be able to filter report data by date range, book, account, and other relevant transaction attributes. [^13] |
| **BR-MON-05** | Reports should be presented visually (e.g., pie charts, bar charts) and include percentage breakdowns for easy interpretation. [^14] |
| **BR-MON-06** | The system must allow users to drill down into report segments (e.g., clicking a category to see its sub-categories). [^12] |

###### Example User Flow

1.  **Login and View Dashboard**: The user logs in and lands on the main overview page, which displays their current net worth, total assets, and total debts.
2.  **Navigate to Reports**: The user clicks on the "Reports" tab to explore their finances in more detail.
3.  **Analyze Expenses**: They select the "Expense by Category" report for their "Personal" book for the current month. A pie chart shows that "Food & Drink" is their largest expense category at 40%.
4.  **Drill-Down**: The user clicks on the "Food & Drink" slice of the pie. The report updates to show the sub-categories, revealing that "Restaurants" makes up the majority of that spending.
5.  **Actionable Insight**: Realizing their restaurant spending is higher than expected, the user decides to cook at home more for the rest of the month.

##### Journey 2: Tracking Incomes & Expenses

This journey covers the fundamental task of recording a new financial transaction, such as a daily expense or a monthly salary deposit.

###### Core Interactions

The user selects the appropriate book (e.g., "Personal Finances") and initiates the creation of a new transaction. A form appears where they can specify the transaction type (Expense or Income), the amount, the date, and the account from which the money was spent or deposited. They also select one or more categories and can optionally add tags, a payee, and descriptive notes.

###### Business Requirements

| Requirement ID | Description |
| :--- | :--- |
| **BR-TRK-01** | The system must support the creation of four transaction types: Expense, Income, Transfer, and Adjust. [^5] |
| **BR-TRK-02** | All transactions must be associated with a specific book and a financial account. [^15] |
| **BR-TRK-03** | For Expense and Income types, a transaction must be linked to one or more spending/earning categories and have an amount. [^16] |
| **BR-TRK-04** | The system must allow for transactions to be split across multiple categories, each with its own amount. [^16] |
| **BR-TRK-05** | Upon confirmation of a transaction, the system must automatically update the balance of the associated account(s). [^17] |
| **BR-TRK-06** | Users must be able to edit and delete existing transactions. Deleting a confirmed transaction must reverse the financial change on the associated account balance. [^18] |
| **BR-TRK-07** | Users can mark transactions as "unconfirmed," which prevents them from affecting account balances until confirmed. [^19] |

###### Example User Flow

1.  **Select Context**: The user is in their "Personal Finances" book and wants to record a grocery purchase.
2.  **Initiate Transaction**: They click the "Add Expense" button.
3.  **Fill Form**:
    *   **Account**: They select their "Checking Account".
    *   **Amount**: They enter `85.40`.
    *   **Category**: They select "Groceries".
    *   **Payee**: They select "Local Supermarket".
    *   **Date**: The current date is pre-filled, which is correct.
    *   **Notes**: They add a note: "Weekly grocery run".
4.  **Save Transaction**: The user clicks "Save".
5.  **System Action**: The system creates the transaction record and deducts $85.40 from the balance of the "Checking Account".

##### Journey 3: Managing Finance Record Files

This journey details how a user attaches a digital document, such as a receipt or warranty, to a transaction for record-keeping.

###### Core Interactions

While adding or editing a transaction, the user finds an "Attach File" option. They click it, which opens a file selector to choose a document from their local device. After the upload is complete, an icon or link appears on the transaction details page. The user can later click this link to view or download the attachment.

###### Business Requirements

| Requirement ID | Description |
| :--- | :--- |
| **BR-FILE-01** | The system must allow users to upload and associate one or more files with a balance flow transaction. [^10] |
| **BR-FILE-02** | File uploads must be restricted to supported types, such as PDF, PNG, and JPG, to ensure compatibility and security. [^20] |
| **BR-FILE-03** | The system must store the file's binary data, content type, size, and original filename. [^21] |
| **BR-FILE-04** | Users must be able to view and download attached files from the transaction details screen. [^22] |
| **BR-FILE-05** | Users must have the ability to delete a previously uploaded file from a transaction. [^23] |

###### Example User Flow

1.  **Record a Purchase**: The user creates a new expense transaction for a new laptop costing $1,200 from the "Electronics" category.
2.  **Attach Receipt**: After saving the transaction, they see an "Add Attachment" button on the details page. They click it.
3.  **Upload File**: They select the PDF receipt for the laptop from their computer's "Downloads" folder and upload it.
4.  **Confirmation**: The file appears in a list of attachments for that transaction.
5.  **Future Retrieval**: Six months later, the user needs to file a warranty claim. They search for the laptop transaction, open it, and download the attached PDF receipt to send to the manufacturer.

##### Journey 4: Supporting Multiple Books

This journey illustrates how a user leverages the multi-book feature to manage separate financial areas, such as personal life and a side business.

###### Core Interactions

The user navigates to a "Manage Books" area. Here, they can create a new book from scratch, from a predefined template, or by copying an existing book. Once multiple books exist, the user can easily switch between them from a primary navigation menu. All subsequent actions—adding transactions, creating categories, viewing reports—are performed within the context of the currently selected book.

###### Business Requirements

| Requirement ID | Description |
| :--- | :--- |
| **BR-BOOK-01** | Users must be able to create, edit, and delete multiple "books" to manage finances in logically separate containers. [^6] |
| **BR-BOOK-02** | Each book must have its own unique set of categories, tags, and payees. [^24] |
| **BR-BOOK-03** | Each book must have a configurable name and a default currency. [^25] |
| **BR-BOOK-04** | The system must provide an easy way for users to switch their active context from one book to another. [^26] |
| **BR-BOOK-05** | Users must be able to create new books from pre-defined templates (e.g., "Personal Life," "Restaurant Business"). [^27] |
| **BR-BOOK-06** | Users must be able to create a new book by copying the structure (categories, tags, payees) of an existing book. [^28] |

###### Example User Flow

1.  **Identify Need**: A user who runs a small online store wants to keep its finances separate from their personal spending.
2.  **Create Business Book**: They go to "Manage Books" and click "Add Book". They choose the "Business" template, name the book "My Online Store," and set the default currency.
3.  **Switch Context**: In the main navigation, a dropdown now shows "Personal Finances" and "My Online Store". The user selects "My Online Store".
4.  **Record Business Transaction**: They add an expense for "Shipping Supplies" and categorize it under "Operations". This transaction is only visible within the "My Online Store" book.
5.  **Record Personal Transaction**: Later, they switch back to the "Personal Finances" book to record their dinner expense. This keeps the two financial areas completely separate.

##### Journey 5: Supporting Multiple Currencies

This journey describes how a user who deals with more than one currency manages their accounts and transactions.

###### Core Interactions

When creating a new financial account, the user selects its currency from a dropdown list (e.g., USD, EUR, JPY). When adding a transaction to an account with a foreign currency, the system prompts for the converted value into the book's default currency. All reports and dashboard summaries automatically display aggregated totals in the user's primary default currency.

###### Business Requirements

| Requirement ID | Description |
| :--- | :--- |
| **BR-CUR-01** | The system must allow users to assign a specific currency to each financial account. [^29] |
| **BR-CUR-02** | A list of global currencies and their exchange rates (relative to a base currency like USD) must be maintained by the system. [^30] |
| **BR-CUR-03** | The system should be able to refresh exchange rates from an external API. [^31] |
| **BR-CUR-04** | When a transaction involves a currency different from the book's default currency, the system must capture both the original amount and the converted amount. [^32] |
| **BR-CUR-05** | When transferring funds between accounts with different currencies, the system must capture the source amount and the target (converted) amount. [^17] |
| **BR-CUR-06** | All reports and financial summaries must present data in a single, consistent default currency, performing conversions as needed. [^12] |

###### Example User Flow

1.  **Setup**: A user based in Canada (CAD book currency) receives payment for freelance work in a US-based bank account. They first create a new account in MoneyNote called "US Bank" and set its currency to "USD".
2.  **Record Foreign Income**: They receive a payment of $500 USD. In MoneyNote, they select the "US Bank" account and add an income of `500`.
3.  **Handle Conversion**: The system detects that the account currency (USD) is different from the book currency (CAD) and prompts for the converted amount. The user enters the equivalent value, for example, `650` CAD.
4.  **System State**: The transaction is saved, and the "US Bank" balance increases by $500. The income report for the month, however, shows an increase of 650 CAD, ensuring consistent reporting.
5.  **Transfer Funds**: The user later transfers $100 from their "US Bank" to their "Canadian Chequing" (CAD) account. The transfer form requires them to enter the source amount (`100` USD) and the destination amount (`130` CAD). The system updates both account balances accordingly.

[^1]: BookService.java: exportFlow() - Allows exporting book transactions to an Excel workbook.
[^2]: Group.java: Group Entity - Represents a user group that can contain multiple users and books.
[^3]: UserGroupRelation.java: role - Defines user roles within a group: 1 (Owner), 2 (Operator), 3 (Guest), 4 (Invited).
[^4]: Account.java: Account Entity - Defines different account types such as CHECKING, CREDIT, ASSET, and DEBT.
[^5]: FlowType.java: FlowType Enum - Defines transaction types: EXPENSE, INCOME, TRANSFER, ADJUST.
[^6]: Book.java: Book Entity - Represents a financial ledger that contains its own transactions, categories, and tags.
[^7]: CurrencyService.java: convert() - Handles currency conversion between different currency codes.
[^8]: Category.java: TreeEntity - Categories are structured as a tree, allowing for hierarchical organization.
[^9]: ReportService.java: reportCategory(), reportTag(), reportPayee() - Provides methods to generate various financial reports.
[^10]: FlowFile.java: FlowFile Entity - Represents a file attached to a balance flow transaction.
[^11]: AccountService.java: overview() - Calculates total assets, debts, and net worth.
[^12]: ReportService.java: reportCategory() - Aggregates transaction amounts, converting them to the default currency for reporting.
[^13]: CategoryReportQueryForm.java: buildPredicate() - Constructs query predicates based on user-supplied filters for reporting.
[^14]: ChartVO.java: Chart View Object - A data transfer object for chart data, including x/y values and percentages.
[^15]: BalanceFlow.java: book, account - A transaction entity is linked to both a Book and an Account.
[^16]: BalanceFlowService.java: add() - Logic to handle adding transactions, including checks for categories and amounts.
[^17]: BalanceFlowService.java: confirmBalance() - Updates account balances after a transaction is confirmed, handling expenses, incomes, and transfers.
[^18]: BalanceFlowService.java: remove(), refundBalance() - Logic to delete a transaction and reverse its impact on account balances.
[^19]: BalanceFlow.java: confirm - A boolean flag indicating if the transaction is confirmed and should affect balances.
[^20]: FileValidator.java: isSupportedContentType() - Validates that an uploaded file has a supported content type (PDF, PNG, JPG, JPEG).
[^21]: FlowFile.java: FlowFile Entity fields - Stores data, contentType, size, and originalName of the uploaded file.
[^22]: FlowFileController.java: handleView() - Endpoint to retrieve and view an attached file.
[^23]: FlowFileService.java: remove() - Service method to delete a file attachment.
[^24]: Category.java, Tag.java, Payee.java: Entities - These entities are all linked to a specific Book.
[^25]: Book.java: defaultCurrencyCode - Each book has its own default currency.
[^26]: UserService.java: setDefaultBook() - Allows a user to change their active book context.
[^27]: BookService.java: addByTemplate() - Creates a new book using a predefined JSON template.
[^28]: BookService.java: addByBook() - Creates a new book by copying the structure of an existing one.
[^29]: Account.java: currencyCode - Each account entity has a currency code attribute.
[^30]: currency.json: Resource file - Contains a list of supported currencies and their default rates against USD.
[^31]: CurrencyService.java: refreshCurrency() - Fetches latest exchange rates from an external API (exchangerate-api.com).
[^32]: BalanceFlow.java: amount, convertedAmount - The transaction entity stores both the original and the converted currency amounts.

### Architecture
#### Architectural Overview

The MoneyNote API is designed as a classic, layered monolithic application. This architecture provides a robust and well-organized foundation for the system's bookkeeping functionalities. Its primary goal is to offer a self-hostable, comprehensive solution for personal and small business financial tracking, emphasizing data ownership and independence from third-party services. The architecture is built using the Spring Boot framework, which promotes convention over configuration and facilitates rapid development.

The choice of a monolithic structure allows for straightforward development, testing, and deployment, which is ideal for a project of this scale. All core business logic is encapsulated within a single, deployable artifact, simplifying initial setup and maintenance.

##### Architectural Layers

The system is logically divided into four distinct layers, each with specific responsibilities. This separation of concerns is a cornerstone of the architecture, promoting maintainability and modularity.

| Layer | Role & Responsibilities | Key Technologies & Components |
| :--- | :--- | :--- |
| **Presentation Layer** | Handles all incoming HTTP requests, authenticates users, and delegates tasks to the business layer. It exposes a RESTful API for clients (web and mobile apps) to interact with. | - Spring Web MVC<br>- `*Controller` classes (e.g., `AccountController`, `BalanceFlowController`) [^1]<br>- Jackson for JSON serialization/deserialization |
| **Business Logic Layer** | Contains the core application logic and orchestrates business workflows. It implements the rules for managing accounts, transactions, books, and user groups. | - Spring `Service` Components<br>- `*Service` classes (e.g., `AccountService`, `BalanceFlowService`, `UserService`) [^2]<br>- Custom business logic for financial calculations and state management |
| **Data Access Layer** | Abstracts the communication with the underlying database. It defines interfaces for CRUD (Create, Read, Update, Delete) operations and complex data queries. | - Spring Data JPA & Hibernate<br>- QueryDSL for type-safe dynamic queries [^3]<br>- `*Repository` interfaces (e.g., `AccountRepository`, `BalanceFlowRepository`) [^4]<br>- Custom repository implementation (`BaseRepositoryImpl`) for shared functionality [^5] |
| **Data Layer** | Represents the persistence tier of the application. It consists of the database schema and the data itself. | - MySQL Database (`mysql-connector-j`) [^6]<br>- JPA Entities (e.g., `Account.java`, `User.java`, `BalanceFlow.java`) [^7]<br>- HikariCP for connection pooling |

##### Main Components and Interactions

The application is structured into several feature-oriented packages, each representing a core domain or component. These components work in concert to deliver the application's features.

| Component | Package | Role & Responsibilities |
| :--- | :--- | :--- |
| **User & Group Management** | `cn.biq.mn.user`, `cn.biq.mn.group` | Manages user registration, authentication, and profiles. Supports multi-user collaboration through "Groups". |
| **Authentication & Security** | `cn.biq.mn.security` | Handles user authentication using JSON Web Tokens (JWT) [^8]. A session-scoped bean (`CurrentSession`) holds user state [^9]. |
| **Book Management** | `cn.biq.mn.book` | Core concept for organizing financial records. A user can have multiple books (e.g., "Personal," "Business"). |
| **Account Management** | `cn.biq.mn.account` | Manages financial accounts like Checking, Credit, Assets, and Debts. Tracks balances and properties. |
| **Transaction Flow** | `cn.biq.mn.balanceflow` | The heart of the system. Records all financial transactions: expenses, incomes, transfers, and balance adjustments [^10]. |
| **Categorization** | `cn.biq.mn.category`, `cn.biq.mn.tag` | Allows users to organize transactions using hierarchical categories and tags for detailed reporting. |
| **File Attachments** | `cn.biq.mn.flowfile` | Manages file uploads (e.g., receipts) and associates them with financial transactions [^11]. |
| **Currency Management** | `cn.biq.mn.currency` | Provides multi-currency support by fetching exchange rates from an external API on startup [^12]. |
| **Reporting** | `cn.biq.mn.report` | Generates financial reports and statistics based on user data, such as expenses by category. |
| **CI/CD Automation**| `.github/workflows` | Defines GitHub Actions workflows for automatically building and publishing Docker images to Aliyun Container Registry and Docker Hub, enabling continuous integration and deployment [^13]. |

###### Example Data Flow: Creating an Expense

1.  A user submits a new expense record via the client application.
2.  The `BalanceFlowController` receives the POST request.
3.  The request is delegated to the `BalanceFlowService`.
4.  `BalanceFlowService` validates the data, creates a `BalanceFlow` entity, and associates it with the correct `Book`, `Account`, `Category`, and `Tags`.
5.  If the transaction is confirmed, the `BalanceFlowService` updates the balance of the associated `Account` by calling the `AccountRepository`.
6.  The new `BalanceFlow` and any related entities (like `CategoryRelation`) are persisted to the MySQL database via their respective repositories.
7.  A success response is returned to the user.

##### Technology and Design Patterns

-   **Architectural Style**: **Layered Monolith**. This classic style is evident in the clear separation between presentation, business, and data access layers within a single codebase.
-   **Key Technologies**:
    -   **Backend**: Java 17, Spring Boot 3
    -   **Data Persistence**: Spring Data JPA, Hibernate, QueryDSL, MySQL
    -   **Authentication**: JSON Web Tokens (JWT)
    -   **Deployment**: Docker, with CI/CD pipelines managed by GitHub Actions.
-   **Design Patterns**:
    -   **Model-View-Controller (MVC)**: Spring MVC is used to separate request handling (`Controller`) from business logic (`Service`) and data (`Entity`).
    -   **Data Transfer Object (DTO)**: `*Form`, `*Details`, and `*Vo` classes are used to transfer data between layers and over the network, decoupling the API from the internal data model.
    -   **Repository Pattern**: Implemented by Spring Data JPA, abstracting data persistence logic.
    -   **Dependency Injection**: Heavily used throughout the application via Spring's IoC container to manage object lifecycles and dependencies.

##### Scalability and Resilience

The current architecture supports scalability primarily through **horizontal scaling**. Multiple instances of the application can be deployed as Docker containers and run behind a load balancer.

-   **Database Pooling**: The use of HikariCP ensures efficient management of database connections, which is critical for performance under load.
-   **Containerization**: The application is designed to be deployed via Docker, as defined in the `Dockerfile` and `docker-compose.yml` files [^14]. This simplifies deployment, environment consistency, and scaling.
-   **CI/CD**: Automated build and push workflows to container registries streamline the process of deploying new versions and scaling out instances.

##### Key Challenges and Architectural Limitations

While the architecture is functional and well-suited for its purpose, certain design choices present challenges for future modernization and large-scale deployment.

-   **Monolithic Structure**: The single-unit design leads to tight coupling between components. Any small change requires a full redeployment of the application. This can slow down development cycles and make it difficult to scale individual features independently.
-   **Stateful Session Management**: The use of a `@SessionScope` bean `CurrentSession` introduces state into the backend [^9]. For horizontal scaling to work effectively, a load balancer with "sticky sessions" is required to route a user's requests to the same application instance. This complicates infrastructure and limits stateless scaling.
-   **Single Point of Failure**:
    -   The entire application relies on a single MySQL database, which can become a performance bottleneck and a single point of failure.
    -   Currency exchange rates are fetched from an external API only at application startup [^12]. If this service is unavailable, rates will not be refreshed. Furthermore, the rates can become stale during the application's runtime.
-   **Database Schema Management**: The application uses an SQL script (`1.sql`) that runs on startup to perform schema migrations [^15]. This approach is less robust than dedicated migration tools like Flyway or Liquibase, as it can be prone to errors and is harder to manage and version control.

[^1]: src/main/java/cn/biq/mn/account/AccountController.java: AccountController - Exposes REST endpoints for managing user accounts.
[^2]: src/main/java/cn/biq/mn/account/AccountService.java: AccountService - Implements business logic for account creation, queries, and balance adjustments.
[^3]: build.gradle: "com.querydsl:querydsl-jpa" - Dependency for QueryDSL, used for building type-safe SQL-like queries.
[^4]: src/main/java/cn/biq/mn/account/AccountRepository.java: AccountRepository - Spring Data JPA interface for database operations on the Account entity.
[^5]: src/main/java/cn/biq/mn/base/BaseRepositoryImpl.java: BaseRepositoryImpl - A custom repository implementation providing shared query logic, such as `calcSum`.
[^6]: build.gradle: "com.mysql:mysql-connector-j" - The MySQL JDBC driver dependency, indicating the use of a MySQL database.
[^7]: src/main/java/cn/biq/mn/balanceflow/BalanceFlow.java: BalanceFlow - JPA entity representing a single financial transaction.
[^8]: src/main/java/cn/biq/mn/security/JwtUtils.java: createToken() - Method for generating a JWT for an authenticated user.
[^9]: src/main/java/cn/biq/mn/security/CurrentSession.java: CurrentSession - A @SessionScope bean that holds the current user's session data, including access token and user object.
[^10]: src/main/java/cn/biq/mn/balanceflow/FlowType.java: FlowType - Enum defining the different types of transactions (EXPENSE, INCOME, TRANSFER, ADJUST).
[^11]: src/main/java/cn/biq/mn/flowfile/FlowFile.java: FlowFile - JPA entity for storing file metadata and its binary content, linked to a `BalanceFlow`.
[^12]: src/main/java/cn/biq/mn/currency/CurrencyRemoteDataLoader.java: run() - Method that triggers a refresh of currency exchange rates from an external API upon application startup.
[^13]: .github/workflows/docker-image-ali.yml: docker/build-push-action - GitHub Action step that builds a Docker image and pushes it to Aliyun Container Registry.
[^14]: Dockerfile: Dockerfile - Defines the steps to build the application's Docker image, including setting up the Java environment and copying the JAR file.
[^15]: src/main/java/cn/biq/mn/SqlScriptRunner.java: run() - Component that executes the `1.sql` script upon application startup to update the database schema.

### Technology Stack
The application is built on a modern Java and Spring Boot foundation, containerized with Docker, and configured for automated deployments through GitHub Actions. The technology stack is generally up-to-date, with only minor version updates recommended for some libraries to ensure the latest security patches and bug fixes are applied.

#### Backend Technologies

The backend is a monolithic application powered by the Spring ecosystem, which provides a robust and scalable foundation.

| Technology/Tool Name | Version | Purpose/Role | EOL Status / Replacement |
| :--- | :--- | :--- | :--- |
| Java (OpenJDK) | 17 | Core programming language for the application backend. | **Not EOL**. Java 17 is a Long-Term Support (LTS) release with premier support until September 2026. Sticking with LTS versions like 17 or migrating to the latest LTS (21) is recommended for long-term stability and security. [^1] |
| Spring Boot | 3.2.1 | The primary framework for building the backend RESTful API, managing dependency injection, and simplifying configuration. | **Not EOL**. Version 3.2.x is actively supported. Upgrading to the latest patch release (e.g., 3.2.x) is advisable for ongoing security updates. [^2] |
| Spring Data JPA | 3.2.1 (from Boot) | Provides the data access layer, simplifying database interactions through an Object-Relational Mapping (ORM) pattern. | **Not EOL**. This component is part of the Spring Boot stack and is actively maintained. [^2] |
| Spring Security | 3.2.1 (from Boot) | Manages authentication and authorization, securing API endpoints. | **Not EOL**. This is a core component of the Spring ecosystem and is actively maintained. [^3] |
| Hibernate | ~6.4.1 (from Boot) | The underlying ORM provider for Spring Data JPA, translating Java objects into database records. | **Not EOL**. Its version is managed by the Spring Boot dependency management, ensuring compatibility. |
| QueryDSL | 5.0.0 | A framework used to write type-safe, SQL-like queries in Java, enhancing maintainability and reducing runtime errors. | **Not EOL**. The latest stable version is 5.1.0. An upgrade is recommended for bug fixes and new features, though version 5.0.0 is stable. [^4] |
| java-jwt (Auth0) | 4.2.1 | Library for creating and verifying JSON Web Tokens (JWT) to enable stateless user authentication. | **Not EOL**, but an older version. The current stable version is 4.4.0. **Replacement**: Upgrade to the latest 4.x version to incorporate the latest security patches and bug fixes. [^5] |
| Apache POI | 5.2.2 | A library used for creating and managing Microsoft Excel files, specifically for the data export feature. | **Not EOL**, but an older version. The current version is 5.2.5. **Replacement**: An upgrade to the latest patch version (5.2.5) is recommended for bug fixes and performance improvements. [^6] |

#### Database

The application relies on a traditional relational database for data persistence.

| Technology/Tool Name | Version | Purpose/Role | EOL Status / Replacement |
| :--- | :--- | :--- | :--- |
| MySQL | Determined by Deployment | The relational database system used for storing all application data, including users, accounts, and transactions. | The EOL status depends on the deployed version (e.g., 5.7 is EOL, 8.0+ is active). **Modernization Path**: For Google Cloud migration, **Cloud SQL for MySQL** offers a fully managed, scalable, and secure replacement with minimal code changes. |
| MySQL Connector/J | Runtime Determined | The official JDBC driver that enables the Java application to connect and interact with the MySQL database. | The project uses the modern `mysql-connector-j` artifact, which is **not EOL**. The specific version is managed by Gradle. [^7] |

#### Build, Deployment, and Infrastructure

The project employs a modern CI/CD pipeline for automated builds and deployments using containerization.

| Technology/Tool Name | Version | Purpose/Role | EOL Status / Replacement |
| :--- | :--- | :--- | :--- |
| Gradle | Wrapper-defined | The build automation and dependency management tool for the project. | **Not EOL**. The Gradle Wrapper ensures a consistent build environment across different machines. |
| Docker | N/A | The containerization platform used to package the application and its dependencies into a portable, isolated environment. | **Not EOL**. Docker is the industry standard for containerization and is a key enabler for cloud migration. [^8] |
| GitHub Actions | N/A | CI/CD platform used to automate building the Java application and publishing the resulting Docker images to container registries. | **Not EOL**. This is a fully managed service from GitHub. **Modernization Path**: Can be integrated with Google Cloud services like **Cloud Build** or used to deploy directly to **Cloud Run** or **Google Kubernetes Engine**. [^9] |
| Aliyun Container Registry (ACR) | N/A | A cloud service from Alibaba Cloud used as one of the target container registries for storing Docker images. | **Not EOL**. This is an actively maintained service. **Modernization Path**: For migration to Google Cloud, **Artifact Registry** is the recommended replacement for storing and managing container images and other build artifacts securely. [^10] |
| Docker Hub | N/A | A public container registry used as an alternative destination for the application's Docker images. | **Not EOL**. While suitable for open-source projects, a private registry like **Artifact Registry** is recommended for production workloads on Google Cloud to ensure better security and control. [^11] |

[^1]: .github/workflows/docker-image-ali.yml: setup-java@v1 - Sets up Java environment with version 17.
[^2]: build.gradle: org.springframework.boot version '3.2.1' - Specifies the version for the Spring Boot framework and its managed dependencies.
[^3]: build.gradle: spring-boot-starter-security - Includes Spring Security for handling application security.
[^4]: build.gradle: com.querydsl:querydsl-jpa:5.0.0 - Defines the version for the QueryDSL JPA integration.
[^5]: build.gradle: com.auth0:java-jwt:4.2.1 - Specifies the version for the Java JWT library from Auth0.
[^6]: build.gradle: org.apache.poi:poi:5.2.2 - Includes the Apache POI library for Excel file manipulation.
[^7]: build.gradle: com.mysql:mysql-connector-j - Declares the dependency for the MySQL JDBC driver.
[^8]: Dockerfile: FROM ubuntu:23.04 - Defines the base Docker image for containerizing the application.
[^9]: .github/workflows/docker-image-ali.yml: name: api acr image - Defines a GitHub Actions workflow to build and push Docker images.
[^10]: .github/workflows/docker-image-ali.yml: registry: registry.cn-hangzhou.aliyuncs.com - Specifies Aliyun Container Registry as the destination for Docker images.
[^11]: .github/workflows/docker-image.yml: tags: markliu2018/moneynote-api:latest - Specifies Docker Hub as a destination for the built image.

### APIs and Endpoints
This section outlines the primary user journeys and features supported by the MoneyNote API, framed as a set of business requirements. This analysis is derived from the application's controllers, services, and data models to reconstruct the intended functionality from a user-centric perspective.

#### User Journeys

##### 1. Monitor Financial Situation

This journey focuses on the user's ability to get a high-level overview of their financial health, including their assets, liabilities, and net worth.

###### Core Interactions

The user logs into the application and accesses a primary dashboard or overview screen. This screen presents a consolidated view of their financial standing. The user can see totals for their assets (what they own) and debts (what they owe), along with their calculated net worth. From this overview, they can drill down into specific reports to see the breakdown of these figures, often visualized through charts.

###### Business Requirements

-   **Financial Overview Calculation**: The system must provide an aggregated overview of the user's finances. This includes calculating total assets, total liabilities (debts), and the resulting net worth [^1].
-   **Account-Based Aggregation**:
    -   Total assets shall be the sum of balances from all enabled and included accounts of type `CHECKING` and `ASSET` [^2].
    -   Total liabilities shall be the sum of balances from all enabled and included accounts of type `CREDIT` and `DEBT` [^2].
    -   Net worth is calculated as Total Assets minus Total Liabilities.
-   **Currency Conversion for Reporting**: All account balances must be converted to the user group's default currency before being aggregated to ensure a consistent and accurate financial summary [^1].
-   **Visual Reporting**: The system should offer visual reports, such as pie charts, that break down the composition of assets and debts by individual accounts. This allows users to quickly identify where their wealth and debt are concentrated [^3].
-   **Account Statistics**: The system must provide summary statistics for a filtered list of accounts, including total balance, total credit limit, and remaining credit limit [^4].

###### Example User Flow: Reviewing Monthly Financial Health

1.  **Login and View Dashboard**: The user logs in and lands on the main dashboard.
2.  **API Call for Overview**: The frontend calls the `/api/v1/accounts/overview` endpoint. The `AccountService` calculates the total assets, debts, and net worth by fetching all relevant accounts, converting their balances to the group's default currency, and summing them up.
3.  **Display Key Metrics**: The dashboard displays the three key metrics: Total Assets: $50,000, Total Debts: $15,000, Net Worth: $35,000.
4.  **API Call for Visuals**: The frontend simultaneously calls `/api/v1/reports/balance`. The `ReportService` generates two data sets: one for asset accounts and one for debt accounts, preparing them for chart visualization.
5.  **View Charts**: The user sees two pie charts. The "Assets" chart shows that "Savings Account" makes up 60% of their assets, and "Investment Portfolio" makes up 40%. The "Debts" chart shows "Visa Credit Card" is 70% of their debt and "Student Loan" is 30%.
6.  **Drill Down**: The user clicks on the "Visa Credit Card" slice in the debt chart. The application navigates to the transaction list for that account, filtering to show only the records associated with it.

##### 2. Track Incomes & Expenses

This journey describes the fundamental bookkeeping capability of the application: recording financial transactions.

###### Core Interactions

The user performs a financial transaction in their daily life (e.g., buys coffee, receives a salary) and wants to record it in the application. They open a form dedicated to adding a new transaction, where they can specify if it's an expense, income, or transfer. The user fills in details such as the amount, date, the account used, and categorizes the transaction. Upon saving, the transaction is logged, and the relevant account balance is updated.

###### Business Requirements

-   **Transaction Types**: The system must support the creation of `EXPENSE`, `INCOME`, and `TRANSFER` transaction types (`FlowType`) [^5].
-   **Core Transaction Attributes**: Every transaction record (`BalanceFlow`) must have a date, an associated "book", an amount, and a confirmation status [^6].
-   **Account Linking**: Transactions can be linked to a source `Account`. When a transaction is marked as confirmed, the system must automatically update the account's balance.
    -   Expenses decrease the balance.
    -   Incomes increase the balance.
    -   Transfers decrease the source account and increase the destination account balance [^7].
-   **Categorization**:
    -   Expense and Income transactions must be associated with at least one `Category`.
    -   The system must support splitting a single transaction across multiple categories, with a specific amount allocated to each [^8].
-   **Optional Details**: Users can enrich transactions with optional details, including a title, notes, a `Payee` (merchant or person), and multiple `Tags` for advanced filtering and reporting [^6].
-   **Data Validation**: The system enforces validation rules, such as preventing duplicate categories in a single transaction and limiting the number of categories per transaction [^9].

###### Example User Flow: Recording a Grocery Shopping Trip

1.  **Initiate Transaction**: The user is in their default book, "Personal Finances," and clicks the "Add Expense" button.
2.  **Open Transaction Form**: The UI displays a form. It's pre-populated with the user's default expense account, "Checking Account."
3.  **Enter Details**:
    -   The user leaves the account as "Checking Account."
    -   They set the date to today.
    -   They click on the "Category" field.
4.  **Split Categories**: The grocery bill includes food and household items. The user adds two category entries:
    -   Category: `Food`, Amount: `$55.50`
    -   Category: `Household`, Amount: `$22.00`
5.  **Add Payee and Tag**: The user selects "SuperMart" as the `Payee` and adds a tag: "Weekly Shopping."
6.  **Save Transaction**: The user clicks "Save."
7.  **API Call**: The frontend sends a `POST` request to `/api/v1/balance-flows` with a JSON payload containing the transaction details.
8.  **Backend Processing**:
    -   `BalanceFlowService.add()` receives the request.
    -   It calculates the total amount of the transaction (`$77.50`) by summing the category amounts.
    -   It creates a new `BalanceFlow` entity and associated `CategoryRelation` entities.
    -   Since the transaction is confirmed, `confirmBalance()` is called, which subtracts `$77.50` from the "Checking Account" balance.

##### 3. Finance Record File

This journey allows the user to attach digital files, such as receipts or invoices, to their transaction records for archival and reference.

###### Core Interactions

While creating or editing a transaction, the user decides to upload a corresponding document. They use a file upload interface to select a file from their device. The file is uploaded and linked to the transaction record. Later, when viewing the transaction details, the user can see a list of attached files and can choose to view or download them.

###### Business Requirements

-   **File Attachment**: The system must provide a mechanism to upload one or more files and associate them with a specific `BalanceFlow` (transaction) record [^10].
-   **File Storage**: Uploaded files must be stored within the system. The `FlowFile` entity stores the file content as a `byte[]` array, along with metadata [^11].
-   **File Metadata**: For each uploaded file, the system must store:
    -   Original filename
    -   File size
    -   Content type (MIME type)
    -   Creation timestamp
    -   The user who uploaded it [^11].
-   **Access and Retrieval**:
    -   Users must be able to retrieve a list of all files attached to a transaction [^12].
    -   A secure endpoint must be available to view or download the file content. Access is controlled by checking the file ID and creation timestamp to prevent simple enumeration of URLs [^13].
-   **File Deletion**: Users must be able to delete previously attached files [^14].
-   **Validation**: The system must enforce constraints on file uploads, including file size (max 100MB) and allowed content types (PDF, PNG, JPG, JPEG) [^15] [^16].

###### Example User Flow: Attaching a Receipt to an Expense

1.  **Find Transaction**: The user locates a recent expense record for "New Monitor" with an amount of `$350`.
2.  **Initiate Upload**: On the transaction detail page, the user clicks "Attach File."
3.  **Select and Upload**: A file dialog opens. The user selects `monitor_receipt.pdf` from their computer and confirms.
4.  **API Call for Upload**: The frontend sends a `POST` request to `/api/v1/balance-flows/25/addFile` (where 25 is the transaction ID). The request is of type `multipart/form-data` and contains the file data.
5.  **Backend Processing**: `BalanceFlowService.addFile()` handles the request. It validates the file, creates a `FlowFile` entity, stores the byte data and metadata, and links it to `BalanceFlow` with ID 25.
6.  **View Attachment**: The transaction detail page now shows `monitor_receipt.pdf` in an "Attachments" section.
7.  **Retrieve File**: Clicking on the filename makes a `GET` request to `/api/v1/flow-files/view?id=101&createTime=1672531200000`. The `FlowFileService` validates the request and serves the PDF file to the user's browser.

##### 4. Support Multiple Books

This journey enables users to segregate their financial data into different contexts (e.g., personal, work, family) using "Books."

###### Core Interactions

The user wants to manage finances for a new project separately from their personal budget. They navigate to a "Book Management" area and create a new book. This new book acts as a self-contained ledger with its own set of transactions, categories, tags, and payees. The user can easily switch their active context between different books.

###### Business Requirements

-   **Book Scoping**: The application's data must be partitioned by `Book`. All core data entities, including `BalanceFlow`, `Category`, `Tag`, and `Payee`, must be linked to a single `Book` [^17].
-   **Book Creation**: Users must be able to create new books. Creation can be done in three ways:
    1.  **From Scratch**: A blank book with only a name and default currency [^18].
    2.  **From Template**: A new book pre-populated with categories, tags, and payees from a predefined `BookTemplate` (e.g., "Personal Life," "Small Business") [^19].
    3.  **By Copying**: A new book that duplicates the entire structure (categories, tags, payees) of an existing book [^20].
-   **Default Book**:
    -   Each `User` has a `defaultBook` which is their active book upon login [^21].
    -   Each `Group` also has a `defaultBook`, which serves as a fallback [^22].
    -   Users must be able to change their default book to any other enabled book they have access to [^23].
-   **Data Isolation**: When a user is working within a book, all data entry (new transactions) and reporting are confined to that book's data set.
-   **Data Export**: The system must allow users to export all transaction data from a specific book into an Excel (`.xlsx`) file for external analysis or backup [^24].

###### Example User Flow: Creating and Using a Vacation Book

1.  **Navigate to Book Management**: The user goes to the "Settings" -> "Books" page.
2.  **Create New Book**: The user clicks "New Book" and chooses the "Copy Existing Book" option. They select their "Personal Finances" book as the source.
3.  **Enter Details**: They name the new book "Hawaii Vacation 2024" and set the default currency to "USD."
4.  **API Call**: The frontend sends a `POST` request to `/api/v1/books/copy`.
5.  **Backend Processing**: `BookService.addByBook()` creates the new book and then systematically copies all categories, tags, and payees from the source book to the new one.
6.  **Switch Context**: The user now sees "Hawaii Vacation 2024" in their list of books. They click on it to make it their active book.
7.  **Record Vacation Expense**: The user adds a new expense for "Flight Tickets" for `$1200`. This transaction is now logged exclusively within the "Hawaii Vacation 2024" book and does not appear in their "Personal Finances" book.
8.  **Export for Review**: After the trip, the user navigates to the book's settings and clicks "Export." This triggers a `GET` request to `/api/v1/books/{id}/export`, and the system generates an Excel file with all vacation-related transactions.

##### 5. Support Multiple Currencies

This journey addresses the need for users to manage finances across different currencies.

###### Core Interactions

A user who travels or has international dealings needs to manage accounts in multiple currencies, such as USD, EUR, and JPY. They create accounts specifying the currency for each. When recording a transaction that involves a currency conversion (e.g., withdrawing local currency from a foreign ATM), the application prompts them for the converted amount. All high-level reports and dashboards present a unified view by converting all amounts into a single default currency.

###### Business Requirements

-   **Currency Data**: The system must maintain a list of world currencies and their exchange rates. These rates are initially loaded from a local `currency.json` file and can be updated from an external API service (`exchangerate-api.com`) [^25] [^26].
-   **Currency Assignment**:
    -   Each `Account` entity must have a `currencyCode` (e.g., "USD", "CNY") [^27].
    -   Each `Book` must have a `defaultCurrencyCode` which determines the base currency for its reporting [^28].
-   **Cross-Currency Transaction Handling**:
    -   For `TRANSFER` transactions between two accounts with different currencies, the system requires both the source `amount` and the `convertedAmount` in the destination currency [^29].
    -   For `EXPENSE` or `INCOME` transactions recorded in an account whose currency does not match the book's default currency, the system also requires a `convertedAmount` [^29].
-   **Reporting and Aggregation**: All financial reports, especially high-level overviews (`/accounts/overview`) and balance reports (`/reports/balance`), must convert individual transaction and account amounts into the group's single default currency before aggregation [^1] [^3]. This ensures that sums of money in different currencies are compared on a like-for-like basis.
-   **Rate Calculation**: The application must provide a utility endpoint to calculate the converted value between any two currencies for a given amount [^30].

###### Example User Flow: Recording a Foreign Currency Expense

1.  **Context**: The user's default book currency is "USD," but they have a "Japanese Yen" credit card account (`currencyCode`: "JPY").
2.  **Initiate Expense**: The user adds a new expense while on a trip to Japan. They select their "JPY Credit Card" as the account.
3.  **Enter Transaction Details**:
    -   They enter the amount as `¥10,000` in a category for "Souvenirs."
    -   Because the account currency (JPY) differs from the book's default currency (USD), the UI shows an additional field: "Converted Amount (USD)."
    -   The user enters `$68.50` based on their credit card statement.
4.  **API Call**: The frontend sends a `POST` to `/api/v1/balance-flows`. The payload includes the category amount of `10000` and the converted amount of `68.50`.
5.  **Backend Processing**:
    -   `BalanceFlowService.add()` creates the transaction. It stores `10000` as the `amount` and `68.50` as the `convertedAmount` for the category relation. The total `amount` on the `BalanceFlow` is `10000` and the total `convertedAmount` is `68.50`.
    -   `confirmBalance()` is called, and the balance of the "JPY Credit Card" is reduced by `¥10,000`.
6.  **View Report**: Later, when the user views their monthly expense report in USD, the `ReportService` uses the stored `convertedAmount` of `$68.50` for this transaction in its calculations, correctly adding it to the total spending in USD.

[^1]: AccountService.java: overview() - Calculates total assets, debts, and net worth, converting all balances to the group's default currency.
[^2]: AccountService.java: getAssets(), getDebts() - These methods retrieve accounts based on their type (`CHECKING`, `ASSET`, `CREDIT`, `DEBT`) for financial calculations.
[^3]: ReportService.java: reportBalance() - Generates data for asset and debt breakdown charts, converting amounts to the default currency.
[^4]: AccountService.java: statistics() - Calculates summary statistics for a given set of accounts, including currency conversion.
[^5]: FlowType.java: enum - Defines the supported transaction types: `EXPENSE`, `INCOME`, `TRANSFER`, `ADJUST`.
[^6]: BalanceFlow.java: class - This entity defines the core attributes of a transaction, including its link to a book, amount, time, and optional fields like payee and tags.
[^7]: BalanceFlowService.java: confirmBalance() - This method handles the logic for updating account balances based on the transaction type and amount.
[^8]: CategoryRelationService.java: addRelation() - Manages the creation of relations between a transaction and one or more categories, each with a specific amount.
[^9]: BalanceFlowService.java: checkBeforeAdd() - Performs validation checks before creating a new transaction, such as ensuring categories are not duplicated.
[^10]: BalanceFlowController.java: handleAddFile() - Endpoint for uploading a file and associating it with a transaction.
[^11]: FlowFile.java: class - Entity that stores the uploaded file's binary data and metadata.
[^12]: BalanceFlowController.java: handleFiles() - Endpoint to retrieve the list of files for a given transaction.
[^13]: FlowFileService.java: getFile() - Service method that retrieves a file's content after validating the ID and a timestamp for security.
[^14]: FlowFileController.java: handleDelete() - Endpoint for deleting a file attachment.
[^15]: application.properties: spring.servlet.multipart.max-file-size - Defines the maximum file size for uploads.
[^16]: FileValidator.java: isSupportedContentType() - This method checks if the uploaded file's MIME type is one of the allowed formats (pdf, png, jpg, jpeg).
[^17]: Book.java: class - The `Book` entity has `@OneToMany` relationships with `Category`, `Tag`, and `Payee`, establishing its role as a data container.
[^18]: BookService.java: add() - The basic method for creating a new, empty book.
[^19]: BookService.java: addByTemplate() - Logic for creating a new book based on a `BookTemplate` JSON definition.
[^20]: BookService.java: addByBook() - Logic for creating a new book by copying the structure of an existing one.
[^21]: User.java: defaultBook - The `User` entity has a direct relationship to their default `Book`.
[^22]: Group.java: defaultBook - The `Group` entity has a default book, which acts as a fallback.
[^23]: UserService.java: setDefaultBook() - Allows the current user to change their active default book.
[^24]: BookService.java: exportFlow() - This method generates a `Workbook` object (Excel file) containing all transactions for a given book.
[^25]: CurrencyDataLoader.java: run() - Loads initial currency data from `currency.json` at application startup.
[^26]: CurrencyService.java: refreshCurrency() - Fetches the latest exchange rates from an external API.
[^27]: Account.java: currencyCode - Each account entity includes a field to specify its currency.
[^28]: Book.java: defaultCurrencyCode - Each book entity has a default currency used for reporting within that book.
[^29]: BalanceFlowService.java: add() - This service method contains the core logic that checks for currency differences and requires the `convertedAmount` field when necessary.
[^30]: CurrencyController.java: handleCalc() - An API endpoint that provides on-the-fly currency conversion calculations.

### Data Layer
The data layer of the MoneyNote API is built on a relational data model, implemented using **Spring Data JPA** as the Object-Relational Mapping (ORM) framework. It leverages **QueryDSL** for constructing type-safe, dynamic queries, which provides a flexible and powerful way to filter and retrieve data. The application is configured to connect to a **MySQL** database, as specified by the `mysql-connector-j` dependency and the JDBC connection string in the configuration files [^1].

Data persistence is managed through a set of well-defined JPA entities, each corresponding to a table in the database. A custom `BaseRepository` interface, implemented by `BaseRepositoryImpl` [^2], extends the standard JPA repository functionality to include custom query logic, such as `calcSum` for aggregations, which is powered by `JPAQueryFactory` from QueryDSL.

At startup, the application executes a SQL script (`1.sql`) to perform schema migrations, such as updating enum-like integer codes and altering column data types to ensure database consistency with the application logic [^3].

#### Data Model

The database schema is designed around core concepts of personal finance management: users, groups, books, accounts, and transactions (balance flows). Relationships are established to support multi-user, multi-book, and multi-currency bookkeeping. The following tables describe the primary entities and their relationships.

##### `t_user_user`
Stores user profile information and their default settings.

| Column | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**, Auto-incremented. |
| `username` | `VARCHAR(16)` | Unique, Nullable. The user's login name. |
| `nick_name` | `VARCHAR(16)` | The user's display name. |
| `password` | `VARCHAR(64)` | Hashed password for authentication. |
| `telephone` | `VARCHAR(16)` | User's phone number. |
| `email` | `VARCHAR(32)` | User's email address. |
| `register_ip` | `VARCHAR(128)` | IP address used during registration. |
| `default_group_id` | `INTEGER` | **Foreign Key** -> `t_user_group(id)`. The user's default group. |
| `default_book_id` | `INTEGER` | **Foreign Key** -> `t_user_book(id)`. The user's default ledger book. |
| `enable` | `BOOLEAN` | `NOT NULL`. Flag to enable or disable the user. |
| `register_time` | `BIGINT` | `NOT NULL`. Timestamp of user registration. |
| `headimgurl` | `VARCHAR(256)`| URL for the user's profile picture. |

**Entity:** `User.java` [^4]

---
##### `t_user_group`
Represents a group of users who can share bookkeeping data. Each group has its own settings.

| Column | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**, Auto-incremented. |
| `name` | `VARCHAR(64)` | `NOT NULL`. The name of the group. |
| `notes` | `VARCHAR(1024)` | Descriptive notes for the group. |
| `enable` | `BOOLEAN` | `NOT NULL`. Flag to enable or disable the group. |
| `creator_id` | `INTEGER` | **Foreign Key** -> `t_user_user(id)`. The user who created the group. |
| `default_book_id` | `INTEGER` | **Foreign Key** -> `t_user_book(id)`. The group's default ledger book. |
| `default_currency_code` | `VARCHAR(8)` | `NOT NULL`. The default currency for the group. |

**Entity:** `Group.java` [^5]

---
##### `t_user_user_group_relation`
A junction table defining the many-to-many relationship between users and groups, including role-based access control.

| Column | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**, Auto-incremented. |
| `user_id` | `INTEGER` | **Foreign Key** -> `t_user_user(id)`. Part of a composite unique key. |
| `group_id` | `INTEGER` | **Foreign Key** -> `t_user_group(id)`. Part of a composite unique key. |
| `role` | `INTEGER` | `NOT NULL`. User's role in the group (e.g., Owner, Operator, Guest). |

**Entity:** `UserGroupRelation.java` [^6]

---
##### `t_user_book`
Represents a single ledger or "book" for tracking finances. It is associated with a group.

| Column | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**, Auto-incremented. |
| `name` | `VARCHAR(64)` | `NOT NULL`. The name of the book. |
| `group_id` | `INTEGER` | `NOT NULL`, **Foreign Key** -> `t_user_group(id)`. The group this book belongs to. |
| `notes` | `VARCHAR(1024)` | Descriptive notes for the book. |
| `enable` | `BOOLEAN` | `NOT NULL`. Flag to enable or disable the book. |
| `default_expense_account_id` | `INTEGER` | **Foreign Key** -> `t_user_account(id)`. Default account for expenses. |
| `default_income_account_id` | `INTEGER` | **Foreign Key** -> `t_user_account(id)`. Default account for income. |
| `default_transfer_from_account_id`| `INTEGER` | **Foreign Key** -> `t_user_account(id)`. Default source account for transfers. |
| `default_transfer_to_account_id`| `INTEGER` | **Foreign Key** -> `t_user_account(id)`. Default destination account for transfers. |
| `default_expense_category_id` | `INTEGER` | **Foreign Key** -> `t_user_category(id)`. Default category for expenses. |
| `default_income_category_id` | `INTEGER` | **Foreign Key** -> `t_user_category(id)`. Default category for income. |
| `default_currency_code` | `VARCHAR(8)` | `NOT NULL`. The default currency for this book. |
| `export_at` | `BIGINT` | Timestamp of the last data export operation. |
| `ranking` | `INTEGER` | Used for sorting books. |

**Entity:** `Book.java` [^7]

---
##### `t_user_account`
Represents a financial account, such as a bank account, credit card, or asset.

| Column | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**, Auto-incremented. |
| `name` | `VARCHAR(64)` | `NOT NULL`. The name of the account. |
| `group_id` | `INTEGER` | `NOT NULL`, **Foreign Key** -> `t_user_group(id)`. The group this account belongs to. |
| `type` | `INTEGER` | `NOT NULL`. Type of account (e.g., Checking, Credit, Asset, Debt). |
| `notes` | `VARCHAR(1024)` | Descriptive notes for the account. |
| `enable` | `BOOLEAN` | `NOT NULL`. Flag to enable or disable the account. |
| `no` | `VARCHAR(32)` | Account number or card number. |
| `balance` | `DECIMAL(20,2)` | `NOT NULL`. The current balance of the account. |
| `include` | `BOOLEAN` | `NOT NULL`. Whether to include this account in net worth calculations. |
| `can_expense` | `BOOLEAN` | `NOT NULL`. Whether this account can be used for expenses. |
| `can_income` | `BOOLEAN` | `NOT NULL`. Whether this account can receive income. |
| `can_transfer_from` | `BOOLEAN` | `NOT NULL`. Whether transfers can originate from this account. |
| `can_transfer_to` | `BOOLEAN` | `NOT NULL`. Whether transfers can be made to this account. |
| `currency_code` | `VARCHAR(8)` | `NOT NULL`. The currency of the account. |
| `initial_balance` | `DECIMAL(20,2)` | The balance when the account was created. |
| `credit_limit` | `DECIMAL(20,2)` | Credit limit for credit-type accounts. |
| `bill_day` | `INTEGER` | Billing day of the month for credit-type accounts. |
| `apr` | `DECIMAL(4,4)` | Annual Percentage Rate for credit/debt accounts. |
| `ranking` | `INTEGER` | Used for sorting accounts. |

**Entity:** `Account.java` [^8]

---
##### `t_user_balance_flow`
This is the central table for all financial transactions (flows), including expenses, incomes, transfers, and adjustments.

| Column | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**, Auto-incremented. |
| `book_id` | `INTEGER` | `NOT NULL`, **Foreign Key** -> `t_user_book(id)`. |
| `type` | `INTEGER` | `NOT NULL`. Type of flow (Expense, Income, Transfer, Adjust). |
| `amount` | `DECIMAL(15,2)` | `NOT NULL`. The transaction amount. |
| `converted_amount` | `DECIMAL(15,2)` | Amount converted to the book's default currency. |
| `account_id` | `INTEGER` | **Foreign Key** -> `t_user_account(id)`. The source account. |
| `to_id` | `INTEGER` | **Foreign Key** -> `t_user_account(id)`. The destination account (for transfers). |
| `create_time` | `BIGINT` | `NOT NULL`. Timestamp of the transaction. |
| `title` | `VARCHAR(32)` | A custom title for the transaction. |
| `notes` | `VARCHAR(1024)` | Detailed notes. |
| `creator_id` | `INTEGER` | `NOT NULL`, **Foreign Key** -> `t_user_user(id)`. |
| `group_id` | `INTEGER` | `NOT NULL`, **Foreign Key** -> `t_user_group(id)`. |
| `payee_id` | `INTEGER` | **Foreign Key** -> `t_user_payee(id)`. |
| `confirm` | `BOOLEAN` | `NOT NULL`. Whether the transaction is confirmed and affects balances. |
| `include` | `BOOLEAN` | Whether to include this transaction in reports. |
| `insert_at` | `BIGINT` | `NOT NULL`, Not updatable. System timestamp of record creation. |

**Entity:** `BalanceFlow.java` [^9]

---
##### `t_user_category` & `t_user_tag`
These tables store hierarchical categories and tags for classifying transactions. They share a similar tree structure.

| Column | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**, Auto-incremented. |
| `name` | `VARCHAR(64)` | `NOT NULL`. Name of the category/tag. |
| `book_id` | `INTEGER` | `NOT NULL`, **Foreign Key** -> `t_user_book(id)`. |
| `parent_id` | `INTEGER` | **Foreign Key** -> self-referencing `id`. Establishes the hierarchy. |
| `level` | `INTEGER` | `NOT NULL`. Depth of the node in the tree. |
| `notes` | `VARCHAR(4096)` | Descriptive notes. |
| `enable` | `BOOLEAN` | `NOT NULL`. |
| `type` (`t_user_category` only) | `INTEGER` | `NOT NULL`. Type of category (Expense or Income). |
| `can_expense`, `can_income`, `can_transfer` (`t_user_tag` only) | `BOOLEAN` | `NOT NULL`. Flags to control where a tag can be applied. |
| `ranking` | `INTEGER` | Sort order. |

**Entities:** `Category.java` [^10], `Tag.java` [^11]

---
##### Other Supporting Tables

-   **`t_user_payee`**: Stores information about payees (merchants, individuals) associated with transactions. Belongs to a `Book`. (Entity: `Payee.java`)
-   **`t_user_category_relation`**: Junction table for the many-to-many relationship between `BalanceFlow` and `Category`. It stores the amount allocated to each category in a multi-category transaction. (Entity: `CategoryRelation.java`)
-   **`t_user_tag_relation`**: Junction table for the many-to-many relationship between `BalanceFlow` and `Tag`. (Entity: `TagRelation.java`)
-   **`t_flow_file`**: Stores file attachments for `BalanceFlow` records, with a `LONGBLOB` column for the file data. (Entity: `FlowFile.java`)
-   **`t_user_note_day`**: Tracks user-specific recurring events or reminders. (Entity: `NoteDay.java`)

#### Data Access and Transaction Analysis

The application follows a standard service-repository pattern. Service classes are annotated with `@Transactional`, ensuring that public methods run within a database transaction. This provides atomicity for complex operations that involve multiple database writes.

##### Data Access Patterns
- **Read Operations**: Queries are predominantly handled through `*QueryForm` objects that construct dynamic `Predicate` instances for QueryDSL. This pattern is used across the application for filtering lists of accounts, transactions, categories, etc. For example, `BalanceFlowService.query()` uses `BalanceFlowQueryForm` to filter transactions by date, type, amount, and associated entities [^12].
- **Write Operations**: New data is created by mapping `*AddForm` DTOs to entities and saving them via the repository (e.g., `AccountService.add()`). Updates follow a "read-modify-write" pattern, where an entity is fetched, modified, and then saved.
- **Aggregate Operations**: The `ReportService` makes heavy use of aggregate functions to generate financial reports. It leverages the custom `calcSum` method to calculate sums of `convertedAmount` for expenses and incomes, grouped by category, tag, or payee [^13].

##### Transaction Analysis
Key business operations are managed as atomic transactions to maintain data integrity, especially when multiple entities are involved.

| Transaction Type | Description & Key Operations | Involved Entities / Tables |
| :--- | :--- | :--- |
| **Read-Write** | **Add Balance Flow** (`BalanceFlowService.add` [^14]) | - **Write**: Inserts new records into `t_user_balance_flow`, `t_user_category_relation`, and `t_user_tag_relation`. <br>- **Read-Modify-Write**: If confirmed, reads the current balance from `t_user_account`, calculates the new balance, and updates it. For transfers, this happens for two accounts. |
| **Read-Write** | **Adjust Account Balance** (`AccountService.adjustBalance` [^15]) | - **Read-Modify-Write**: Reads the current balance from `t_user_account`, calculates the difference, and updates the balance to the new value. <br>- **Write**: Inserts a new `ADJUST` type record into `t_user_balance_flow` to log the adjustment. |
| **Read-Write** | **Update Balance Flow** (`BalanceFlowService.update` [^16]) | - **Complex**: This operation is implemented by deleting the old flow record (which triggers a balance refund) and creating a new one with the updated details. This ensures balance consistency without complex differential logic. Involves `DELETE` and `INSERT` on flow/relation tables and `UPDATE` on `t_user_account`. |
| **Read-Only** | **Generate Category Report** (`ReportService.reportCategory` [^17]) | - **Read & Aggregate**: Fetches all `CategoryRelation` records matching the query filters. It then processes this data in-memory to group amounts by parent categories and calculates totals and percentages. |

#### Data Flow Between Components

Data flows through the application in a typical three-tier architecture: Controller -> Service -> Repository. DTOs (Data Transfer Objects) are used to transfer data between the web layer and the service layer, while JPA entities are used between the service and data access layers.

| Source | Destination | Operation | Description |
| :--- | :--- | :--- | :--- |
| **API**: `POST /balance-flows` (`BalanceFlowController.handleAdd`) | **Database**: `t_user_balance_flow`, `t_user_category_relation`, `t_user_account` | Insert & Update | The JSON payload (`BalanceFlowAddForm`) is passed to `BalanceFlowService.add`. This service creates and saves the `BalanceFlow` and its related entities. It also calls `confirmBalance` to update the balances in the `t_user_account` table. |
| **Database**: `t_user_account`, `t_user_group` | **API**: `GET /accounts` (`AccountController.handleQuery`) | Read | The `AccountService.query` method uses `AccountQueryForm` to build a query. It fetches a page of `Account` entities, converts them to `AccountDetails` DTOs (including calculating converted balances), and returns them as a JSON response. |
| **Database**: `t_user_balance_flow`, `t_user_category_relation` | **API**: `GET /reports/expense-category` (`ReportController.handleExpenseCategory`) | Read & Aggregate | `ReportService.reportCategory` fetches all relevant `CategoryRelation` records. It then aggregates the `convertedAmount` for each top-level category and their children to build a `ChartVO` list, which is returned as a JSON response. |
| **API**: `POST /accounts/{id}/adjust` (`AccountController.handleAdjust`) | **Database**: `t_user_account`, `t_user_balance_flow` | Read-Modify-Write | The `AdjustBalanceAddForm` is processed by `AccountService.adjustBalance`. It updates the balance of the specified account and inserts a new `BalanceFlow` record of type `ADJUST` to document the change. |

[^1]: src/main/resources/application.properties: spring.datasource.url - Defines the JDBC connection string for a MySQL database.
[^2]: src/main/java/cn/biq/mn/base/BaseRepositoryImpl.java: BaseRepositoryImpl - Implements custom repository logic using JPAQueryFactory for QueryDSL.
[^3]: src/main/java/cn/biq/mn/SqlScriptRunner.java: run - Executes the `1.sql` script on application startup.
[^4]: src/main/java/cn/biq/mn/user/User.java: @Entity - Defines the `User` entity, mapped to the `t_user_user` table.
[^5]: src/main/java/cn/biq/mn/group/Group.java: @Entity - Defines the `Group` entity, mapped to the `t_user_group` table.
[^6]: src/main/java/cn/biq/mn/user/UserGroupRelation.java: @Entity - Defines the `UserGroupRelation` join entity.
[^7]: src/main/java/cn/biq/mn/book/Book.java: @Entity - Defines the `Book` entity, mapped to the `t_user_book` table.
[^8]: src/main/java/cn/biq/mn/account/Account.java: @Entity - Defines the `Account` entity, mapped to the `t_user_account` table.
[^9]: src/main/java/cn/biq/mn/balanceflow/BalanceFlow.java: @Entity - Defines the `BalanceFlow` entity, mapped to `t_user_balance_flow`.
[^10]: src/main/java/cn/biq/mn/category/Category.java: @Entity - Defines the `Category` entity, mapped to `t_user_category`.
[^11]: src/main/java/cn/biq/mn/tag/Tag.java: @Entity - Defines the `Tag` entity, mapped to `t_user_tag`.
[^12]: src/main/java/cn/biq/mn/balanceflow/BalanceFlowQueryForm.java: buildPredicate - Constructs a dynamic query for filtering balance flows.
[^13]: src/main/java/cn/biq/mn/report/ReportService.java: reportCategory - Aggregates financial data to generate reports.
[^14]: src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java: add - Service method for adding a new balance flow transaction.
[^15]: src/main/java/cn/biq/mn/account/AccountService.java: adjustBalance - Service method for adjusting an account's balance.
[^16]: src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java: update - Implements the update logic by removing the old flow and adding a new one.
[^17]: src/main/java/cn/biq/mn/report/ReportService.java: reportCategory - Fetches and aggregates data for category-based reports.

## Assessment Findings
### Security and Compliance
This section outlines the primary user journeys and features of the MoneyNote application, framed as a requirements document that could have guided its development. Each journey is detailed from the perspective of a user interacting with the system, followed by the specific business requirements the codebase implements and an example user flow.

#### User Journeys

##### 1\. Monitor Financial Situation

This journey describes how a user gains a high-level understanding of their overall financial health by viewing aggregated assets, liabilities, and net worth.

###### Core Interactions

The user navigates to a primary dashboard or overview screen within the application. This action triggers the system to fetch and process data from all relevant financial accounts. The system then presents a consolidated view, showing the user their total assets (what they own), total liabilities (what they owe), and their resulting net worth. This view serves as a financial snapshot, allowing the user to quickly assess their position without delving into individual transaction details.

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| FIN-MON-01 | The system must provide a financial overview that summarizes the user's total assets, total debts, and net worth [^1]. | `AccountService.java`: `overview()` |
| FIN-MON-02 | Accounts must be categorized to distinguish between assets and liabilities. The system defines `CHECKING` and `ASSET` as asset types, and `CREDIT` and `DEBT` as liability types [^2]. | `AccountType.java`, `AccountService.java`: `getAssets()`, `getDebts()` |
| FIN-MON-03 | The financial summary must aggregate balances from all accounts that are marked for inclusion in reports. Users must have the ability to exclude specific accounts from this summary view [^3]. | `Account.java`: `include` field; `AccountService.java`: `getAssets()`, `getDebts()` |
| FIN-MON-04 | All monetary values in the summary must be converted to the user's group-defined default currency to provide a consistent and unified view, regardless of the individual account's currency [^4]. | `AccountService.java`: `overview()`, `CurrencyService.java`: `convert()` |
| FIN-MON-05 | The system must provide a separate statistics view that calculates total balance, total credit limit, and remaining credit limit across a filtered set of accounts [^5]. | `AccountService.java`: `statistics()` |

###### Example User Flow: Checking Net Worth

1.  **Login and Navigation**: The user, Alex, logs into the MoneyNote application. He lands on the main dashboard.
2.  **View Overview**: The dashboard automatically displays a "Financial Overview" widget.
3.  **System Processing**:
    *   The frontend calls the `/accounts/overview` endpoint.
    *   The backend `AccountService` invokes the `getAssets()` and `getDebts()` methods [^2]. These methods query for all `Account` entities that are `enabled` and marked with `include=true`.
    *   The service iterates through the asset and debt accounts, using the `CurrencyService` to convert each account's balance to the user's default group currency (e.g., USD) [^4].
    *   The `overview()` method calculates the sum of all converted asset balances, the sum of all converted debt balances, and the net worth (Assets - Debts).
4.  **Display**: The UI displays the following:
    *   **Total Assets**: $55,000
    *   **Total Debts**: $15,000
    *   **Net Worth**: $40,000

---

##### 2\. Track Incomes & Expenses

This journey covers the fundamental user activity of recording, categorizing, and reviewing their daily financial transactions.

###### Core Interactions

The user initiates the process of adding a new financial transaction. They select the transaction type (e.g., "Expense" or "Income"), input the amount, and choose which account was used. To add context, they can assign one or more categories, add descriptive tags, specify a payee, and write notes. After saving, the transaction appears in a historical log. Users can later browse this log, apply filters to find specific transactions, and view reports based on this data.

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| TRACK-TX-01 | The system must allow users to create financial transactions and classify them by `FlowType`: `EXPENSE`, `INCOME`, `TRANSFER`, or `ADJUST` [^6]. | `BalanceFlow.java`, `FlowType.java` |
| TRACK-TX-02 | Every transaction must be associated with a specific `Book` and have a creation time, amount, and an optional title and notes [^7]. | `BalanceFlow.java`, `BalanceFlowAddForm.java` |
| TRACK-TX-03 | Income and Expense transactions must be linked to a financial `Account`. The system must update the account's balance upon confirmation of the transaction [^8]. | `BalanceFlowService.java`: `confirmBalance()` |
| TRACK-TX-04 | Transactions can be enriched with additional data, including associations with one or more `Category` entities, a `Payee`, and a set of `Tag` entities [^9]. | `BalanceFlow.java`, `CategoryRelation.java`, `TagRelation.java` |
| TRACK-TX-05 | For transactions involving multiple categories, the system must support splitting the total amount across different categories [^10]. | `CategoryRelationForm.java` (list), `BalanceFlowService.java`: `add()` |
| TRACK-TX-06 | The system must provide a paginated and filterable view of all transactions. Filters must include date range, transaction type, account, category, and tags [^11]. | `BalanceFlowQueryForm.java`, `BalanceFlowService.java`: `query()` |
| TRACK-TX-07 | Transactions can be marked as "unconfirmed," in which case they will not affect account balances until confirmed by the user [^12]. | `BalanceFlow.java`: `confirm` field; `BalanceFlowService.java`: `confirm()` |

###### Example User Flow: Recording a Grocery Shopping Expense

1.  **Initiate Transaction**: User Priya clicks the "Add New" button and selects "Expense".
2.  **Enter Details**:
    *   She enters `75.40` in the amount field.
    *   She selects her "Chase Debit" `Account`.
    *   She chooses the `Category`: "Groceries".
    *   She selects the `Payee`: "Local Supermarket".
    *   She adds a `Tag`: "#weekly-shop".
    *   The transaction date defaults to the current day.
3.  **Save Transaction**: Priya clicks "Save".
4.  **System Processing**:
    *   The frontend sends a `POST` request to `/balance-flows` with the data in a `BalanceFlowAddForm` object.
    *   `BalanceFlowService.add()` is called. It creates a new `BalanceFlow` entity [^7].
    *   It links the entity to the selected `Book`, `Account`, `Category`, `Payee`, and `Tag`.
    *   Because the transaction is confirmed, `confirmBalance()` is called, which subtracts `75.40` from the balance of the "Chase Debit" account [^8].
5.  **Confirmation**: The transaction now appears at the top of Priya's transaction list.

---

##### 3\. Finance Record File

This journey allows users to attach digital files, such as receipts or invoices, to their transaction records for archival and reference purposes.

###### Core Interactions

When creating or editing a transaction, the user sees an option to "Add Attachment". The user selects a file from their local device (e.g., a photo of a receipt). The file is uploaded to the server and linked to the specific transaction. When viewing the transaction details later, the user can see a list of attached files, view them directly in the browser if they are images, or download them.

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| FILE-ATTACH-01 | Users must be able to upload and attach one or more files to any `BalanceFlow` transaction record [^13]. | `BalanceFlowController.java`: `handleAddFile()` |
| FILE-ATTACH-02 | The system must validate uploaded files, restricting them to supported content types such as `application/pdf`, `image/png`, `image/jpg`, and `image/jpeg` [^14]. | `ValidFile.java`, `FileValidator.java` |
| FILE-ATTACH-03 | File data must be stored securely as a binary large object (`LONGBLOB`) in the database [^15]. | `FlowFile.java`: `data` field with `@Lob` annotation |
| FILE-ATTACH-04 | The system must store essential metadata for each file, including its original filename, content type, size, and creation time [^16]. | `FlowFile.java` |
| FILE-ATTACH-05 | Users must be able to retrieve a list of all files attached to a transaction [^17]. | `BalanceFlowController.java`: `handleFiles()` |
| FILE-ATTACH-06 | The system must provide a secure endpoint to view or download an attached file, using a combination of the file's ID and creation time as a security measure [^18]. | `FlowFileController.java`: `handleView()`, `FlowFileViewForm.java` |

###### Example User Flow: Attaching a Warranty PDF to a Purchase

1.  **Find Transaction**: User John locates the expense transaction for a new laptop he purchased.
2.  **Upload File**: He clicks on the transaction to open the details view, then clicks "Add Attachment".
3.  **Select File**: A file dialog opens. He selects `laptop_warranty.pdf` from his computer.
4.  **System Processing**:
    *   The file is uploaded via a `POST` request to the `/balance-flows/{id}/addFile` endpoint.
    *   The `FileValidator` ensures the file type is supported [^14].
    *   `BalanceFlowService.addFile()` creates a `FlowFile` entity, populates it with the file's binary data and metadata, and links it to the laptop's `BalanceFlow` record [^13].
5.  **View Attachment**: The transaction details page now lists `laptop_warranty.pdf` as an attachment. John can click on it, which directs him to the `/flow-files/view?id=...&createTime=...` endpoint to open the PDF.

---

##### 4\. Support Multiple Books

This journey describes how users can maintain separate, parallel sets of financial records for different purposes, such as personal vs. business finances.

###### Core Interactions

The user decides they need to segregate their finances. They navigate to a "Manage Books" section and create a new "Book". They can create one from scratch, copy an existing book's structure, or use a predefined template. Each book functions as a self-contained ledger with its own default currency, categories, tags, and transaction history. The user can switch their active view between books at any time, and all subsequent actions and views will be scoped to the currently selected book.

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| MULTI-BOOK-01 | The system must allow a user to create, manage, and switch between multiple independent ledgers, known as `Book` entities [^19]. | `Book.java`, `BookController.java` |
| MULTI-BOOK-02 | Each `Book` must be scoped to a `Group` and have its own set of `Category`, `Tag`, and `Payee` entities, ensuring separation of concerns [^20]. | `Category.java`, `Tag.java`, `Payee.java` (all link to a `Book`) |
| MULTI-BOOK-03 | All `BalanceFlow` transactions must belong to a single `Book` [^7]. | `BalanceFlow.java`: `book` field |
| MULTI-BOOK-04 | The application must maintain the user's currently active `Book` in their session, ensuring all data displays and operations are correctly scoped [^21]. | `CurrentSession.java`: `book` field; `AuthInterceptor.java` |
| MULTI-BOOK-05 | Users must be able to change their default/active `Book` at any time [^22]. | `UserController.java`: `handleSetDefaultBook()` |
| MULTI-BOOK-06 | The system must facilitate the creation of new books by providing predefined templates (e.g., "Personal Finance," "Restaurant") or by copying the structure of an existing book [^23]. | `BookService.java`: `addByTemplate()`, `addByBook()` |

###### Example User Flow: Creating and Using a Business Book

1.  **Create New Book**: User Sarah, a freelance designer, decides to separate her business finances. She goes to "Settings" -> "Books" and clicks "Create New Book".
2.  **Use Template**: She chooses to create a book from the "Daily Life" template to get a standard set of categories. She names the new book "Freelance Design".
3.  **System Processing**:
    *   The `BookService.addByTemplate()` method is called [^23].
    *   A new `Book` entity named "Freelance Design" is created.
    *   The service reads the `book_tpl.json` file, finds the "Daily Life" template, and programmatically creates all associated `Category` and `Tag` entities, linking them to the new "Freelance Design" book.
4.  **Switch Active Book**: Sarah now has two books: "Personal" and "Freelance Design". She selects "Freelance Design" from a dropdown menu. The application calls `/setDefaultBook/{id}` to update her session.
5.  **Scoped View**: The dashboard refreshes. All transactions, accounts, and reports shown are now exclusively from the "Freelance Design" book. When she goes to add a new transaction, the category options are the ones created for this new book.

---

##### 5\. Support Multiple Currencies

This journey enables users to manage accounts and transactions in different currencies and view consolidated reports in a single, preferred currency.

###### Core Interactions

A user with international dealings creates financial accounts in multiple currencies (e.g., a bank account in USD and another in EUR). When recording a transaction in a non-default currency, the system captures both the original amount and its equivalent value in the user's primary currency. All high-level reports and dashboards automatically convert and aggregate these varied currencies into a unified view, providing a clear financial picture without manual calculations.

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| MULTI-CUR-01 | The system must allow each `Account` to be associated with a specific currency code (e.g., "USD", "EUR") [^24]. | `Account.java`: `currencyCode` field |
| MULTI-CUR-02 | Each `Book` must define a `defaultCurrencyCode` that serves as the base for all consolidated reporting [^25]. | `Book.java`: `defaultCurrencyCode` field |
| MULTI-CUR-03 | For transactions where the account currency differs from the book's default currency, the system must store both the original `amount` and a `convertedAmount` in the book's default currency [^26]. | `BalanceFlow.java`: `amount`, `convertedAmount` fields |
| MULTI-CUR-04 | The system must automatically handle currency conversion when transferring funds between two accounts with different currencies [^27]. | `BalanceFlowService.java`: `confirmBalance()` logic for `TRANSFER` type |
| MULTI-CUR-05 | The system must be capable of fetching the latest exchange rates from an external API to ensure conversion accuracy. It also ships with a static list of currencies as a fallback [^28]. | `CurrencyService.java`: `refreshCurrency()`; `currency.json` |
| MULTI-CUR-06 | All financial reports and summaries (e.g., financial overview, expense reports) must aggregate data by converting all transaction amounts to the book's or group's default currency [^4]. | `AccountService.java`: `overview()`; `ReportService.java` |

###### Example User Flow: Recording an Expense in a Foreign Currency Account

1.  **Context**: User David's main `Book` has a default currency of `USD`. He has an `Account` named "German Bank" with the currency `EUR`.
2.  **Record Transaction**: While on a trip in Berlin, David buys a train ticket for €10. He records this as an expense from his "German Bank" account.
3.  **Enter Details**: He enters `10` as the amount for the new transaction.
4.  **System Processing**:
    *   The `BalanceFlowService` detects that the account's currency (`EUR`) is different from the book's default currency (`USD`).
    *   It calls `CurrencyService.convert("EUR", "USD")` to get the current exchange rate (e.g., 1.08).
    *   The service calculates the `convertedAmount` as `10 * 1.08 = 10.80`.
    *   It saves the `BalanceFlow` with `amount` = 10 and `convertedAmount` = 10.80 [^26].
    *   The balance of the "German Bank" account is reduced by €10.
5.  **View Report**: Later, when David views his monthly expense report, this transaction is included as `$10.80` in the "Transportation" category, seamlessly integrated with his other USD-based expenses.

[^1]: AccountService.java: `overview()` - Calculates and returns an array containing total assets, total debts, and net worth.
[^2]: AccountService.java: `getAssets()`, `getDebts()` - These methods retrieve accounts based on their `AccountType` (CHECKING/ASSET for assets, CREDIT/DEBT for debts).
[^3]: Account.java: `include` - A boolean field on the `Account` entity that determines if it is included in summary calculations.
[^4]: AccountService.java: `overview()` - This method iterates through accounts and uses `currencyService.convert()` to normalize all balances to the group's default currency before summing them up.
[^5]: AccountService.java: `statistics()` - Calculates total balance, total credit limit, and remaining credit across a given set of accounts, converting currencies as needed.
[^6]: BalanceFlow.java: `type` - An enum field of type `FlowType` that classifies the transaction.
[^7]: BalanceFlow.java: This entity serves as the core model for all financial transactions, containing fields for amount, time, book, and more.
[^8]: BalanceFlowService.java: `confirmBalance()` - This private method contains the logic to update account balances based on the transaction type and amount.
[^9]: BalanceFlow.java: `categories`, `tags`, `payee` - Fields that establish relationships with `Category`, `Tag`, and `Payee` entities to provide detailed transaction context.
[^10]: CategoryRelationForm.java: Used within `BalanceFlowAddForm` as a list, allowing a single transaction to be associated with multiple categories, each with its own amount.
[^11]: BalanceFlowQueryForm.java: `buildPredicate()` - Constructs a dynamic QueryDSL predicate based on various filter criteria to search for transactions.
[^12]: BalanceFlow.java: `confirm` - A boolean field indicating whether the transaction is finalized and should impact account balances.
[^13]: BalanceFlowService.java: `addFile()` - Handles the logic for processing a `MultipartFile`, creating a `FlowFile` entity, and associating it with a `BalanceFlow`.
[^14]: FileValidator.java: `isSupportedContentType()` - A validator that checks the `contentType` of an uploaded file against a list of allowed MIME types.
[^15]: FlowFile.java: `data` - A `byte[]` field annotated with `@Lob` and `columnDefinition = "LONGBLOB"` to store the file's binary content in the database.
[^16]: FlowFile.java: Contains fields like `originalName`, `contentType`, and `size` to store file metadata.
[^17]: BalanceFlowController.java: `handleFiles()` - An endpoint that retrieves all `FlowFile` records associated with a given `BalanceFlow` ID.
[^18]: FlowFileController.java: `handleView()` - An endpoint that serves the file content. It requires the file ID and `createTime` in the request, adding a layer of security to prevent simple enumeration of file IDs.
[^19]: BookController.java: Provides REST endpoints for CRUD operations on `Book` entities.
[^20]: Category.java, Tag.java, Payee.java: Each of these entities contains a mandatory `ManyToOne` relationship to the `Book` entity.
[^21]: CurrentSession.java: A session-scoped bean that holds the current user's active `Book` object.
[^22]: UserController.java: `handleSetDefaultBook()` - An endpoint that allows the user to change their active book, which is then persisted on the `User` entity and updated in the session.
[^23]: BookService.java: `addByTemplate()`, `addByBook()` - Methods that create a new book and populate its categories, tags, and payees based on a JSON template or an existing book.
[^24]: Account.java: `currencyCode` - A string field on the `Account` entity to store the currency code (e.g., 'USD').
[^25]: Book.java: `defaultCurrencyCode` - A string field on the `Book` entity that sets the reporting currency for that ledger.
[^26]: BalanceFlow.java: `amount` and `convertedAmount` - Two `BigDecimal` fields to store the transaction value in its original currency and in the book's default currency.
[^27]: BalanceFlowService.java: `confirmBalance()` - When a `TRANSFER` `FlowType` is processed, this method handles debiting the 'from' account by `amount` and crediting the 'to' account by `convertedAmount`.
[^28]: CurrencyService.java: `refreshCurrency()` - Method that makes an HTTP GET request to an external exchange rate API (`https://api.exchangerate-api.com/v4/latest/USD`) and updates the in-memory currency rates.

### Modernization Challenges
#### User Journeys

This section outlines the primary user journeys that the MoneyNote application supports. By analyzing the application's code, we can reverse-engineer the intended functionality and distill it into a set of business requirements and user flows. This serves as a foundational requirements document, detailing what the system currently does from a user's perspective.

##### 1\. Monitor Financial Situation

This journey describes how a user gains a high-level understanding of their overall financial health by viewing aggregated assets, debts, and net worth.

###### Core Interactions

The user interacts with dashboard or reporting sections of the application to see a consolidated view of their finances. The system aggregates data from various accounts, performs necessary currency conversions, and presents the information in a summarized and graphical format. This provides an at-a-glance overview without needing to inspect individual accounts.

###### Business requirements

The system implements the following business rules to provide a financial overview:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-FIN-01 | The system must calculate the total value of all assets. Assets are defined as accounts of type `CHECKING` and `ASSET` that are marked as `enabled` and `included` in statistics. [^1] | `AccountService.java: getAssets()` |
| REQ-FIN-02 | The system must calculate the total value of all debts. Debts are defined as accounts of type `CREDIT` and `DEBT` that are marked as `enabled` and `included` in statistics. [^2] | `AccountService.java: getDebts()` |
| REQ-FIN-03 | The system must calculate the user's net worth by subtracting total debts from total assets. [^3] | `AccountService.java: overview()` |
| REQ-FIN-04 | All financial totals (assets, debts, net worth) must be presented in the user's active group's default currency. The system must perform currency conversions for accounts with different currencies. [^4] | `AccountService.java: overview()` |
| REQ-FIN-05 | The system must provide data for generating charts that break down total assets and total debts by individual accounts, showing the contribution of each account to the total. [^5] | `ReportService.java: reportBalance()` |
| REQ-FIN-06 | When calculating report totals, the system must use the appropriate currency conversion rate to ensure all values are comparable in the group's default currency. [^6] | `ReportService.java: reportBalance()` |

###### Example user flow

**User Goal:** To quickly check their current net worth.

1.  **Login:** The user logs into the MoneyNote application.
2.  **Navigate to Dashboard:** The user accesses the main dashboard or "Overview" page.
3.  **API Call:** The frontend makes a request to the `/accounts/overview` endpoint.
4.  **System Processing:**
    *   The `AccountService` fetches all `ASSET` and `CHECKING` accounts.
    *   It then fetches all `CREDIT` and `DEBT` accounts.
    *   It iterates through each list, converting each account's balance to the group's default currency.
    *   It sums the converted values to get a total asset value and a total debt value.
    *   It calculates the net worth.
5.  **Display Information:** The UI displays three prominent figures: "Total Assets," "Total Debts," and "Net Worth."

##### 2\. Track Incomes & Expenses

This journey covers the fundamental task of recording financial transactions, including expenditures and earnings, and classifying them for reporting and analysis.

###### Core Interactions

The user creates a new transaction by filling out a form. They specify the transaction type (income or expense), associate it with an account and a book, assign it to one or more categories, and enter the amount. They can also add optional details like tags, a payee, and notes. Once saved, the transaction is logged, and the corresponding account balance is updated.

###### Business requirements

The system implements the following business rules for tracking transactions:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :- |
| REQ-TRK-01 | Users must be able to create financial transactions of type `EXPENSE` and `INCOME`. [^7] | `FlowType.java` |
| REQ-TRK-02 | Every transaction must belong to a specific `Book` and be associated with a `Group`. [^8] | `BalanceFlow.java` |
| REQ-TRK-03 | A transaction must be linked to a source/destination `Account`. [^9] | `BalanceFlowAddForm.java` |
| REQ-TRK-04 | Transactions must be classifiable using at least one `Category`. The system supports splitting a single transaction across multiple categories, each with its own amount. [^10] | `BalanceFlowAddForm.java`, `CategoryRelation.java` |
| REQ-TRK-05 | The total amount of an expense or income transaction is calculated as the sum of all its category amounts. [^11] | `BalanceFlowService.java: add()` |
| REQ-TRK-06 | Users can optionally add multiple `Tags` to a transaction for further classification. [^12] | `BalanceFlowAddForm.java` |
| REQ-TRK-07 | Users can optionally associate a `Payee` with an income or expense transaction. [^13] | `BalanceFlowAddForm.java` |
| RE-TRK-08 | When a transaction is marked as 'confirmed', the system must automatically update the balance of the associated account. The balance is decreased for an expense and increased for an income. [^14] | `BalanceFlowService.java: confirmBalance()` |
| REQ-TRK-09 | The system must provide full CRUD (Create, Read, Update, Delete) operations for all transactions. [^15] | `BalanceFlowController.java` |

###### Example user flow

**User Goal:** To record a grocery shopping expense.

1.  **Initiate Transaction:** The user clicks the "Add Transaction" button from their current book view.
2.  **Fill Form:**
    *   Selects **Type**: `EXPENSE`.
    *   Selects **Account**: "My Checking Account".
    *   Selects **Category**: "Food" and enters an **Amount**: 50.75.
    *   (Optional) Adds a second category split: "Household" and **Amount**: 12.50.
    *   (Optional) Adds **Tag**: "Weekly Shopping".
    *   (Optional) Selects **Payee**: "Local Supermarket".
    *   (Optional) Adds **Notes**: "Weekly groceries and cleaning supplies".
    *   Sets the **Date**.
3.  **Confirm and Save:** The user saves the transaction.
4.  **API Call:** The frontend sends a `POST` request to `/balance-flows` with the form data.
5.  **System Processing:**
    *   `BalanceFlowService` validates the input.
    *   It calculates the total amount: 50.75 + 12.50 = 63.25.
    *   It creates a new `BalanceFlow` entity and associated `CategoryRelation` entities.
    *   The `confirmBalance` method is called, which subtracts 63.25 from the balance of "My Checking Account".
6.  **Confirmation:** The transaction appears in the user's transaction list.

##### 3\. Attach Financial Record Files

This journey allows users to attach digital files, such as receipts or invoices, to their transaction records for archival and proof-of-purchase.

###### Core Interactions

Within the context of a specific transaction, the user selects an option to upload a file. They choose a file from their local device, and the application uploads and links it to the transaction. The user can later view a list of attachments for that transaction and download or view them.

###### Business requirements

The system implements the following business rules for file attachments:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-FILE-01 | The system must allow users to attach files to an existing `BalanceFlow` (transaction) record. [^16] | `FlowFileController.java: handleAddFile()` |
| REQ-FILE-02 | The system must validate uploaded files and only accept specific content types: `application/pdf`, `image/png`, `image/jpg`, and `image/jpeg`. [^17] | `FileValidator.java` |
| REQ-FILE-03 | For each uploaded file, the system must store its binary data, original filename, content type, and size. [^18] | `FlowFile.java` |
| REQ-FILE-04 | Each file record (`FlowFile`) must be associated with the user who uploaded it and the specific transaction (`BalanceFlow`) it belongs to. [^19] | `FlowFile.java` |
| REQ-FILE-05 | The system must provide a secure endpoint for viewing and downloading attached files. Access is granted based on the file ID and its creation timestamp to prevent simple enumeration. [^20] | `FlowFileController.java: handleView()` |
| REQ-FILE-06 | Users must be able to delete previously attached files from a transaction. [^21] | `FlowFileService.java: remove()` |

###### Example user flow

**User Goal:** To attach a PDF invoice to a business expense.

1.  **Navigate to Transaction:** The user finds and opens the details of a transaction, for example, "Software License Renewal".
2.  **Upload File:** The user clicks an "Attach File" or "Upload Receipt" button.
3.  **Select File:** A file browser opens, and the user selects `invoice-2023.pdf` from their computer.
4.  **API Call:** The frontend sends a multipart `POST` request to `/balance-flows/{id}/addFile` with the selected file.
5.  **System Processing:**
    *   The `FileValidator` checks if the content type is `application/pdf`.
    *   `FlowFileService` reads the file's bytes and metadata.
    *   It creates a new `FlowFile` entity, links it to the "Software License Renewal" transaction, and saves it to the database.
6.  **Confirmation:** The transaction detail view is updated to show a link to `invoice-2023.pdf` in its list of attachments.

##### 4\. Support Multiple Books

This journey enables users to maintain separate, self-contained ledgers (called "Books") to segregate different areas of their financial life, such as personal, family, or business finances.

###### Core Interactions

A user can create new Books, either from scratch, by copying an existing Book, or from a predefined template. Each Book acts as an independent container with its own default currency and its own set of categories, tags, and payees. The user can switch their active context to a different Book to record and view transactions relevant only to that ledger.

###### Business requirements

The system implements the following business rules for managing Books:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-BOOK-01 | Users must be able to create and manage multiple `Books` to organize transactions. [^22] | `BookController.java: handleAdd()` |
| REQ-BOOK-02 | Each `Book` is an isolated container for its own `Categories`, `Tags`, and `Payees`. [^23] | `Book.java` |
| REQ-BOOK-03 | Each `Book` must have a `defaultCurrencyCode` which serves as the base currency for its transactions and reports. [^24] | `Book.java` |
| REQ-BOOK-04 | The system must provide a mechanism for users to create a new `Book` based on a predefined `BookTemplate`, which pre-populates categories and tags. [^25] | `BookService.java: addByTemplate()` |
| REQ-BOOK-05 | The system must allow a user to create a new `Book` by copying the structure (categories, tags, payees) of an existing `Book`. [^26] | `BookService.java: addByBook()` |
| REQ-BOOK-06 | A user must be able to set a specific `Book` as their default/active book for the current session. All subsequent actions will be performed within the context of this book. [^27] | `UserService.java: setDefaultBook()` |
| REQ-BOOK-07 | A `Book` cannot be deleted if it contains any transaction records (`BalanceFlow`). [^28] | `BookService.java: remove()` |

###### Example user flow

**User Goal:** To create a new book to track expenses for a vacation.

1.  **Navigate to Book Management:** The user goes to the "Settings" or "Manage Books" area of the application.
2.  **Create New Book:** The user clicks "Add New Book."
3.  **Choose Creation Method:** The user is presented with options and chooses "Create from Template."
4.  **Select Template:** The user selects a "Travel/Vacation" template from a list.
5.  **Configure Book:**
    *   Enters **Name**: "Europe Trip 2024".
    *   Sets **Default Currency**: "EUR".
6.  **API Call:** The frontend sends a `POST` request to `/books/template`.
7.  **System Processing:**
    *   `BookService` creates a new `Book` entity named "Europe Trip 2024".
    *   It loads the "Travel/Vacation" `BookTemplate` and programmatically creates all associated categories (e.g., "Flights," "Hotels," "Tours") and tags for the new book.
8.  **Confirmation:** The "Europe Trip 2024" book is created. The user can now switch to this book to log trip-related expenses.

##### 5\. Support Multiple Currencies

This journey describes the system's capability to handle accounts and transactions in different currencies, perform conversions, and provide consolidated reporting.

###### Core Interactions

Users can create accounts in various currencies (e.g., USD, EUR, CNY). When recording transactions between accounts with different currencies, the system prompts for or calculates the converted amount. In reports and dashboards, all financial data is converted to a single, user-defined base currency for consistent analysis.

###### Business requirements

The system implements the following business rules for multi-currency support:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-CUR-01 | The system must maintain a list of supported world currencies and their exchange rates relative to a base currency (USD). [^29] | `currency.json`, `CurrencyService.java` |
| REQ-CUR-02 | The system must be able to refresh its exchange rate data by querying an external API. [^30] | `CurrencyService.java: refreshCurrency()` |
| REQ-CUR-03 | Each `Account` entity must be assigned a specific `currencyCode`. [^31] | `Account.java` |
| REQ-CUR-04 | For expense or income transactions involving an account whose currency differs from the Book's default currency, the system must store both the original `amount` and the `convertedAmount`. [^32] | `BalanceFlow.java`, `BalanceFlowService.java: add()` |
| REQ-CUR-05 | For transfer transactions between two accounts with different currencies, the system must store the `amount` sent from the source account and the `convertedAmount` received in the destination account. [^33] | `BalanceFlowService.java: add()` |
| REQ-CUR-06 | All high-level financial reports and overview statistics must convert amounts from all currencies into the group's single default currency for accurate aggregation. [^34] | `AccountService.java: statistics()`, `ReportService.java: reportBalance()` |

###### Example user flow

**User Goal:** To record a salary payment of €3,000 into a EUR-denominated account, while the main book currency is USD.

1.  **User Setup:**
    *   User has a `Book` with default currency USD.
    *   User has an `Account` named "German Bank Account" with currency EUR.
2.  **Initiate Transaction:** The user starts to add a new `INCOME` transaction.
3.  **Fill Form:**
    *   **Account**: Selects "German Bank Account (EUR)".
    *   **Category**: Selects "Salary" and enters **Amount**: 3000.
4.  **Handle Conversion:**
    *   The system detects that the account currency (EUR) is different from the book's default currency (USD).
    *   The UI calls the `/currencies/rate?from=EUR&to=USD` endpoint to get the exchange rate (e.g., 1.08).
    *   The UI displays the calculated converted amount: 3000 \* 1.08 = $3,240. It allows the user to override this value if needed.
5.  **Save Transaction:** The user confirms and saves.
6.  **API Call:** The frontend sends a `POST` request to `/balance-flows`, including the `amount` (3000) and `convertedAmount` (3240).
7.  **System Processing:**
    *   A `BalanceFlow` entity is created.
    *   `confirmBalance` is called, and the balance of the "German Bank Account" is increased by €3,000.
    *   When the user later views a report in their USD-default book, this transaction contributes $3,240 to their total income.

[^1]: AccountService.java: getAssets() - This method retrieves all accounts of type `CHECKING` and `ASSET` that are enabled and included in statistical calculations, defining what constitutes an asset.
[^2]: AccountService.java: getDebts() - This method retrieves all accounts of type `CREDIT` and `DEBT` that are enabled and included, defining what constitutes a debt.
[^3]: AccountService.java: overview() - This method orchestrates the calculation of total assets, total debts, and subtracts debts from assets to determine the net worth.
[^4]: AccountService.java: overview() - Within this method, it iterates through asset and debt accounts, calling `currencyService.convert` to standardize all balances to the group's default currency before summation.
[^5]: ReportService.java: reportBalance() - This method generates the data structure for balance charts by creating `ChartVO` objects for each asset and debt account, including their converted balance and percentage of the total.
[^6]: ReportService.java: reportBalance() - This method explicitly calls `currencyService.convert` for each account to ensure all values are in the group's default currency before being added to the report.
[^7]: FlowType.java: EXPENSE, INCOME - This enum defines the possible types for a financial flow, including `EXPENSE` and `INCOME`, which forms the basis of transaction tracking.
[^8]: BalanceFlow.java: book, group - The `BalanceFlow` entity contains mandatory (`@NotNull`) fields for `Book` and `Group`, enforcing that every transaction belongs to both.
[^9]: BalanceFlowAddForm.java: account - The form for adding a new transaction includes an `account` field, linking the flow to a specific financial account.
[^10]: BalanceFlowAddForm.java: categories - The form accepts a list of `CategoryRelationForm` objects, allowing a single transaction to be split across multiple categories.
[^11]: BalanceFlowService.java: add() - This method calculates the total transaction amount by summing the `amount` field from each `CategoryRelationForm` in the input list.
[^12]: BalanceFlowAddForm.java: tags - The form for a new transaction accepts a `Set<Integer>` of tag IDs, enabling multi-tag classification.
[^13]: BalanceFlowAddForm.java: payee - The transaction creation form includes an optional `payee` field to associate the transaction with a specific person or business.
[^14]: BalanceFlowService.java: confirmBalance() - This method contains the logic to update an account's balance. It subtracts for expenses and adds for income.
[^15]: BalanceFlowController.java: handleAdd, handleQuery, handleUpdate, handleDelete - This controller exposes REST endpoints for creating, reading, updating, and deleting `BalanceFlow` entities.
[^16]: FlowFileController.java: handleAddFile() - This endpoint accepts a `MultipartFile` and an `id` to associate an uploaded file with a specific transaction.
[^17]: FileValidator.java: isSupportedContentType() - This validation class checks the content type of an uploaded file against a hardcoded list of allowed types (pdf, png, jpg, jpeg).
[^18]: FlowFile.java: - This entity defines the database schema for storing file attachments, including fields for `data`, `originalName`, `contentType`, and `size`.
[^19]: FlowFile.java: creator, flow - The entity includes `@ManyToOne` relationships to the `User` who uploaded the file and the `BalanceFlow` it's attached to.
[^20]: FlowFileController.java: handleView() - This endpoint requires both the file `id` and its `createTime` as query parameters to authorize access, making it harder to guess valid URLs.
[^21]: FlowFileService.java: remove() - This service method handles the logic for deleting a `FlowFile` entity from the database.
[^22]: BookController.java: handleAdd() - This endpoint allows for the creation of new `Book` entities.
[^23]: Book.java: categories, tags, payees - The `Book` entity has `@OneToMany` relationships to its own sets of `Category`, `Tag`, and `Payee` entities, indicating they are scoped to the book.
[^24]: Book.java: defaultCurrencyCode - The `Book` entity has a `@NotNull` field for `defaultCurrencyCode`, making it a mandatory attribute.
[^25]: BookService.java: addByTemplate() - This method takes a template ID, loads a `BookTemplate` from a JSON file, and uses it to create a new `Book` with pre-filled categories and tags.
[^26]: BookService.java: addByBook() - This method copies the categories, tags, and payees from a source `Book` to a newly created `Book`.
[^27]: UserService.java: setDefaultBook() - This method updates the `defaultBook` field on the current `User` entity, changing their active context.
[^28]: BookService.java: remove() - This method checks if any `BalanceFlow` records exist for a book before allowing its deletion, preventing data loss.
[^29]: currency.json: - This resource file contains a predefined list of world currencies and their default exchange rates against USD.
[^30]: CurrencyService.java: refreshCurrency() - This method makes an HTTP GET request to an external exchange rate API (`api.exchangerate-api.com`) and updates the in-memory currency rates.
[^31]: Account.java: currencyCode - The `Account` entity contains a non-nullable `currencyCode` field, ensuring every account is tied to a specific currency.
[^32]: BalanceFlow.java: amount, convertedAmount - The transaction entity has fields for both the original `amount` and the `convertedAmount`, used when the transaction currency differs from a base currency.
[^33]: BalanceFlowService.java: add() - The logic for `FlowType.TRANSFER` handles cases where the source and destination account currencies differ, storing the sent amount in `amount` and the received amount in `convertedAmount`.
[^34]: AccountService.java: statistics() - This service method explicitly calls `currencyService.convert` to standardize all account balances to the group's default currency before aggregation.

### Modernization Opportunities
#### User Journeys

This section deconstructs the application's functionality into distinct user journeys. Each journey represents a core task a user would perform, outlining the interactions, the underlying business requirements implemented in the code, and a practical user flow example. This analysis serves as a reverse-engineered requirements document based on the provided codebase.

##### 1. Tracking Income and Expenses

This journey describes the fundamental process of recording financial transactions. It is the primary data entry point for the user and the foundation for all financial tracking and reporting.

###### Core Interactions

1.  **Initiate Transaction**: The user starts by selecting the option to add a new transaction from the main interface.
2.  **Select Transaction Type**: The user chooses the type of transaction, which is typically 'Expense' or 'Income' [^1].
3.  **Enter Core Details**: The user inputs the fundamental details of the transaction, such as the date, the account to be used, and the total amount.
4.  **Categorize the Transaction**: The user assigns one or more spending or income categories to the transaction. The system supports splitting the transaction amount across multiple categories [^5].
5.  **Add Optional Details**: The user can enrich the transaction with optional information, including a descriptive title, a payee (merchant or source of funds), descriptive tags, and detailed notes [^3].
6.  **Handle Currency**: If the selected account's currency differs from the book's default currency, the user provides the converted amount to ensure accurate reporting [^9].
7.  **Confirm and Save**: The user saves the transaction. The system can be configured to save the transaction as 'confirmed' or 'unconfirmed'. A confirmed transaction immediately impacts the associated account's balance [^11].

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-TRACK-01 | The system must allow users to record transactions classified as **Expense**, **Income**, **Transfer**, or **Adjust** [^1]. | `FlowType.java`, `BalanceFlowAddForm.java` |
| REQ-TRACK-02 | Every transaction (`BalanceFlow`) must be associated with a specific `Book` and belong to the user's active `Group` [^2]. | `BalanceFlow.java` |
| REQ-TRACK-03 | A transaction must include a creation time (`createTime`) and can have an optional `title` and `notes` [^3]. | `BalanceFlow.java` |
| REQ-TRACK-04 | Expense and Income transactions must be associated with at least one `Category` and cannot be saved without it [^4]. | `BalanceFlowService.java`: `checkBeforeAdd()` |
| REQ-TRACK-05 | The system must support splitting a single transaction across multiple categories, with a specific amount for each category `CategoryRelationForm` [^5]. | `BalanceFlowAddForm.java`, `CategoryRelation.java` |
| REQ-TRACK-06 | The total amount of an Expense or Income transaction is automatically calculated as the sum of amounts from all its associated categories [^6]. | `BalanceFlowService.java`: `add()` |
| REQ-TRACK-07 | A transaction can be optionally linked to a `Payee` from a predefined list within the book [^7]. | `BalanceFlow.java` |
| REQ-TRACK-08 | A transaction can be optionally linked to multiple `Tags` for granular filtering and reporting [^8]. | `BalanceFlow.java`, `TagRelation.java` |
| REQ-TRACK-09 | If an account's currency differs from the book's default currency, the system must capture a `convertedAmount` for the transaction [^9]. | `BalanceFlowService.java`: `add()` logic |
| REQ-TRACK-10 | Transactions can be saved in a `confirm=false` state and confirmed later. This allows for pending or scheduled transactions [^10]. | `BalanceFlowAddForm.java` |
| REQ-TRACK-11 | Upon confirmation (`confirm=true`), the system must update the balance of the associated `Account`. Expenses decrease the balance, while incomes increase it [^11]. | `BalanceFlowService.java`: `confirmBalance()` |
| REQ-TRACK-12 | Users can delete existing transactions. Deleting a confirmed transaction must reverse the corresponding balance adjustment on the account [^12]. | `BalanceFlowService.java`: `remove()`, `refundBalance()` |

###### Example User Flow: Recording a Shared Dinner Expense

1.  **User `Alice` logs into the MoneyNote app.** Her default book, "Personal Finances," is active.
2.  She taps the "Add Transaction" button.
3.  She selects **"Expense"** as the transaction type.
4.  She chooses her "Credit Card" account, which is in USD. Her book's default currency is also USD.
5.  She enters the date and sets "Dinner with friends" as the `title`.
6.  The total bill was $50. She paid for everyone. She needs to categorize it.
    *   She adds the category **"Food -> Restaurants"** with an amount of **$20** (her share).
    *   She adds another category **"Social -> Lending"** with an amount of **$30** (to track money her friends owe her).
7.  She selects "City Diner" from her list of `Payees`.
8.  She adds the `tag` "friends" to the transaction.
9.  She leaves the "Confirm" option checked and saves the transaction.
10. The system creates a new `BalanceFlow` record with a total amount of $50 and two `CategoryRelation` entries. The balance of her "Credit Card" account is immediately decreased by $50.

##### 2. Monitoring Financial Situation

This journey focuses on how users review and analyze their financial data to understand their financial health, track assets and liabilities, and analyze spending patterns.

###### Core Interactions

1.  **View Dashboard Overview**: The user navigates to the main dashboard or overview page.
2.  **Analyze Net Worth**: The user views a high-level summary of their total assets, total debts, and overall net worth, all converted to a single default currency [^13].
3.  **Review Accounts**: The user navigates to the account list to see a detailed breakdown of all their financial accounts (e.g., bank accounts, credit cards, loans).
4.  **Filter and Sort Accounts**: The user can filter the account list by type (e.g., `CHECKING`, `CREDIT`), status, or name to focus on specific information [^14].
5.  **Generate Reports**: The user moves to the reporting section to create analytical charts and tables.
6.  **Customize and Drill Down**: The user customizes a report by selecting a date range and filtering by categories or tags. The system generates a visual chart, and the user can click on segments to drill down into sub-categories or view the underlying transactions [^15].

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-MONITOR-01 | The system must provide a financial overview by calculating and displaying total assets, total debts, and net worth (assets - debts) [^13]. | `AccountService.java`: `overview()` |
| REQ-MONITOR-02 | Total assets must be calculated by summing the balances of all active and included accounts of type `CHECKING` and `ASSET` [^16]. | `AccountService.java`: `getAssets()` |
| REQ-MONITOR-03 | Total debts must be calculated by summing the balances of all active and included accounts of type `CREDIT` and `DEBT` [^17]. | `AccountService.java`: `getDebts()` |
| REQ-MONITOR-04 | All overview and report calculations must convert account balances to the user's group default currency for consistent comparison [^13]. | `AccountService.java`: `overview()`, `CurrencyService.java` |
| REQ-MONITOR-05 | The system must provide a comprehensive list of all user accounts, showing details such as name, type, current balance, currency, and enabled status [^18]. | `AccountController.java`: `handleQuery()` |
| REQ-MONITOR-06 | The account list must be filterable by parameters including `type`, `enable` status, `name`, balance range, and `currencyCode` [^14]. | `AccountQueryForm.java`: `buildPredicate()` |
| REQ-MONITOR-07 | The system must offer reporting tools to analyze financial data aggregated by `Category`, `Tag`, and `Payee` [^19]. | `ReportController.java` |
| REQ-MONITOR-08 | Reports must be filterable by a date range, specific book, account, and other transaction attributes [^20]. | `CategoryReportQueryForm.java` |
| REQ-MONITOR-09 | Report visualizations must show the total amount for each item (e.g., category) and its percentage of the grand total [^15]. | `ReportService.java`: `reportCategory()` |
| REQ-MONITOR-10 | A balance report must be available to visualize the breakdown of assets and debts across individual accounts [^21]. | `ReportService.java`: `reportBalance()` |

###### Example User Flow: Analyzing Monthly Spending

1.  **User `Bob` wants to understand his spending habits for the last month.** He opens the MoneyNote app and navigates to the "Reports" section.
2.  He selects the **"Expense by Category"** report type.
3.  He uses the date picker to set the range from the 1st to the 31st of the previous month.
4.  He ensures his "Daily Life" book is selected.
5.  He clicks **"Generate Report."**
6.  The application displays a pie chart. He quickly sees that "Food & Dining" constitutes 40% of his spending.
7.  He clicks on the "Food & Dining" slice of the chart.
8.  The report view drills down, displaying a new chart for the sub-categories within "Food & Dining." He discovers that "Restaurants" make up 75% of this spending, while "Groceries" are only 25%. This insight helps him decide to cook more at home.

##### 3. Managing Finances in Multiple Currencies

This journey addresses the need for users who deal with more than one currency, such as travelers, expatriates, or those with international investments.

###### Core Interactions

1.  **Create a Foreign Currency Account**: The user creates a new account (e.g., for a European bank) and explicitly sets its currency to "EUR" [^32].
2.  **Record Foreign Transaction**: The user records an expense in the EUR account. Because the account's currency is different from the book's default (e.g., USD), the system prompts for the `convertedAmount` in USD [^9].
3.  **Perform Cross-Currency Transfer**: The user initiates a transfer from their USD account to their EUR account. The form requires them to enter both the source amount (in USD) and the final received amount in the destination currency (EUR), effectively capturing the exchange rate of the transaction [^33].
4.  **View Consolidated Reports**: The user views their net worth summary. The system automatically converts the balance of the EUR account to USD using the latest exchange rates, presenting a unified financial picture [^13].

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-CUR-01 | The system must support a predefined list of world currencies, loaded from a configuration file (`currency.json`) [^34]. | `CurrencyDataLoader.java` |
| REQ-CUR-02 | The application must attempt to refresh currency exchange rates periodically from an external API service (`exchangerate-api.com`) [^35]. | `CurrencyService.java`: `refreshCurrency()` |
| REQ-CUR-03 | Each `Account` entity must have a `currencyCode` attribute to define its currency [^32]. | `Account.java` |
| REQ-CUR-04 | Each `Book` must have a `defaultCurrencyCode` which serves as the base for reporting and consolidation [^23]. | `Book.java` |
| REQ-CUR-05 | When recording an Expense or Income in an account with a currency different from the book's default, the system must store both the original `amount` and the `convertedAmount` [^9]. | `BalanceFlowService.java`: `add()` |
| REQ-CUR-06 | For `TRANSFER` transactions between accounts of different currencies, the system must store the `amount` in the source currency and the `convertedAmount` in the destination currency [^33]. | `BalanceFlowService.java`: `add()` and `confirmBalance()` |
| REQ-CUR-07 | All aggregated financial reports and summaries (e.g., Net Worth Overview) must present data in the group's default currency by converting all amounts as needed [^13]. | `AccountService.java`: `overview()`, `statistics()` |
| REQ-CUR-08 | The system must provide a utility endpoint to calculate the converted value between any two currencies for a given amount [^36]. | `CurrencyController.java`: `handleCalc()` |

###### Example User Flow: Transferring Funds for an International Trip

1.  **User `Diana` is preparing for a trip to Europe.** She has a "US Checking" account in USD and has already created a "Travel Card" account in EUR.
2.  She needs to load her travel card. She navigates to the "Transfer" screen.
3.  In the 'From' field, she selects "US Checking (USD)".
4.  In the 'To' field, she selects "Travel Card (EUR)".
5.  She enters `500` in the amount field for the source account.
6.  The UI, recognizing the currency difference, displays a `convertedAmount` field. She checks her bank statement and sees that $500 resulted in €475 being credited. She enters `475` into the `convertedAmount` field.
7.  She confirms the transfer.
8.  The system correctly deducts $500 from her "US Checking" account and adds €475 to her "Travel Card" account. When she views her financial overview, the €475 balance is converted back to its USD equivalent for the net worth calculation.

##### 4. Managing Multiple "Books"

This journey outlines how users can segregate different areas of their financial life (e.g., personal, family, small business) into separate containers known as "Books."

###### Core Interactions

1.  **Navigate to Book Management**: The user goes to the "Manage Books" section of the application.
2.  **Create a New Book**: The user clicks "Add Book" and chooses to either create a blank book, copy an existing book, or use a predefined template (e.g., "Daily Life," "Small Business") [^22].
3.  **Configure the New Book**: The user provides a name and sets a default currency for the new book [^23]. If created from a template, it comes pre-populated with relevant categories and tags.
4.  **Switch Active Book**: From a dropdown or menu, the user selects a different book to make it active. The entire application context (transactions, reports, accounts shown) switches to that of the selected book [^24].
5.  **Export Book Data**: The user selects a book and chooses the "Export" option. The system generates and downloads an Excel file containing all transactions for that book [^26].

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-BOOK-01 | The system must support multiple `Books` within a user's `Group`, allowing financial segregation [^27]. | `Book.java` |
| REQ-BOOK-02 | Each `Book` must have a unique `name` within its group and a `defaultCurrencyCode` [^23]. | `BookAddForm.java` |
| REQ-BOOK-03 | Users must be able to create new books from predefined `BookTemplate`s, which auto-populate `Category`, `Tag`, and `Payee` data [^28]. | `BookService.java`: `addByTemplate()` |
| REQ-BOOK-04 | Users must be able to duplicate an existing book, which copies its entire structure (categories, tags, payees) to a new book [^29]. | `BookService.java`: `addByBook()` |
| REQ-BOOK-05 | Each user must have a `defaultBook` assigned, which is automatically loaded upon login [^30]. | `User.java` |
| REQ-BOOK-06 | Users must have the ability to switch their active book during a session, changing the context for all financial operations [^24]. | `UserController.java`: `handleSetDefaultBook()` |
| REQ-BOOK-07 | Core data entities (`BalanceFlow`, `Category`, `Tag`, `Payee`) must be strictly scoped to a single `Book` [^31]. | `Category.java`, `Tag.java`, `Payee.java` |
| REQ-BOOK-08 | A `Book` can be configured with default accounts and categories for different transaction types to speed up data entry [^25]. | `BookUpdateForm.java`, `Book.java` |
| REQ-BOOK-09 | The system must provide a feature to export all transactions of a book into an `.xlsx` spreadsheet [^26]. | `BookService.java`: `exportFlow()` |

###### Example User Flow: Creating and Using a Business Book

1.  **User `Charlie`, a freelance designer, decides to track his business finances separately.** He navigates to "Manage Books."
2.  He clicks "Add Book" and chooses the "Create from Template" option. He selects the "Restaurant Business" template.
3.  He names the new book "Design Business" and sets "USD" as the default currency.
4.  The book is created and pre-filled with business-centric categories like "Client Revenue," "Software Licenses," and "Contractor Payments."
5.  He makes "Design Business" his active book.
6.  He navigates to the "Add Transaction" screen and logs a $5,000 payment from a client as "Income" in his "Client Revenue" category. This transaction is now stored exclusively within the "Design Business" book and does not mix with his personal finances.

##### 5. Attaching Files to Financial Records

This journey enables users to associate digital documents like receipts, invoices, or warranties with their transactions for record-keeping and proof-of-purchase.

###### Core Interactions

1.  **Locate Transaction**: The user finds and opens the details of an existing transaction.
2.  **Upload File**: The user clicks an "Attach File" button, which opens a file picker.
3.  **Select and Upload**: The user selects a file (e.g., a PDF invoice or a photo of a receipt) from their device. The file is then uploaded to the server.
4.  **View Attachments**: The uploaded file's name appears in an "Attachments" list on the transaction detail page.
5.  **Retrieve File**: At any time, the user can return to this transaction, click on the file's name, and the system will serve the file for viewing or download [^39].
6.  **Delete Attachment**: The user can remove an attachment from a transaction.

###### Business Requirements

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-FILE-01 | The system must allow users to upload files and associate them with a specific `BalanceFlow` (transaction) record [^38]. | `BalanceFlowController.java`: `handleAddFile()` |
| REQ-FILE-02 | File data must be stored directly in the database as a `LONGBLOB` data type [^40]. | `FlowFile.java` |
| REQ-FILE-03 | The system must store file metadata, including `originalName`, `contentType`, `size`, and `createTime` [^41]. | `FlowFile.java` |
| REQ-FILE-04 | File uploads must be validated to restrict them to supported content types, specifically `pdf`, `png`, `jpg`, and `jpeg` [^37]. | `FileValidator.java` |
| REQ-FILE-05 | The maximum size for a single file upload and for the total request size is configurable in the application properties (defaults to 100MB) [^42]. | `application.properties` |
| REQ-FILE-06 | Users must be able to retrieve a list of all files attached to a given transaction [^39]. | `BalanceFlowController.java`: `handleFiles()` |
| REQ-FILE-07 | The system must provide a secure endpoint for viewing/downloading files that validates access rights [^43]. | `FlowFileController.java`: `handleView()` |
| REQ-FILE-08 | When a `BalanceFlow` record is deleted, all its associated `FlowFile` records must also be deleted from the database to prevent orphaned data [^44]. | `BalanceFlowService.java`: `remove()` |

###### Example User Flow: Attaching a Warranty Receipt

1.  **User `Ethan` buys a new monitor and records it as an expense.**
2.  He receives the receipt as a PDF in his email. He wants to save it with the transaction for warranty purposes.
3.  He opens the monitor expense transaction in the MoneyNote app.
4.  He taps the "Attach File" button.
5.  He selects the `monitor-receipt.pdf` file from his device.
6.  The file uploads, and he sees it listed under the transaction's attachments.
7.  A year later, the monitor malfunctions. He easily finds the transaction in MoneyNote, clicks the attachment, and downloads the PDF receipt to initiate a warranty claim.

[^1]: `src/main/java/cn/biq/mn/balanceflow/FlowType.java`: Defines the enum for transaction types including EXPENSE and INCOME.
[^2]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlow.java`: The `BalanceFlow` entity has required relationships with `Book` and `Group`.
[^3]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowAddForm.java`: This form includes fields for `createTime`, `title`, and `notes`.
[^4]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java`: The `checkBeforeAdd` method validates that categories are not empty for expense and income types.
[^5]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowAddForm.java`: The form accepts a `List<CategoryRelationForm>`, allowing multiple categories per transaction.
[^6]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java`: In the `add` method, the total `amount` is calculated by summing the amounts from the `categories` list.
[^7]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlow.java`: The entity includes an optional relationship to the `Payee` entity.
[^8]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlow.java`: The entity includes a `Set<TagRelation>` to link multiple tags.
[^9]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java`: The `add` method logic checks if account currency differs from book currency and uses `convertedAmount`.
[^10]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowAddForm.java`: The `confirm` boolean field controls the confirmation status of a new transaction.
[^11]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java`: The `confirmBalance` method updates the account balance based on the flow type.
[^12]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java`: The `remove` method calls `refundBalance` to reverse the financial impact on the account.
[^13]: `src/main/java/cn/biq/mn/account/AccountService.java`: The `overview()` method calculates total assets, debts, and net worth, converting all currencies to the group's default.
[^14]: `src/main/java/cn/biq/mn/account/AccountQueryForm.java`: This form class defines various predicates to filter the account list.
[^15]: `src/main/java/cn/biq/mn/report/ReportService.java`: Methods like `reportCategory` calculate totals and percentages for chart generation.
[^16]: `src/main/java/cn/biq/mn/account/AccountService.java`: The `getAssets` method retrieves all accounts of type `CHECKING` and `ASSET`.
[^17]: `src/main/java/cn/biq/mn/account/AccountService.java`: The `getDebts` method retrieves all accounts of type `CREDIT` and `DEBT`.
[^18]: `src/main/java/cn/biq/mn/account/AccountController.java`: The `handleQuery` endpoint returns a paginated list of `AccountDetails`.
[^19]: `src/main/java/cn/biq/mn/report/ReportController.java`: Exposes endpoints for reports on categories (`expense-category`), tags (`expense-tag`), and payees (`expense-payee`).
[^20]: `src/main/java/cn/biq/mn/report/CategoryReportQueryForm.java`: Defines filters for reports, including date range (`minTime`, `maxTime`), book, and account.
[^21]: `src/main/java/cn/biq/mn/report/ReportService.java`: The `reportBalance` method generates data for asset and debt breakdown by account.
[^22]: `src/main/java/cn/biq/mn/book/BookController.java`: Contains endpoints for adding a book from a template (`/template`) or by copying (`/copy`).
[^23]: `src/main/java/cn/biq/mn/book/BookAddForm.java`: The form for creating a new book requires a `name` and `defaultCurrencyCode`.
[^24]: `src/main/java/cn/biq/mn/user/UserController.java`: The `handleSetDefaultBook` endpoint allows a user to change their active book.
[^25]: `src/main/java/cn/biq/mn/book/BookUpdateForm.java`: Allows updating a book's name and its default accounts/categories.
[^26]: `src/main/java/cn/biq/mn/book/BookService.java`: The `exportFlow` method generates an Excel workbook (`.xlsx`) with all transactions from a book.
[^27]: `src/main/java/cn/biq/mn/book/Book.java`: The `Book` entity has a mandatory `ManyToOne` relationship with the `Group` entity.
[^28]: `src/main/java/cn/biq/mn/book/BookService.java`: The `addByTemplate` method uses a `BookTemplate` to create a new book with predefined categories, tags, and payees.
[^29]: `src/main/java/cn/biq/mn/book/BookService.java`: The `addByBook` method copies categories, tags, and payees from a source book to a new one.
[^30]: `src/main/java/cn/biq/mn/user/User.java`: The `User` entity has a `defaultBook` field.
[^31]: `src/main/java/cn/biq/mn/category/Category.java`: `Category`, `Tag`, and `Payee` entities all have a required `ManyToOne` relationship with the `Book` entity.
[^32]: `src/main/java/cn/biq/mn/account/Account.java`: The `Account` entity contains a `currencyCode` field.
[^33]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java`: The `add` method enforces providing a `convertedAmount` for transfers between accounts with different currencies.
[^34]: `src/main/java/cn/biq/mn/currency/CurrencyDataLoader.java`: Loads a list of currencies from `currency.json` into the application scope at startup.
[^35]: `src/main/java/cn/biq/mn/currency/CurrencyService.java`: The `refreshCurrency` method calls an external API to update exchange rates.
[^36]: `src/main/java/cn/biq/mn/currency/CurrencyController.java`: The `/calc` endpoint takes from/to currencies and an amount to perform a conversion.
[^37]: `src/main/java/cn/biq/mn/validation/FileValidator.java`: Implements logic to validate the content type of an uploaded file, restricting it to specific image and PDF types.
[^38]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowController.java`: The `handleAddFile` endpoint handles the file upload and associates it with a `BalanceFlow` ID.
[^39]: `src/main/java/cn/biq/mn/flowfile/FlowFileController.java`: The `handleView` endpoint serves the file data for viewing or download.
[^40]: `src/main/java/cn/biq/mn/flowfile/FlowFile.java`: The `data` field is annotated with `@Lob` and `columnDefinition = "LONGBLOB"`.
[^41]: `src/main/java/cn/biq/mn/flowfile/FlowFile.java`: The entity stores `originalName`, `contentType`, `size`, and other metadata.
[^42]: `src/main/resources/application.properties`: Contains `spring.servlet.multipart.max-file-size` and `max-request-size` properties set to 100MB.
[^43]: `src/main/java/cn/biq/mn/flowfile/FlowFileService.java`: The `getFile` method validates the request using both the file ID and `createTime` to add a layer of security.
[^44]: `src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java`: The `remove` method explicitly calls `flowFileRepository.deleteByFlow(entity)` before deleting the transaction itself.

## Cloud Migration
### Migration Overview
This document outlines potential strategies for migrating the MoneyNote application to Google Cloud. It considers two primary scenarios: a low-effort "lift-and-shift" approach and a higher-effort modernization path that refactors the application to fully leverage cloud-native services.

#### Migration Scenarios and Compute Targets

The choice of compute target on Google Cloud depends on the desired level of effort and the long-term goals for the application. The application is a stateful Spring Boot monolith, currently deployed via Docker [^1], which influences the suitability of each target.

| Migration Target | Low-Effort Scenario (As-Is) | High-Effort Scenario (Modernization) |
| :--- | :--- | :--- |
| **Compute Engine** | Ideal for a "lift-and-shift" migration. The existing Docker container can be deployed directly onto a VM with minimal changes. | Less ideal, but possible. The modernized application (e.g., microservices) could be deployed on a fleet of VMs, but this forgoes the benefits of managed orchestration. |
| **Google Kubernetes Engine** | Viable with moderate effort. Requires creating Kubernetes manifests to deploy the container. Offers better orchestration and scalability than VMs. | **Highly Recommended**. GKE is an excellent target for a modernized, microservices-based architecture, providing robust orchestration, auto-scaling, and resilience. |
| **Cloud Run** | High effort. The application's reliance on session state [^2] conflicts with Cloud Run's stateless model and would require significant refactoring to work correctly. | **Highly Recommended**. After refactoring the application into stateless microservices, Cloud Run offers a fully managed, serverless platform with scale-to-zero capabilities for cost efficiency. |

A detailed analysis of migrating to each of these services is available in the "Shift to Compute Engine," "Modernize to Kubernetes Engine," and "Modernize to Cloud Run" sections of this report.

#### External Dependencies and Google Cloud Services

The application relies on several external components that can be migrated to managed Google Cloud services to reduce operational overhead and improve reliability.

##### Database

The application uses an on-premises or self-hosted MySQL database [^3][^4].

*   **Migration Path**: The recommended target is **Cloud SQL for MySQL**. This is a fully managed database service that handles backups, replication, and scaling automatically. Migration would involve:
    1.  Provisioning a Cloud SQL for MySQL instance.
    2.  Migrating the schema (the `1.sql` script can be used as a baseline [^5]) and data using the Database Migration Service.
    3.  Updating the application's datasource configuration in `application.properties` to connect to the Cloud SQL instance.

##### Container Registry

The CI/CD pipelines currently push Docker images to Aliyun Container Registry and Docker Hub [^6].

*   **Migration Path**: These can be consolidated into **Artifact Registry**. Artifact Registry is a fully managed service for storing container images and other build artifacts. It offers vulnerability scanning and provides seamless, secure integration with Google Cloud's compute services like GKE and Cloud Run. The CI/CD workflows would be updated to authenticate with and push images to an Artifact Registry repository.

#### Leveraging Google Cloud Horizontals

Migrating to Google Cloud unlocks access to a suite of powerful services that can enhance the application's performance, security, and maintainability.

##### CI/CD

The project currently uses GitHub Actions for its CI/CD pipeline [^7]. This can be retained and integrated with Google Cloud. A more cloud-native approach would be to adopt **Cloud Build**.

*   **Integration**: Create triggers in Cloud Build that listen for commits to the GitHub repository.
*   **Pipeline**: Define a `cloudbuild.yaml` file to automate the process of building the Docker image, pushing it to Artifact Registry, and deploying it to the chosen compute target (e.g., GKE or Cloud Run).

##### Observability (Logging and Monitoring)

The application lacks a dedicated observability framework. Google Cloud's Operations Suite (formerly Stackdriver) provides a comprehensive solution.

*   **Cloud Logging**: Automatically aggregates logs from applications running on Google Cloud compute services. No code changes are required for standard log collection.
*   **Cloud Monitoring**: Provides dashboards, metrics, and alerting on the health and performance of the application and its underlying infrastructure (CPU, memory, request latency, etc.).

##### Storage

The application currently stores uploaded files, such as transaction attachments, as `LONGBLOB` data within the database [^8]. This approach is inefficient, increases database size, and does not scale well.

*   **Modernization Path**: Refactor the file upload logic in `BalanceFlowService` [^9] to use **Cloud Storage**. Files would be uploaded directly to a Cloud Storage bucket, and only the unique object identifier or URL would be stored in the database. This approach is more scalable, cost-effective, and performant.

##### Secret Management

Passwords and other secrets are currently managed through GitHub secrets and environment variables [^10].

*   **Best Practice**: Use **Secret Manager** to securely store and manage all application secrets, including database credentials and API keys. The application can be granted IAM permissions to access these secrets at runtime, eliminating the need to store them in configuration files or environment variables.

#### Proposed Migration Strategies

Based on the analysis, two primary migration strategies are proposed.

##### Strategy 1: Low-Effort Lift and Shift

This strategy focuses on migrating the application to Google Cloud with minimal code and architectural changes.

*   **Objective**: Get the application running quickly on Google Cloud to benefit from its reliable infrastructure.
*   **Migration Plan**:
    1.  **Database**: Provision a **Cloud SQL for MySQL** instance and migrate the existing database.
    2.  **Compute**: Provision a **Compute Engine** VM. Install Docker on the VM.
    3.  **Configuration**: Update the `application.properties` file to point to the Cloud SQL instance, using **Secret Manager** for the database password.
    4.  **CI/CD**: Modify the existing GitHub Actions workflow to:
        *   Build the Docker image.
        *   Push the image to **Artifact Registry**.
        *   Connect to the Compute Engine VM to pull and run the new container image.
    5.  **Networking**: Configure a **Cloud Load Balancer** to direct traffic to the VM and manage SSL.

##### Strategy 2: High-Benefit Modernization

This strategy involves refactoring the application to adopt cloud-native principles for improved scalability, resilience, and cost-efficiency.

*   **Objective**: Evolve the application into a scalable, serverless-first architecture that minimizes operational overhead.
*   **Migration Plan**:
    1.  **Database**: Migrate the database to **Cloud SQL for MySQL**.
    2.  **Storage**: Refactor the file upload functionality (`FlowFileService`) to use **Cloud Storage** instead of storing blobs in the database.
    3.  **Application Refactoring**:
        *   Break the monolithic application into smaller, independent microservices (e.g., `user-service`, `account-service`, `transaction-service`).
        *   Ensure each service is stateless to work with modern serverless compute platforms.
    4.  **Compute**: Deploy the new microservices to **Cloud Run**. For scheduled tasks or background jobs, use **Cloud Scheduler** to trigger **Cloud Functions**.
    5.  **CI/CD**: Implement a full CI/CD pipeline using **Cloud Build**. Each microservice would have its own build pipeline that automatically builds, tests, and deploys to Cloud Run upon code changes.
    6.  **Observability**: Leverage the native integration of Cloud Run with **Cloud Logging** and **Cloud Monitoring** to gain deep insights into application performance and health.

[^1]: Dockerfile: - Defines the container image for the Java application, starting from an Ubuntu base and running the application JAR.
[^2]: src/main/java/cn/biq/mn/security/CurrentSession.java: CurrentSession - A @SessionScope bean that holds user, book, group, and token information, indicating stateful session management.
[^3]: build.gradle: com.mysql:mysql-connector-j - The project includes the MySQL Connector/J dependency, indicating the use of a MySQL database.
[^4]: src/main/resources/application.properties: spring.datasource.url - Defines the JDBC connection string for a MySQL database, with placeholders for host, port, user, and password (e.g., `password=${DB_PASSWORD:******}`).
[^5]: src/main/resources/1.sql: - A SQL script containing UPDATE and ALTER TABLE statements, likely for database schema migrations and data adjustments.
[^6]: .github/workflows/docker-image-ali.yml: registry: registry.cn-hangzhou.aliyuncs.com - Specifies Aliyun Container Registry as the target for Docker images.
[^7]: .github/workflows/docker-image.yml: name: api docker hub image - Defines a GitHub Actions workflow to build and push a Docker image to Docker Hub.
[^8]: src/main/java/cn/biq/mn/flowfile/FlowFile.java: @Column(columnDefinition = \"LONGBLOB\", nullable = false) private byte[] data; - The `FlowFile` entity maps file content to a `LONGBLOB` database column, storing binary data directly in the database.
[^9]: src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java: addFile - This method handles the logic for attaching a file to a balance flow record.
[^10]: .github/workflows/docker-image-ali.yml: username: \"${{ secrets.ACR_USERNAME }}\" - The workflow uses secrets stored in GitHub to authenticate with the container registry.

### Shift to Compute Engine
#### Lift and Shift to Compute Engine

Migrating the MoneyNote API to Google Cloud can be achieved with minimal disruption by adopting a "lift-and-shift" strategy using Compute Engine. This approach involves moving the application to virtual machines on Google Cloud, which closely mimics a traditional on-premises or private server environment. Given that the application is already containerized with Docker [^1], this process is significantly simplified.

The core of this strategy is to deploy the existing Docker container onto a Compute Engine VM, requiring almost no changes to the application code itself. This allows the team to quickly establish a foothold in the cloud, deferring more complex modernization efforts.

##### Migrating to Compute Engine with Minimal Changes

The application can be deployed on a Compute Engine instance running a container-optimized OS or a standard Linux distribution with Docker installed. The existing `Dockerfile` can be used to build the container image.

The migration would follow these general steps:
1.  **Provision a Compute Engine VM**: Create a VM instance of an appropriate size (e.g., `e2-medium`) to host the application container.
2.  **Install Docker**: If not using a container-optimized OS, install Docker and Docker Compose on the VM.
3.  **Container Image Management**: The current CI/CD pipelines push images to Aliyun Container Registry and Docker Hub [^2]. To align with the Google Cloud ecosystem, the pipeline should be updated to push images to **Artifact Registry**.
4.  **Deploy the Container**: Pull the application image from Artifact Registry and run it using a `docker run` command or a simple `docker-compose.yml` file. The application's configuration, particularly database connection details, would be passed as environment variables.

##### External Dependency Analysis

The application has one primary external dependency: a MySQL database.

| Dependency | Location in Code | Current Setup | Recommended Google Cloud Service | Migration Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **MySQL Database** | `build.gradle` [^3]<br>`application.properties` [^4] | The application is configured to connect to a MySQL database. The connection string `jdbc:mysql://${DB_HOST...` indicates it expects an external database host. | **Cloud SQL for MySQL** | **1. Provision:** Create a new Cloud SQL for MySQL instance. This provides a fully managed, scalable, and secure database service, offloading administrative tasks like patching, backups, and replication.<br>**2. Migrate Data:** Use the **Database Migration Service** for a seamless migration from the existing database. Alternatively, perform a manual dump and import using the backup procedures mentioned in the project notes [^5].<br>**3. Reconfigure:** Update the application's environment variables (`DB_HOST`, `DB_USER`, `DB_PASSWORD`) to point to the new Cloud SQL instance. For enhanced security, connect via the Cloud SQL Auth Proxy running on the same VM or in a sidecar container. |

By migrating the database to a managed service like Cloud SQL, the project immediately benefits from increased reliability, automated backups, and easier scalability without requiring application code changes.

##### Leveraging Google Cloud Horizontals

Adopting Google Cloud offers access to-managed services that can enhance the application's operational posture with minimal effort.

| Google Cloud Service | Description | Integration Strategy |
| :--- | :--- | :--- |
| **Artifact Registry** | A fully managed, private repository for storing, and managing container images and other build artifacts. | Modify the existing GitHub Actions workflows to authenticate with Google Cloud and push the built Docker images to an Artifact Registry repository instead of Docker Hub or Aliyun ACR. This centralizes artifacts within the target cloud environment. |
| **Cloud Build** | A serverless CI/CD platform for building, testing, and deploying applications. | For a more integrated CI/CD pipeline, Cloud Build can be configured to listen for changes in the GitHub repository. It can automatically build the Docker image, push it to Artifact Registry, and even deploy it to the Compute Engine instance, streamlining the entire delivery process. |
| **Cloud Logging & Monitoring** | Centralized services for collecting, searching, and analyzing log data and performance metrics. | Install the **Ops Agent** on the Compute Engine VM. The agent will automatically collect logs from the application's `stdout` and system metrics, sending them to Cloud Logging and Cloud Monitoring. This enables centralized observability, dashboarding, and alerting without any code modifications. |
| **Cloud Storage** | Scalable and durable object storage for unstructured data. | The application currently stores uploaded files as `LONGBLOB` in the database [^6]. A highly recommended (though optional for initial migration) improvement is to modify the file upload logic in `BalanceFlowService` [^7] to save files to a Cloud Storage bucket. The database would then only store a reference to the object, drastically reducing database size and load. |
| **Cloud Load Balancing** | A globally distributed, high-performance load balancing service. | Place an External HTTP(S) Load Balancer pobreza of the Compute Engine instance(s). This provides a stable public IP address, enables easy SSL certificate management with Google-managed certificates, and offers DDoS protection. It also paves the way for future scaling by distributing traffic across multiple VMs. |
| **Secret Manager** | A secure and convenient storage system for API keys, passwords, and other sensitive data. | Instead of passing secrets like `DB_PASSWORD` directly as environment variables, they should be stored in Secret Manager. The application, with the right permissions, can then fetch these secrets at startup, which is a much more secure practice. |

#### Detailed Migration Plan to Compute Engine

This plan outlines the steps for a lift-and-shift migration of the MoneyNote API to Compute Engine.

##### Phase 1: Foundation and Scaffolding

1.  **Create Google Cloud Project**: Set up a new Google Cloud project to house all resources.
2.  **VPC Network Configuration**:
    *   Use the default VPC or create a new one.
    *   Configure firewall rules to allow incoming traffic for SSH (for management) and on the application port (`9092`).
3.  **Setup Artifact Registry**: Create a new Docker repository in Artifact Registry to store the application's container images.
4.  **IAM & Service Accounts**: Create a dedicated service account for the Compute Engine VM with the necessary permissions (e.g., Artifact Registry Reader, Cloud SQL Client, Secret Manager Secret Accessor, Logs Writer, Monitoring Metric Writer).

##### Phase 2: Database Migration

1.  **Provision Cloud SQL**: Create a new Cloud SQL for MySQL instance. Configure it with an appropriate machine size, and enable automated backups. For security, configure it to use a private IP address.
2.  **Data Migration**:
    *   Use the **Database Migration Service** to perform a continuous migration from the source database.
    *   Alternatively, perform a manual one-time migration by exporting the database schema and data and importing it into the new Cloud SQL instance.
3.  **Secure Credentials**: Store the new database username and password in **Secret Manager**.

##### Phase 3: CI/CD Pipeline Integration

1.  **Update GitHub Actions**:
    *   Add a step to the existing workflows to authenticate to Google Cloud using the service account created in Phase 1.
    *   Modify the `docker/build-push-action` step to push the built image to the Artifact Registry repository.
2.  **Test Pipeline**: Trigger a build to ensure the new image is successfully pushed to Artifact Registry.

##### Phase 4: Application Deployment

1.  **Create VM Template**: Create a Compute Engine instance template.
    *   Choose a suitable machine type (e.g., `e2-standard-2`).
    *   Select a container-optimized OS or a standard Linux distribution.
    *   Assign the service account created in Phase 1.
    *   Add a startup script to:
        *   Install/update the Ops Agent.
        *   Install Docker.
        *   Fetch secrets from Secret Manager.
        *   Pull the latest Docker image from Artifact Registry.
        *   Run the container, passing the database credentials and other configurations as environment variables.
2.  **Create Managed Instance Group (MIG)**: Create a MIG using the instance template. Start with a size of 1. A MIG allows for auto-healing and easy scaling in the future.

##### Phase 5: Expose, Test, and Cutover

1.  **Configure Load Balancer**:
    *   Set up an External HTTP(S) Load Balancer.
    *   Create a backend service that points to the MIG created in the previous step.
    *   Configure a health check to monitor the application's health on its port.
    *   Create a frontend with a reserved static IP address and a Google-managed SSL certificate for your domain.
2.  **Update DNS**: Point the application's domain name (e.g., `api.moneynote.com`) to the load balancer's static IP address.
3.  **Validation**:
    *   Verify that logs and metrics are appearing in Cloud Logging and Cloud Monitoring.
    *   Conduct thorough end-to-end testing of the application to ensure all functionalities, including user registration, transaction recording, and reporting, are working as expected.
4.  **Decommission**: Once the Google Cloud deployment is stable and validated, the old environment can be decommissioned.

[^1]: Dockerfile: FROM ubuntu:23.04 - Defines the base image and steps to containerize the application.
[^2]: .github/workflows/docker-image-all-ali.yml: build-push-action - This step in the GitHub Actions workflow pushes the built Docker image to a container registry.
[^3]: build.gradle: runtimeOnly 'com.mysql:mysql-connector-j' - This dependency declaration indicates that the project uses the MySQL JDBC driver at runtime.
[^4]: application.properties: spring.datasource.url=jdbc:mysql://${DB_HOST:127.0.0.1}:${DB_PORT:3306}/${DB_NAME:moneynote} - This property defines the JDBC connection string for a MySQL database.
[^5]: notes/data_backup.txt: 1. 使用phpmyadmin的导入导出功能。 - Mentions using phpmyadmin for data import/export, a viable method for manual database migration.
[^6]: src/main/java/cn/biq/mn/flowfile/FlowFile.java: private byte[] data; - The `data` field is defined as a byte array and annotated with `@Lob` and `@Column(columnDefinition = "LONGBLOB")`, indicating that file contents are stored directly in the database as large binary objects.
[^7]: src/main/java/cn/biq/mn/balanceflow/BalanceFlowService.java: addFile - This method handles the logic for attaching a file to a transaction record.

### Modernize to Kubernetes Engine
#### User Journeys

This section outlines the primary user journeys and features of the MoneyNote application. Each journey is broken down into core user interactions, the underlying business requirements derived from the codebase, and a practical example of the user's flow through the system.

##### 1. Monitoring Financial Situation

This journey focuses on providing the user with a high-level, consolidated overview of their financial health, enabling them to understand their net worth at a glance.

###### Core Interactions

The user logs into the application and accesses a dashboard or overview screen. This screen presents key financial metrics, including their total assets, total liabilities (debts), and overall net worth. The user can also view graphical representations, such as pie charts, that break down their assets and debts by individual accounts, providing a clear picture of where their money is held and owed.

###### Business Requirements

The system's functionality is designed to meet the following business requirements for financial monitoring:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-FIN-01 | The system must calculate and display the user's total assets. Assets are defined as the sum of balances in `CHECKING` and `ASSET` type accounts [^1]. | `AccountService.java`: `getAssets()` |
| REQ-FIN-02 | The system must calculate and display the user's total liabilities. Liabilities are defined as the sum of balances in `CREDIT` and `DEBT` type accounts [^2]. | `AccountService.java`: `getDebts()` |
| REQ-FIN-03 | The system must calculate and display the user's net worth, defined as Total Assets minus Total Liabilities. | `AccountService.java`: `overview()` |
| REQ-FIN-04 | Only accounts explicitly marked for inclusion (`include=true`) shall be part of the aggregated financial summaries [^1] [^2]. | `AccountRepository.java`: `findAllByGroupAndTypeAndEnableAndInclude(...)` |
| REQ-FIN-05 | All financial summaries involving multiple currencies must be converted to the user's active group's default currency for consistent reporting [^3]. | `AccountService.java`: `overview()`, `statistics()` |
| REQ-FIN-06 | The system must provide a dedicated API endpoint (`/accounts/overview`) to retrieve the calculated totals for assets, debts, and net worth [^4]. | `AccountController.java`: `handleOverview()` |
| REQ-FIN-07 | The system must provide a reporting endpoint (`/reports/balance`) that structures asset and debt data for visualization, such as in charts [^5]. | `ReportController.java`: `handleBalance()` |
| REQ-FIN-08 | In reports, debt balances (which are often negative) must be presented as positive values to accurately represent the magnitude of the liability [^6]. | `ReportService.java`: `reportBalance()` |

###### Example User Flow

1.  **Login and Initialization**: The user logs in. The application calls the `/initState` endpoint to load their profile and default settings, including their default group and its associated currency (e.g., USD) [^7].
2.  **Navigate to Dashboard**: The user navigates to the "Overview" or "Dashboard" page in the user interface.
3.  **API Request for Overview**: The frontend makes a GET request to the `/accounts/overview` endpoint [^4].
4.  **Backend Processing**:
    *   The `AccountService.overview()` method is executed [^3].
    *   It fetches all asset accounts (`CHECKING`, `ASSET`) and debt accounts (`CREDIT`, `DEBT`) that are enabled and marked for inclusion.
    *   It iterates through each account. If an account's currency is different from the group's default currency (e.g., a EUR account in a USD group), it calls the `CurrencyService` to get the conversion rate and calculate the balance in the default currency [^8].
    *   The service sums the converted balances to produce `totalAssets` and `totalDebts`, then calculates `netWorth`.
5.  **Display Data**: The API returns an array containing the three key values: `[totalAssets, totalDebts, netWorth]`. The UI displays these figures prominently.
6.  **Visualize Breakdown**: The UI makes a separate call to `/reports/balance` to fetch data for pie charts. This endpoint provides a detailed list of individual asset and debt accounts with their respective balances converted to the default currency, allowing the user to see the composition of their assets and liabilities [^6].

##### 2. Tracking Incomes & Expenses

This is the core data-entry journey, allowing users to meticulously record their daily financial transactions, including expenditures and earnings.

###### Core Interactions

The user initiates the creation of a new financial record. They are presented with a form to add an expense or an income, where they can input details such as a descriptive title, the transaction amount, date, the account used, and one or more categories. Optionally, they can add tags for finer-grained analysis and specify a payee. Once saved, the transaction appears in their record list, and the corresponding account balance is updated. The user can also view, modify, and delete past transactions.

###### Business Requirements

The system supports detailed transaction tracking through the following requirements:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-TRK-01 | The system must allow the creation of financial transactions with distinct types: `EXPENSE`, `INCOME`, `TRANSFER`, and `ADJUST` [^9]. | `BalanceFlow.java`: `FlowType` enum |
| REQ-TRK-02 | An `EXPENSE` transaction must debit (decrease) the balance of the selected account, while an `INCOME` transaction must credit (increase) it [^10]. | `BalanceFlowService.java`: `confirmBalance()` |
| REQ-TRK-03 | Each transaction (`BalanceFlow`) must be associated with a specific `Book` to support compartmentalized bookkeeping [^11]. | `BalanceFlow.java`: `book` field |
| REQ-TRK-04 | Expense and income transactions must be classifiable under one or more `Category`s. The sum of amounts across all assigned categories must equal the transaction's total amount [^12]. | `BalanceFlowService.java`: `add()` |
| REQ-TRK-05 | The system must support multi-category transactions, where a single transaction's amount is split across several categories [^13]. | `BalanceFlowAddForm.java`: `categories` list |
| REQ-TRK-06 | Transactions can be further organized with multiple descriptive `Tag`s [^14]. | `BalanceFlow.java`: `tags` field |
| REQ-TRK-07 | Deleting a transaction must correctly revert the balance change on the associated account(s) to maintain data integrity [^15]. | `BalanceFlowService.java`: `refundBalance()` |
| REQ-TRK-08 | Updating a transaction is implemented as an atomic operation of deleting the old record and creating a new one, preserving attached files and ensuring balance accuracy [^16]. | `BalanceFlowService.java`: `update()` |

###### Example User Flow

1.  **Initiate Transaction**: While viewing the transaction list within the "Personal" `Book`, the user clicks the "Add Expense" button.
2.  **Fill Form**: A form appears. The user fills in the details:
    *   **Account**: Selects "My Credit Card" (a `CREDIT` type account).
    *   **Categories**:
        *   Clicks "Add Category", selects "Groceries", and enters an amount of `50.00`.
        *   Clicks "Add Category" again, selects "Household Goods", and enters `25.00`.
    *   **Date**: Selects yesterday's date from a calendar picker.
    *   **Payee**: Selects "Local Supermarket".
    *   **Tags**: Adds the "weekly-shopping" tag.
    *   **Notes**: Types "Stocked up on pantry items".
3.  **Submit Form**: The user clicks "Save".
4.  **API Request**: The frontend sends a `POST` request to the `/balance-flows` endpoint with the form data [^17].
5.  **Backend Processing**:
    *   The `BalanceFlowService.add()` method validates the input [^12]. It calculates the total amount of the transaction by summing the amounts from the categories (`50.00 + 25.00 = 75.00`).
    *   A new `BalanceFlow` entity of type `EXPENSE` is created.
    *   Because the transaction is confirmed by default, the `confirmBalance()` method is called. This reduces the balance of the "My Credit Card" account by `75.00` [^10].
    *   `CategoryRelation` and `TagRelation` entities are created to link the transaction to its respective classifications.
6.  **Confirmation**: The transaction is saved to the database. The UI refreshes the transaction list, displaying the new `75.00` expense. The balance of "My Credit Card" is updated on the accounts screen.

##### 3. Attaching a Financial Record File

This journey provides users with the ability to link digital documents, such as receipts or invoices, directly to their financial transactions for better record-keeping and auditing.

###### Core Interactions

After recording a transaction, the user opens its detailed view. They find an "Attachments" section and an option to upload a file. The user selects a file (e.g., a photo of a receipt or a PDF invoice) from their local device and uploads it. The file is now linked to the transaction. They can later view a list of all attachments for that transaction, open any file to view its content, or delete it if it's no longer needed.

###### Business Requirements

The system must support file attachments with the following capabilities:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-FILE-01 | Users must be able to upload one or more files to any `BalanceFlow` entity [^18]. | `BalanceFlowController.java`: `handleAddFile()` |
| REQ-FILE-02 | The system must validate uploaded files to ensure they are of a supported content type (e.g., PDF, PNG, JPG, JPEG) [^19]. | `FileValidator.java`, `ValidFile.java` |
| REQ-FILE-03 | The system must store the file's binary data, content type, original filename, and size. The binary data is stored as a `LONGBLOB` in the database [^20]. | `FlowFile.java` |
| REQ-FILE-04 | Users must be able to retrieve and view a list of all files associated with a specific transaction [^21]. | `BalanceFlowController.java`: `handleFiles()` |
| REQ-FILE-05 | The system must provide an endpoint to serve the raw content of a specific file with the correct `Content-Type` header, allowing it to be viewed in the browser or downloaded [^22]. | `FlowFileController.java`: `handleView()` |
| REQ-FILE-06 | Users must be able to delete a previously uploaded file. This action must only remove the file and not the associated financial transaction [^23]. | `FlowFileController.java`: `handleDelete()` |

###### Example User Flow

1.  **Select Transaction**: The user has previously recorded an expense for "New Office Chair" amounting to `250.00`. They click on this transaction in their list to open the details view.
2.  **Upload File**: In the "Attachments" area of the transaction details, the user clicks the "Add File" or "Upload Receipt" button. This opens their device's file selection dialog.
3.  **Choose File**: The user selects the PDF invoice for the chair, `invoice-12345.pdf`.
4.  **API Request**: The frontend sends a multipart `POST` request to `/balance-flows/{id}/addFile`, where `{id}` is the ID of the "New Office Chair" transaction [^18].
5.  **Backend Processing**:
    *   The `BalanceFlowService.addFile()` method receives the file.
    *   The `@ValidFile` annotation triggers `FileValidator` to check if the file's content type is supported [^19].
    *   The service creates a new `FlowFile` entity. It reads the file's bytes and populates the entity with the binary data, content type (`application/pdf`), size, and original filename.
    *   The `FlowFile` is linked to the `BalanceFlow` entity via the `flow` field and saved to the database [^20].
6.  **Confirmation**: The API returns details of the newly created file record. The UI updates to show `invoice-12345.pdf` in the attachments list, with options to view or delete it.

##### 4. Supporting Multiple Books

This journey enables users to manage separate sets of financial records within a single account, such as for personal use, a side business, or different projects.

###### Core Interactions

A user who wants to keep their business finances separate from their personal ones decides to create a new ledger. They navigate to the "Books" management section and choose to create a new `Book`. They are given the option to start from scratch, use a predefined template (e.g., "Restaurant Ledger"), or copy the structure of an existing book. After creating the new `Book`, they can switch their active context to it, ensuring that all subsequent transactions, categories, and payees are recorded within that specific ledger.

###### Business Requirements

The multi-book functionality is governed by these requirements:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-BOOK-01 | The system must allow a user to create and manage multiple `Book` entities [^24]. | `BookController.java`: `handleAdd()` |
| REQ-BOOK-02 | Each `Book` must function as a self-contained ledger, with its own distinct set of `Categories`, `Tags`, and `Payees` [^25]. | `Book.java`: `categories`, `tags`, `payees` fields |
| REQ-BOOK-03 | The system must provide predefined `BookTemplate`s that users can select to quickly set up a new book with relevant categories and tags [^26]. | `BookService.java`: `addByTemplate()` |
| REQ-BOOK-04 | Templates for books are loaded from a JSON configuration file, allowing for easy updates and additions without code changes [^27]. | `book_tpl.json`, `BookTplDataLoader.java` |
| REQ-BOOK-05 | Users must be able to create a new book by duplicating the entire structure (categories, tags, payees) of an existing book [^28]. | `BookService.java`: `addByBook()` |
| REQ-BOOK-06 | Users must be able to set a default `Book` for their session. All data entry and viewing will be scoped to this active book until it is changed [^29]. | `UserController.java`: `handleSetDefaultBook()` |
| REQ-BOOK-07 | All transaction-related data, including balance flows, categories, and payees, must be queryable and filterable by `Book` ID [^30]. | `CategoryQueryForm.java`, `PayeeQueryForm.java` |

###### Example User Flow

1.  **Navigate to Books**: The user goes to the "Settings" -> "Manage Books" page.
2.  **Initiate Creation**: They click the "Create Book" button. The UI presents several options.
3.  **Select Template**: The user chooses "Create from Template". A list of available templates, such as "Daily Life" and "Restaurant Ledger," is displayed [^27].
4.  **Choose and Configure**: The user selects "Restaurant Ledger". A form prompts them for a name and default currency for the new book. They enter "My Cafe" and select "EUR" as the currency.
5.  **API Request**: The user clicks "Create". The frontend sends a `POST` request to `/books/template` with the new book's details and the selected template ID [^26].
6.  **Backend Processing**:
    *   The `BookService.addByTemplate()` method is invoked.
    *   It first creates a new `Book` entity named "My Cafe".
    *   It then loads the "Restaurant Ledger" template from `book_tpl.json`.
    *   It iterates through the categories, tags, and payees defined in the template JSON and creates corresponding new entities in the database, linking them all to the "My Cafe" book [^28].
7.  **Confirmation and Activation**: The new book is created. The user sees "My Cafe" in their list of books. They can then click on it and set it as their active book for recording cafe-related income and expenses.

##### 5. Supporting Multiple Currencies

This journey addresses the needs of users who deal with more than one currency, enabling them to record transactions in their original currency and view consolidated reports in a single base currency.

###### Core Interactions

A user has bank accounts in both the United States (USD) and Europe (EUR). They add both accounts to the application, specifying the correct currency for each. When they record a transaction from their EUR account, they enter the amount in EUR. The system, aware that the user's primary reporting currency is USD, fetches the current exchange rate and calculates the equivalent value in USD. In their financial overview, the balance of the EUR account is shown in its converted USD value, contributing to a unified financial summary.

###### Business Requirements

The multi-currency feature is built upon the following requirements:

| Requirement ID | Description | Implemented In |
| :--- | :--- | :--- |
| REQ-CUR-01 | The system must maintain a list of world currencies with their exchange rates relative to a base currency (USD) [^31]. | `currency.json`, `CurrencyDataLoader.java` |
| REQ-CUR-02 | Each `Account` entity must be assigned a specific `currencyCode` [^32]. | `Account.java`: `currencyCode` field |
| REQ-CUR-03 | Each `Book` must have a `defaultCurrencyCode` which serves as the base currency for all reporting within that book [^33]. | `Book.java`: `defaultCurrencyCode` field |
| REQ-CUR-04 | For transactions where the account currency differs from the book's default currency, the system must store both the original `amount` and the `convertedAmount` in the book's currency [^34]. | `BalanceFlow.java`: `amount`, `convertedAmount` fields |
| REQ-CUR-05 | The system must provide a mechanism to refresh currency exchange rates from an external API service to ensure they are up-to-date [^35]. | `CurrencyService.java`: `refreshCurrency()` |
| REQ-CUR-06 | All aggregated financial reports (e.g., net worth, category spending) must convert all transaction amounts into a single, consistent currency (the group's default) before aggregation [^3]. | `AccountService.java`: `overview()` |
| REQ-CUR-07 | The system must expose an API endpoint to calculate the value of an amount from one currency to another (`/currencies/calc`) [^36]. | `CurrencyController.java`: `handleCalc()` |

###### Example User Flow

1.  **Account Setup**: The user has already configured their accounts: "Bank of America" (USD) and "BNP Paribas" (EUR). Their group's default currency is set to USD.
2.  **Record Foreign Transaction**: The user needs to record a `€50` dinner expense paid from their "BNP Paribas" account. They create a new expense.
3.  **UI Assistance**:
    *   They select the "BNP Paribas" account. The UI detects its currency is EUR, which is different from the group's default of USD.
    *   The UI makes a background call to `/currencies/rate?from=EUR&to=USD` to fetch the conversion rate (e.g., 1.08).
    *   It automatically calculates the converted amount (`50 * 1.08 = 54.00`) and displays "$54.00" next to the amount field, allowing the user to override it if needed.
4.  **Submit Transaction**: The user confirms the details and saves. The frontend sends a `POST` request to `/balance-flows` with `amount: 50` (in EUR) and `convertedAmount: 54` (in USD).
5.  **Backend Processing**:
    *   The `BalanceFlowService` saves the transaction, storing both the original and converted amounts [^34].
    *   The balance of the "BNP Paribas" account is correctly reduced by `€50`.
6.  **Consolidated Reporting**: Later, when the user generates a monthly spending report, this transaction contributes `$54` to the total, allowing it to be aggregated seamlessly with other USD-based transactions.

[^1]: AccountService.java: getAssets() - This method retrieves all accounts of type CHECKING and ASSET that are enabled and included in summaries.
[^2]: AccountService.java: getDebts() - This method retrieves all accounts of type CREDIT and DEBT that are enabled and included in summaries.
[^3]: AccountService.java: overview() - This method calculates total assets, debts, and net worth by converting each account's balance to the group's default currency.
[^4]: AccountController.java: handleOverview() - This endpoint exposes the financial overview functionality through a GET request.
[^5]: ReportController.java: handleBalance() - This endpoint provides asset and debt data structured for reporting and charting.
[^6]: ReportService.java: reportBalance() - This service prepares the data for balance reports, negating debt balances for correct representation as liabilities.
[^7]: UserService.java: getInitState() - This method provides the initial session data for a logged-in user, including their default book and group settings.
[^8]: CurrencyService.java: convert() - This utility method calculates the exchange rate between a 'from' and 'to' currency code.
[^9]: BalanceFlow.java: FlowType - This enum defines the four types of financial transactions supported by the system.
[^10]: BalanceFlowService.java: confirmBalance() - This method applies the financial impact of a transaction to the corresponding account balances.
[^11]: BalanceFlow.java: book - The `BalanceFlow` entity has a mandatory association with a `Book` entity.
[^12]: BalanceFlowService.java: add() - The logic in this method ensures that expenses/incomes have categories and calculates the total amount from them.
[^13]: BalanceFlowAddForm.java: categories - The transaction creation form accepts a list of category-amount pairs, enabling multi-category entries.
[^14]: BalanceFlow.java: tags - The `BalanceFlow` entity has a one-to-many relationship with `TagRelation`, allowing multiple tags per transaction.
[^15]: BalanceFlowService.java: refundBalance() - This method reverts the balance changes when a transaction is deleted.
[^16]: BalanceFlowService.java: update() - This method handles transaction updates by creating a new record and deleting the old one, while re-associating any attached files.
[^17]: BalanceFlowController.java: handleAdd() - This is the API endpoint for creating a new balance flow transaction.
[^18]: BalanceFlowController.java: handleAddFile() - This endpoint handles the uploading of a file and associating it with a transaction.
[^19]: FileValidator.java: isValid() - This custom validator checks if the uploaded file's content type is in a list of allowed types.
[^20]: FlowFile.java: data - This field in the `FlowFile` entity is defined as a `LONGBLOB` to store the binary content of the uploaded file.
[^21]: BalanceFlowController.java: handleFiles() - This endpoint returns a list of all files attached to a given transaction.
[^22]: FlowFileController.java: handleView() - This endpoint serves the raw file data with the appropriate `Content-Type` header.
[^23]: FlowFileController.java: handleDelete() - This endpoint deletes a `FlowFile` entity by its ID.
[^24]: BookController.java: handleAdd() - The endpoint for creating a new, empty `Book`.
[^25]: Book.java: categories, tags, payees - These fields establish that a book is the root owner for its own set of categories, tags, and payees.
[^26]: BookController.java: handleAddByTemplate() - This endpoint facilitates the creation of a new book from a predefined template.
[^27]: book_tpl.json: - This JSON file contains the definitions for all available book templates, including their categories and tags.
[^28]: BookService.java: addByBook() - This service method contains the logic to copy the structure from one book to a new one.
[^29]: UserController.java: handleSetDefaultBook() - This endpoint allows a user to change their active book for the current session.
[^30]: CategoryQueryForm.java: bookId - Query forms for entities like Category and Payee include a `bookId` to filter results by the active book.
[^31]: currency.json: - This file contains a list of supported currencies and their default exchange rates against USD.
[^32]: Account.java: currencyCode - Each `Account` has a mandatory `currencyCode` to define the currency of its balance.
[^33]: Book.java: defaultCurrencyCode - Each `Book` has a default currency used for consolidated reporting.
[^34]: BalanceFlow.java: amount, convertedAmount - These two fields store the transaction value in its original currency and its equivalent in the book's default currency.
[^35]: CurrencyService.java: refreshCurrency() - This method calls an external API to fetch the latest exchange rates and update the in-memory currency list.
[^36]: CurrencyController.java: handleCalc() - This endpoint provides a utility to convert an amount between two specified currencies.

### Modernize to Cloud Run
#### User Journeys

This section outlines the primary user journeys and features of the MoneyNote application, reverse-engineered from the codebase. Each journey is detailed from the perspective of a senior business analyst, describing the user's interactions, the underlying business requirements the system fulfills, and an example flow of execution.

##### Journey 1: Monitoring Financial Situation

This journey describes how a user assesses their overall financial health by viewing aggregated summaries and reports. It is the primary "read-only" or analytical journey, providing the user with a high-level snapshot of their assets, debts, and net worth.

###### Core Interactions

1.  **Dashboard Overview**: Upon login, the user is presented with a primary dashboard that displays their most critical financial metrics. This includes Total Assets, Total Debts, and the resulting Net Worth, providing an immediate understanding of their financial position.
2.  **Account Drill-Down**: From the dashboard, the user can navigate to a detailed list of all their financial accounts. This view lists each account (e.g., checking, savings, credit cards, loans) along with its current balance.
3.  **Visual Reporting**: The user can access a dedicated reporting section to visualize their financial data. A key report is the "Balance Report," which typically uses pie charts to illustrate the composition of their assets and debts, showing which accounts contribute most to each category.

###### Business Requirements

| Requirement ID | Description | Technical Implementation |
| :--- | :--- | :--- |
| FIN-MON-01 | The system must calculate and display a user's total assets, total liabilities (debts), and net worth. | The `AccountService.overview()` method orchestrates this calculation. It separates accounts into assets and debts and sums their balances [^1]. |
| FIN-MON-02 | Asset accounts are defined as types `CHECKING` and `ASSET`. | The `AccountService.getAssets()` method specifically queries for accounts of type `CHECKING` and `ASSET` that are enabled and included in reports [^2]. |
| FIN-MON-03 | Debt accounts are defined as types `CREDIT` and `DEBT`. | The `AccountService.getDebts()` method queries for accounts of type `CREDIT` and `DEBT` that are enabled and included in reports [^3]. |
| FIN-MON-04 | All account balances must be converted to the user's group-defined default currency before aggregation to ensure a consistent summary. | The `overview()` and `statistics()` methods in `AccountService` use `CurrencyService.convert()` to normalize all balances to the group's `defaultCurrencyCode` before summing them [^4]. |
| FIN-MON-05 | The system must provide a visual breakdown of assets and debts by individual account. | The `ReportService.reportBalance()` method generates two lists of `ChartVO` objects, one for assets and one for debts, which are designed to be consumed by a charting library on the frontend [^5]. |
| FIN-MON-06 | Users can exclude certain accounts from the main financial overview calculations. | The `Account` entity contains an `include` boolean flag. All overview and reporting queries filter accounts where `include` is `true` [^6]. |

###### Example User Flow: Checking Net Worth

1.  **Login**: The user, Alice, logs into the MoneyNote application. The system authenticates her and establishes her session.
2.  **Initial State Load**: The frontend makes a `GET` request to `/api/v1/initState`. The backend `UserService.getInitState()` fetches Alice's user profile, her default group, and default book settings.
3.  **Dashboard Display**: The main dashboard UI is rendered. To populate the financial overview widget, the frontend sends a `GET` request to `/api/v1/accounts/overview`.
4.  **Backend Calculation**: The `AccountController` routes the request to `AccountService.overview()`. This service:
    *   Fetches all of Alice's asset accounts (`CHECKING`, `ASSET`) and debt accounts (`CREDIT`, `DEBT`).
    *   For each account, it converts the `balance` to the group's default currency (e.g., converting a EUR balance to USD).
    *   It sums the converted balances to get a total asset value and a total debt value.
5.  **API Response**: The API responds with an array containing the total assets, total debts, and the calculated net worth (Assets - Debts).
6.  **UI Render**: The dashboard widget updates, displaying Alice's key financial figures, such as "Total Assets: $50,000," "Total Debts: $15,000," and "Net Worth: $35,000."

##### Journey 2: Tracking Incomes & Expenses

This is the fundamental data-entry journey of the application. It details the process a user follows to record their day-to-day financial transactions, such as expenses, incomes, and transfers between accounts.

###### Core Interactions

1.  **Select Book**: The user first ensures they are in the correct financial "Book" (e.g., "Personal" vs. "Business").
2.  **Initiate Transaction**: The user clicks a button like "Add Expense" or "Add Income."
3.  **Complete Form**: A form is presented where the user provides the transaction details:
    *   Selects the source/destination account.
    *   Splits the total amount across one or more spending/earning categories.
    *   Optionally selects a Payee (e.g., "Starbucks," "ACME Corp").
    *   Optionally adds descriptive tags, a title, and notes.
4.  **Save Transaction**: The user saves the form. The system records the transaction and, if it is marked as "confirmed," immediately updates the balance of the affected account(s).
5.  **Review and Edit**: The user can view a list of recent transactions. They can select any transaction to view its full details, edit the information, or delete it entirely.

###### Business Requirements

| Requirement ID | Description | Technical Implementation |
| :--- | :--- | :--- |
| FIN-TRK-01 | The system must allow users to create financial records of type `EXPENSE`, `INCOME`, and `TRANSFER`. | The `BalanceFlow` entity has a `FlowType` enum which includes these types. The `BalanceFlowAddForm` allows the user to specify the type upon creation [^7]. |
| FIN-TRK-02 | Every transaction must belong to a specific `Book`, ensuring data isolation. | The `BalanceFlow` entity has a mandatory `ManyToOne` relationship with the `Book` entity [^8]. |
| FIN-TRK-03 | Expense and Income transactions can be split across multiple categories, each with a specific amount. The transaction's total amount is the sum of these splits. | A `BalanceFlow` can have a `Set` of `CategoryRelation` objects. The service logic in `BalanceFlowService.add()` calculates the total amount by summing the amounts from the `CategoryRelationForm` list [^9]. |
| FIN-TRK-04 | Transactions can be marked as "Confirmed" to immediately impact account balances, or "Unconfirmed" to be saved as a draft. | The `BalanceFlow` entity has a `confirm` boolean flag. The `confirmBalance()` method in `BalanceFlowService` contains the logic to update account balances only if this flag is true [^10]. |
| FIN-TRK-05 | Recording a confirmed expense must decrease the account balance. Recording a confirmed income must increase it. | The `confirmBalance()` method subtracts from the account balance for `FlowType.EXPENSE` and adds to it for `FlowType.INCOME` [^10]. |
| FIN-TRK-06 | Deleting a confirmed transaction must correctly reverse the balance change on the associated account(s). | The `refundBalance()` method in `BalanceFlowService` is called before deleting a `BalanceFlow` entity. It adds back expense amounts and subtracts income amounts to restore the previous balance [^11]. |
| FIN-TRK-07 | Users must be able to modify the details of an existing transaction. | The `BalanceFlowService.update()` method handles modifications by effectively deleting the old transaction (and refunding its balance impact) and creating a new one with the updated details [^12]. |

###### Example User Flow: Recording a Multi-Category Grocery Bill

1.  **Navigation**: Alice selects her "Household" book from the main navigation. She then clicks "Add Expense."
2.  **Form Entry**: A form appears.
    *   **Account**: She selects her "Debit Card" account.
    *   **Payee**: She selects "Local Supermarket."
    *   **Categories**: She clicks "Add Category Split."
        *   Row 1: She selects the "Groceries" category and enters "$50."
        *   Row 2: She selects the "Household Supplies" category and enters "$15."
    *   **Confirmation**: She leaves the "Confirm" checkbox ticked.
3.  **Submission**: Alice clicks "Save." The frontend constructs a JSON payload and sends a `POST` request to `/api/v1/balance-flows`.
4.  **Backend Processing**: The request is handled by `BalanceFlowService.add()`:
    *   It validates that the categories are not duplicated and are within limits.
    *   It sums the category amounts ($50 + $15) to determine the total transaction `amount` is $65.
    *   It creates a new `BalanceFlow` entity and two associated `CategoryRelation` entities.
    *   It calls `confirmBalance()`. Since the type is `EXPENSE`, it retrieves the "Debit Card" `Account` and updates its balance by subtracting $65.
5.  **Response and UI Update**: The API returns a success response. The UI displays a confirmation message and adds the new $65 expense to the top of the transaction list.

##### Journey 3: Attaching Files to Financial Records

This journey enables users to attach supporting documents, such as receipts or invoices, to their transactions. This provides context and proof for financial records, enhancing auditability and personal record-keeping.

###### Core Interactions

1.  **Access Attachment Feature**: While creating a new transaction or editing an existing one, the user finds an "Attach File" or "Add Receipt" button.
2.  **File Selection**: Clicking the button opens the device's native file explorer. The user selects the relevant file (e.g., a photo of a paper receipt or a PDF invoice).
3.  **Upload and Link**: The selected file is uploaded to the server and is permanently linked to the transaction record.
4.  **View and Manage Attachments**: When viewing the transaction's details, the user sees a list of all attached files. They can click on any file to view it in their browser or download it. They also have the option to delete attachments.

###### Business Requirements

| Requirement ID | Description | Technical Implementation |
| :--- | :--- | :--- |
| FIN-FLE-01 | The system must allow one or more files to be associated with a single `BalanceFlow` record. | The `BalanceFlow` entity has a `OneToMany` relationship with the `FlowFile` entity, allowing a collection of files per flow [^13]. |
| FIN-FLE-02 | The system must restrict uploaded file types to a predefined list (e.g., PDF, PNG, JPG/JPEG). | A custom `@ValidFile` annotation and its corresponding `FileValidator` class check the `contentType` of the uploaded file against a supported list [^14]. |
| FIN-FLE-03 | The system must store the file's binary data, original filename, size, and MIME type. | The `FlowFile` entity contains fields for `data` (as a `LONGBLOB`), `originalName`, `size`, and `contentType` [^15]. |
| FIN-FLE-04 | File uploads must be constrained by a maximum size limit. | The `application.properties` file configures server-wide multipart request limits (`spring.servlet.multipart.max-file-size=100MB`) [^16]. |
| FIN-FLE-05 | Users must be able to securely retrieve and view the content of an attached file. | The `FlowFileController.handleView()` endpoint serves the file's byte data. Access is secured by requiring the file's ID and creation timestamp in the request, making the URL difficult to guess [^17]. |
| FIN-FLE-06 | Users must have the ability to delete a previously attached file from a transaction. | The `/flow-files/{id}` `DELETE` endpoint in `FlowFileController` allows for the removal of a `FlowFile` entity, but only after verifying the user has rights to the parent transaction [^18]. |

###### Example User Flow: Attaching an E-Receipt to an Expense

1.  **Find Transaction**: Alice has an existing expense record for an online purchase of a new monitor for $300. She wants to attach the PDF receipt she received via email. She navigates to the transaction details page.
2.  **Initiate Upload**: She clicks the "Add Attachment" button. A file dialog opens.
3.  **Select File**: She selects `monitor_receipt.pdf` from her computer.
4.  **API Request**: The frontend initiates a `POST` request to the endpoint `/api/v1/balance-flows/{id}/addFile`, where `{id}` is the ID of the monitor expense. The request is of type `multipart/form-data` and contains the file data.
5.  **Backend Handling**: The `BalanceFlowController` receives the request.
    *   The `@ValidFile` annotation triggers the `FileValidator`, which checks if the file's content type is `application/pdf`. It is, so validation passes.
    *   The request is passed to `BalanceFlowService.addFile()`.
    *   This service creates a new `FlowFile` entity, populates it with the file's bytes, metadata (name, size, type), and links it to the `BalanceFlow` record.
    *   The `FlowFile` entity is saved to the database.
6.  **UI Update**: The service returns details of the newly created `FlowFile`. The frontend updates the attachments section on the transaction details page to show a link to `monitor_receipt.pdf`. Alice can now click this link to view the receipt at any time.

##### Journey 4: Using Multiple Financial Books

This journey caters to users who need to manage separate, isolated sets of financial records. A common use case is separating personal finances from small business finances. Each "Book" acts as a self-contained ledger with its own settings and data.

###### Core Interactions

1.  **Book Creation**: A user can create a new Book. They are given options to:
    *   Start with a blank slate.
    *   Use a predefined template (e.g., "Daily Life," "Restaurant Business") that comes pre-populated with relevant categories and tags.
    *   Duplicate one of their existing Books, copying all its settings.
2.  **Book Switching**: The user interface provides a clear mechanism (like a dropdown menu) to switch the active Book.
3.  **Contextual Operations**: Once a Book is selected, all subsequent actions—adding transactions, creating accounts (within the group), managing categories, and viewing reports—are performed exclusively within the context of that active Book.
4.  **Book Management**: The user can view a list of all their books, edit their properties (like name or default accounts), and set a global default book for their user profile.

###### Business Requirements

| Requirement ID | Description | Technical Implementation |
| :--- | :--- | :--- |
| FIN-BK-01 | The system must support the creation of multiple `Book` entities within a user's `Group`. | The `Book` entity has a `ManyToOne` relationship with the `Group` entity, allowing a group to contain multiple books [^19]. |
| FIN-BK-02 | Each Book must act as a container, isolating its own set of `Category`, `Tag`, and `Payee` records. | `Category`, `Tag`, and `Payee` entities each have a mandatory `ManyToOne` relationship with the `Book` entity, ensuring they are scoped to a single book [^20]. |
| FIN-BK-03 | Users must be able to create new books from predefined templates. | The `BookService.addByTemplate()` method uses a `BookTemplate` object (loaded from `book_tpl.json`) to create a new book and populate its associated categories, tags, and payees [^21]. |
| FIN-BK-04 | Users must be able to create a new book by copying an existing one. | The `BookService.addByBook()` method first creates a new book and then copies the categories, tags, and payees from the source book to the new one [^22]. |
| FIN-BK-05 | A user's session must have an active "current book" context, which filters all data views and actions. | The `CurrentSession` bean holds a reference to the active `Book`. Services like `CategoryService` use `sessionUtil.getCurrentBook()` to scope their database queries [^23]. |
| FIN-BK-06 | Users can specify a default book for their profile, which is automatically selected upon login. | The `User` entity has a `defaultBook` field. The `UserService.setDefaultBook()` method allows users to change this preference [^24]. |

###### Example User Flow: Creating and Using a Separate Business Book

1.  **Creation**: Alice, who uses MoneyNote for her personal finances, decides to start tracking the finances for her freelance design work separately. She navigates to the "Books" management page.
2.  **Select Template**: She clicks "Add Book" and chooses the "Daily Life" template, as it's a good starting point. She names the new book "Freelance Work."
3.  **API Call**: The frontend sends a `POST` request to `/api/v1/books/template`.
4.  **Backend Process**: `BookService.addByTemplate()` creates the new "Freelance Work" `Book`. It then reads the "Daily Life" template from `book_tpl.json` and programmatically creates all the default categories (e.g., "Active Income") and tags (e.g., "Food") under this new book.
5.  **Switch Active Book**: The book list now shows "Personal Finances" and "Freelance Work." Alice selects "Freelance Work" from the UI's book switcher. This triggers a `PATCH` request to `/api/v1/setDefaultBook/{id}`.
6.  **Session Update**: The backend updates Alice's `User` profile to make "Freelance Work" her new default book and also updates the `CurrentSession` bean.
7.  **Isolated Context**: When Alice now navigates to the "Categories" page, she sees only the categories associated with the "Freelance Work" book. When she adds a new expense, it is recorded only in this book, keeping her personal and business finances completely separate.

##### Journey 5: Handling Multiple Currencies

This journey addresses the needs of users who operate with more than one currency. It allows them to manage accounts in different currencies and accurately record transactions that involve currency conversion.

###### Core Interactions

1.  **Multi-Currency Accounts**: When creating a new financial `Account`, the user can select its currency from a list of world currencies (e.g., USD, EUR, CNY).
2.  **Cross-Currency Transactions**: The user records a transaction using an account with a foreign currency (relative to the Book's default currency). The system prompts for both the original amount and the converted amount.
3.  **Inter-Account Transfers**: The user initiates a transfer between two accounts with different currencies (e.g., from a USD account to a EUR account). The system requires them to specify the source amount (in USD) and the final destination amount (in EUR).
4.  **Aggregated Reporting**: When viewing high-level reports like the Net Worth overview, all balances are automatically converted to a single, consistent default currency for accurate aggregation.

###### Business Requirements

| Requirement ID | Description | Technical Implementation |
| :--- | :--- | :--- |
| FIN-CUR-01 | The system must support a comprehensive list of world currencies. | A list of currencies and their base exchange rates to USD is loaded on application startup from `currency.json` into the `ApplicationScopeBean` [^25]. |
| FIN-CUR-02 | The system should periodically update exchange rates from a reliable external source. | `CurrencyService.refreshCurrency()` makes an HTTP GET request to `api.exchangerate-api.com` to fetch the latest rates and updates the in-memory currency list [^26]. |
| FIN-CUR-03 | Each financial `Account` must be assigned a specific `currencyCode`. Each `Book` must also have a `defaultCurrencyCode`. | The `Account` and `Book` entities both contain a `currencyCode` string field to store this information [^27]. |
| FIN-CUR-04 | For transactions where the account currency does not match the book's default currency, the system must store both the original `amount` and the `convertedAmount`. | The `BalanceFlow` entity contains fields for both `amount` and `convertedAmount`. The `BalanceFlowService.add()` logic checks for currency mismatch and requires `convertedAmount` to be present if they differ [^28]. |
| FIN-CUR-05 | For cross-currency transfers, the system must debit the `amount` from the source account and credit the `convertedAmount` to the destination account. | In `BalanceFlowService.confirmBalance()`, for `FlowType.TRANSFER`, the `amount` is subtracted from the source account and `convertedAmount` is added to the destination `toAccount` [^10]. |
| FIN-CUR-06 | All summary reports must present data in a single, unified currency. | Services like `AccountService` and `ReportService` consistently use `CurrencyService.convert()` to normalize values to the group's default currency before performing calculations or presenting data [^4]. |

###### Example User Flow: Recording a Purchase in Europe with a USD Card

1.  **Setup**: Alice has a "Travel" book with a default currency of USD. She also has a "European Bank" account with a currency of EUR.
2.  **Transaction Entry**: While in Paris, she buys a souvenir for €50 using her European Bank card. She opens MoneyNote to record the expense.
    *   **Book**: "Travel" (USD)
    *   **Account**: "European Bank" (EUR)
3.  **Conversion Prompt**: The UI detects that the account currency (EUR) is different from the book's default currency (USD). Alice enters "50" in the amount field for the "Souvenirs" category. The UI prompts for the converted USD amount. Based on her bank statement, the charge was $55. She enters "55" into the "Converted Amount" field.
4.  **API Submission**: The frontend sends a `POST` to `/api/v1/balance-flows`. The `categories` array in the payload contains `{ "category": 123, "amount": 50, "convertedAmount": 55 }`.
5.  **Backend Processing**: `BalanceFlowService.add()` is executed:
    *   It creates a `BalanceFlow` record, setting its `amount` to 50 and its `convertedAmount` to 55.
    *   It calls `confirmBalance()`. This method retrieves the "European Bank" account and subtracts **50** from its balance, as the transaction amount is in the account's native currency.
6.  **Reporting**: Later, when Alice runs an expense report for her "Travel" book, the system uses the `convertedAmount` field. This transaction will appear as a **$55** expense, ensuring the report is consistently in USD.

[^1]: AccountService.java: overview() - Calculates total assets, debts, and net worth by separating accounts by type and summing their converted balances.
[^2]: AccountService.java: getAssets() - Queries for all enabled and included accounts of type `CHECKING` and `ASSET` for the current user group.
[^3]: AccountService.java: getDebts() - Queries for all enabled and included accounts of type `CREDIT` and `DEBT` for the current user group.
[^4]: AccountService.java: statistics() - Iterates through accounts and uses `currencyService.convert()` to normalize balances to the group's default currency before aggregation.
[^5]: ReportService.java: reportBalance() - Generates data for balance charts by separating asset and debt accounts and converting their balances to a common currency for comparison.
[^6]: Account.java: include - A boolean field on the Account entity that determines if the account's balance is included in summary calculations.
[^7]: BalanceFlow.java: type - An enum field `FlowType` that defines the transaction as `EXPENSE`, `INCOME`, `TRANSFER`, or `ADJUST`.
[^8]: BalanceFlow.java: book - A non-nullable `ManyToOne` relationship that links every transaction to a specific `Book`.
[^9]: BalanceFlowService.java: add() - Processes a list of `CategoryRelationForm` objects, summing their amounts to calculate the total transaction value.
[^10]: BalanceFlowService.java: confirmBalance() - Contains the core logic for applying financial changes to account balances based on the transaction's type and its `confirm` status.
[^11]: BalanceFlowService.java: refundBalance() - Reverses the financial impact of a transaction on account balances, used when a transaction is deleted or updated.
[^12]: BalanceFlowService.java: update() - Handles transaction updates by creating a new record with the updated data and removing the old one, ensuring financial integrity by calling `refundBalance` on the old record.
[^13]: BalanceFlow.java: files - A `OneToMany` mapped field to a `Set` of `FlowFile` entities, allowing multiple files per transaction.
[^14]: ValidFile.java: FileValidator.class - A custom constraint validator that checks the content type of a `MultipartFile` against a list of allowed types (PDF, PNG, JPG, JPEG).
[^15]: FlowFile.java: `data`, `originalName`, `size`, `contentType` - Entity fields that store the essential metadata and binary content of an uploaded file.
[^16]: application.properties: spring.servlet.multipart.max-file-size - Configuration property that sets the maximum size for a single uploaded file.
[^17]: FlowFileController.java: handleView() - An endpoint that serves the raw byte data of a file, using the creation timestamp as a simple security measure to make the URL less predictable.
[^18]: FlowFileService.java: remove() - Service method to delete a `FlowFile` after verifying that the requesting user has ownership of the parent `BalanceFlow`.
[^19]: Book.java: group - A `ManyToOne` relationship to the `Group` entity, structuring books within a user group.
[^20]: Category.java: book - A mandatory `ManyToOne` relationship field, ensuring every category is scoped to exactly one book. The same pattern applies to `Tag.java` and `Payee.java`.
[^21]: BookService.java: addByTemplate() - Logic to create a new `Book` and populate its initial `Categories`, `Tags`, and `Payees` from a `BookTemplate` loaded from a JSON file.
[^22]: BookService.java: addByBook() - Logic to create a new `Book` by copying the `Categories`, `Tags`, and `Payees` from an existing source `Book`.
[^23]: SessionUtil.java: getCurrentBook() - A utility method to retrieve the currently active book from the user's session scope, used throughout the service layer to filter data.
[^24]: UserService.java: setDefaultBook() - An endpoint and service method allowing a user to update their `defaultBook` preference, which is stored on the `User` entity.
[^25]: CurrencyDataLoader.java: run() - An `ApplicationRunner` that loads a list of currencies from `currency.json` into a shared `ApplicationScopeBean` on startup.
[^26]: CurrencyService.java: refreshCurrency() - Method that calls an external exchange rate API and updates the currency rates in the application-scoped bean.
[^27]: Account.java: currencyCode - A string field on the `Account` entity to specify its currency. The `Book` entity has a similar `defaultCurrencyCode` field.
[^28]: BalanceFlowService.java: checkBeforeAdd() - Validation logic that checks if an account's currency differs from the book's currency and throws an exception if `convertedAmount` is missing.

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
from helper_funcs import get_md_analyzer_and_content
import subprocess

def run_gemini_prompt(prompt: str)->bool:

    try:
        result = subprocess.run([
            'gemini',
            '-y',
            '-p',
            prompt
        ], capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing shell command: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    
    return True

code_mod_report = "customized_report_money_note_detailed_journeys.md"

analyzer, content = get_md_analyzer_and_content(code_mod_report)
headers =  analyzer.identify_headers()['Header']


# The prompt specifies creating a new section called "User Journeys"
journey_header = [header for header in headers if "User Journeys" in header['text']][0]

# Find the next headers with -1 level of heading.
in_user_journey_section = False
start_level = 0
user_journey_header_texts = []
for header in headers:
    if header['text'] == "User Journeys":
        start_level = header['level']
        in_user_journey_section = True
        continue # skip next block and jump to next header
    
    if in_user_journey_section:
        if header['level'] == (start_level+1):
            user_journey_header_texts.append(header['text'])
        elif header['level'] <= start_level:
            in_user_journey_section = False
            break # we're done, avoid duplicate User Journey Sessions



for user_journey_name in user_journey_header_texts:
    print(user_journey_name)
    prompt = f"""
    Look at the customized_report_money_note_detailed_journeys.md file, and the customized_report_money_note_data_layer.md file. 
    These files represent a report for code in moneynote-api directory. 
    As a senior business analyst Document {user_journey_name}. Document your results in an .md file with the following content:

    * Detailed user journey and flows. If there are multiple journeys include one section for each journey.
    * Detailed object level data structures. For each data structure, capture the data attributes as present in code or the database.
    * Database tables to be updated
    * API Calls that are made.
    * Business rules and functionality (include code snippets from original code to make it clearer)
    * Detailed Test cases
    * State any assumptions

    Refer back to the original code to get a better understanding. 
    Use the example_user_journey.md as an example file, follow the format and structure of that file. 
    Save the file to the current working directory {user_journey_name}.md file
    """

    run_gemini_prompt(prompt=prompt)

# Run prompt for functional specificaiton introduction
prompt = """
As a senior business analyst, craft out an introduction to a functional specification document, covering the following 3 areas. 

Purpose of the Document: Explains why this functional specification is needed.
Goals and Objectives: The high-level goals the system aims to achieve.
Scope: Defines what is included and excluded from the project.

Use the following files to guide you:

* customized_report_money_note_detailed_journeys.md
* customized_report_money_note_data_layer.md

and all user journey files in this folder.

output the results to the functional_specs_introduction.md file
"""
run_gemini_prompt(prompt=prompt)
