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

