# Business Requirement Document: Multi-Currency Support

## 1.0 Summary
This document outlines the business requirements for the Multi-Currency Support feature within the Moneynote application. The purpose of this feature is to provide users with the capability to manage their finances across different currencies seamlessly. The system allows users to define a base currency for their financial records ("Books"), manage accounts in various international currencies, and record transactions in a currency different from their base currency. The solution involves fetching exchange rates from an external provider, caching them, and performing automatic conversions for reporting and financial consolidation. This provides a comprehensive and accurate financial overview for users dealing with multiple currencies, thereby increasing the application's utility for international users.

---

## 2.0 Project Scope
### 2.1 In-Scope
*   **Base Currency Configuration:** Users can define a default currency for each financial "Book".
*   **Multi-Currency Accounts:** Users can create and manage financial "Accounts" in different currencies supported by the system.
*   **Foreign Currency Transactions:** Users can record transactions (incomes, expenses) in an account's specific currency, which may differ from the book's base currency.
*   **Automatic Exchange Rate Conversion:** The system will automatically calculate and store the converted value of a transaction in the book's base currency, using the most recently cached exchange rate.
*   **Exchange Rate Management:** The system will load an initial list of currencies and rates from a local file and periodically refresh these rates from an external API.
*   **Viewing Currencies:** Users can view the list of all supported currencies and their current exchange rates.

### 2.2 Out-of-Scope
*   Real-time, tick-by-tick exchange rate updates. Daily updates are sufficient.
*   Support for cryptocurrencies or other non-fiat currencies.
*   Historical exchange rate tracking for "what-if" analysis or re-calculation of past transactions. The conversion is based on the rate available at the time of transaction entry.
*   Persistence of manually updated exchange rates. Manual overrides are for the current session only.

---

## 3.0 Business Requirements

**BR-001:** The system must allow a user to define a single, default currency for each financial "Book" upon its creation. This currency will serve as the base for all consolidated reporting within that book. This is implemented in the `Book` entity (`t_user_book` table) via the `defaultCurrencyCode` field.

**BR-002:** The system must support the creation of financial "Accounts" in any of the currencies pre-defined in `currency.json`. The currency assigned to an account is immutable. This is implemented in the `Account` entity (`t_user_account` table) via the `currencyCode` field.

**BR-003:** When a transaction is recorded in an account where the currency differs from the "Book's" default currency, the system must automatically apply the latest cached exchange rate to calculate and store the equivalent value in the book's default currency. This is implemented in the `BalanceFlow` entity (`t_user_balance_flow` table) with the `amount` and `convertedAmount` fields.

**BR-004:** The system must maintain an in-memory list of supported currencies and their exchange rates against a primary base currency (USD), ensuring all currency-related operations can be performed with a 99.9% success rate. This is achieved by loading data from `currency.json` into the `ApplicationScopeBean` on startup, as handled by `CurrencyDataLoader.java`.

### 3.1 Functional Requirements

**FR-001:** Upon application startup, the system shall load the list of supported currencies and their base exchange rates from the `currency.json` file into the application's in-memory cache (`ApplicationScopeBean`) within 500ms. Success is measured by the full and accurate population of currency data available to the `CurrencyService`.

**FR-002:** The system must refresh its in-memory exchange rates from the external API (`https://api.exchangerate-api.com`) at least once every 24 hours, or upon a manual trigger by the user via the `POST /currencies/refresh` endpoint. Success is measured by the `rate` property being updated in the in-memory `CurrencyDetails` objects. This is implemented by the `CurrencyRemoteDataLoader.java`.

**FR-003:** The user must be able to create a new financial account and assign it any currency supported by the system via the `AccountAddForm`. The system must validate that the provided currency code exists in the in-memory list using `CurrencyService.checkCode()`. Success is measured by the successful creation of an account with a valid currency code and the rejection of an account with an invalid one, with a 100% accuracy rate.

**FR-004:** When a user requests a financial report, all transaction amounts must be presented in the "Book's" default currency. The system must use the pre-calculated `convertedAmount` from the `BalanceFlow` entity for all aggregation and display purposes, ensuring report generation is completed within 2 seconds. This is handled by the `ReportService`.

**FR-005:** The system must provide an endpoint (`GET /currencies/calc`) that allows a client to calculate the equivalent value between any two currencies based on the currently cached exchange rates. The calculation must complete successfully within 200ms for 99% of requests.

---
## 4.0 Assumptions, Constraints, and Dependencies
### 4.1 Assumptions
*   The external exchange rate API is assumed to be reliable, available, and will continue to provide data in the expected JSON format with USD as the base currency.
*   Having currency exchange rates stored only in-memory is an acceptable design, and temporary manual rate changes that are lost on restart meet user requirements.
*   Daily exchange rate updates are sufficient for the user's financial tracking and reporting needs.
*   The `currency.json` file is considered the source of truth for the initial set of supported currencies and is assumed to be present and correctly formatted at application startup.

### 4.2 Dependencies
*   **External API:** The entire multi-currency functionality is critically dependent on the availability and accuracy of the external exchange rate provider (`api.exchangerate-api.com`). Any downtime or change in this external service will directly impact the system's ability to provide current exchange rates.
