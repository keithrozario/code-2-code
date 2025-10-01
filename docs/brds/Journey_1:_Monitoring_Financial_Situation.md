# Business Requirement Document: Financial Situation Monitoring

## 1.0 Summary
This document outlines the business requirements for the "Financial Situation Monitoring" feature of the MoneyNote application. The primary objective is to provide users with a clear, accurate, and immediate overview of their financial health. The feature allows users to view key metrics such as net worth, total assets, and total liabilities, and to visualize the composition of their assets and debts through interactive charts. This functionality is read-only and is designed to aggregate existing financial data into an easily digestible format for the user.

---

## 2.0 Project Scope
### 2.1 In-Scope
*   **Financial Overview Calculation:** The system will calculate and display three key metrics: Total Assets, Total Liabilities, and Net Worth.
*   **Currency Conversion:** All financial calculations will be converted to the user's default currency for a consolidated view.
*   **Asset and Debt Visualization:** The system will generate and display two separate charts that break down the composition of the user's assets and debts by account.
*   **Interactive Drill-Down:** Users will be able to click on a segment of a chart to navigate to a pre-filtered list of transactions for the corresponding account.

### 2.2 Out-of-Scope
*   Creation or modification of accounts or transactions.
*   Income vs. Expense reporting (covered in a separate user journey).
*   Financial forecasting or predictive analysis.
*   Budget creation and tracking.
*   Investment performance analysis.

---

## 3.0 Business Requirements

**BR-001: Consolidated Financial Overview**
The system must provide a consolidated overview of the user's financial position by calculating and displaying their total assets, total liabilities, and net worth. This calculation must be performed in real-time upon user request, ensuring all active and included accounts are aggregated and converted to the user's default currency. This is critical for providing users with an accurate, up-to-date snapshot of their financial health. This requirement is implemented in the `AccountService.overview()` method.

### 3.1 Functional Requirements

**FR-001: Financial Metrics Display**
The user dashboard must display the user's Total Assets, Total Liabilities, and Net Worth within 2 seconds of loading. Success is measured by the displayed values accurately reflecting the sum of balances from all `Account` entities marked as `include=true` and `enable=true`, with balances converted to the user's default currency, as validated by test case `TC-MON-01`. This functionality is provided by the `/api/v1/accounts/overview` endpoint.

**FR-002: Asset and Debt Composition Visualization**
The system shall display two separate charts on the dashboard to visualize the composition of assets and debts. Each chart segment will represent a financial account, and its size will be proportional to its percentage of the total. The charts must be generated within 2 seconds of the dashboard loading. Success is measured by the charts accurately reflecting the proportional value of each account, as detailed in test case `TC-MON-05`. This is implemented by the `ReportService.reportBalance()` method, available at `/api/v1/reports/balance`.

**FR-003: Interactive Chart Drill-Down**
Users must be able to click on a specific segment of either the asset or debt chart and be immediately navigated to the transaction list page. This page must be automatically filtered to display only the transactions associated with the selected account. The navigation and application of the filter must be completed within 1.5 seconds.

---
## 4.0 Assumptions, Constraints, and Dependencies
### 4.1 Assumptions
*   **Correct Account Classification:** The accuracy of the financial overview is dependent on the user having correctly classified their accounts (e.g., as `ASSET`, `DEBT`, `CHECKING`, or `CREDIT`).
*   **Currency Rate Availability:** It is assumed that the system has access to valid exchange rates via the `CurrencyService` to perform all necessary currency conversions to the user's default currency.
*   **User Context:** All calculations are performed within the context of the user's currently active `Group`, and the system correctly identifies this group from the user's session.

### 4.2 Constraints
*   **Transactional Database Reporting:** All reporting queries are executed directly against the primary transactional (OLTP) database. As noted in the CodMod report, this can lead to performance degradation under heavy load.
*   **In-Memory Caching:** The system relies on a local, in-memory cache for currency exchange rates, which is not suitable for a horizontally scaled, distributed deployment environment.

### 4.3 Dependencies
*   **Data Integrity:** The accuracy of all financial reports is wholly dependent on the user diligently and accurately recording all their transactions and maintaining correct balances within the `BalanceFlow` and `Account` entities.
