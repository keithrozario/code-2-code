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
