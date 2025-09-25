# Journey 5: Supporting Multiple Currencies

This document outlines the user journeys, data structures, and business logic related to the multi-currency support feature in the Moneynote API.

## 1. Detailed User Journeys and Flows

### Journey 5.1: Viewing Available Currencies and Exchange Rates

**Objective:** To allow a user to see the list of supported currencies and their current exchange rates relative to a specific base currency.

**Flow:**
1.  **Start:** The user navigates to the currency management section of the application.
2.  **User Action:** The user requests the list of currencies. They can optionally specify a base currency (e.g., "EUR") to see all rates relative to it.
3.  **System Response:** The system calls the `GET /currencies` endpoint.
4.  **Backend Logic:**
    *   The `CurrencyService` retrieves the list of `CurrencyDetails` objects held in memory.
    *   If a `base` currency is provided in the query, the service calculates the exchange rate of every currency relative to the specified base currency. The base for all stored rates is USD, so the calculation is `(target_rate_to_usd) / (base_rate_to_usd)`.
    *   The service returns a paginated list of currencies with their names, descriptions, and calculated rates.
5.  **System Response:** The UI displays the list of currencies and their exchange rates.
6.  **End:** The user has viewed the currency exchange rates.

---

### Journey 5.2: Recording a Transaction in a Foreign Currency

**Objective:** To allow a user to record a transaction (expense, income) in an account whose currency is different from the book's default currency.

**Flow:**
1.  **Start:** The user initiates the creation of a new transaction (e.g., an expense).
2.  **User Action:** The user selects an account for the transaction. Let's assume the book's default currency is `CNY` and the user selects a credit card account with `USD` currency.
3.  **User Action:** The user enters the transaction amount, for example, `100 USD`.
4.  **System Response (Frontend):** The UI detects that the account currency (`USD`) is different from the book's base currency (`CNY`). It makes a call to the backend (`GET /currencies/calc?from=USD&to=CNY&amount=100`) to get the calculated converted amount.
5.  **System Response (Frontend):** The UI displays the original amount (`100 USD`) and the automatically converted amount (e.g., `~710 CNY`) to the user. The user might be given the option to override the converted amount.
6.  **User Action:** The user confirms and saves the transaction.
7.  **System Response:** The system calls the `POST /balance-flows` endpoint, sending a `BalanceFlowAddForm` payload. This payload includes the original `amount` (100) and the `convertedAmount` (710). The `account` field specifies the ID of the USD account.
8.  **Backend Logic:**
    *   The `BalanceFlowService` creates a new `BalanceFlow` entity.
    *   It saves both the original `amount` (100) and the `convertedAmount` (710).
    *   The transaction is now stored. All reporting and budget calculations within the book will use the `convertedAmount`.
9.  **End:** The foreign currency transaction is successfully recorded and converted to the book's base currency.

---

### Journey 5.3: Manually Updating an Exchange Rate

**Objective:** To allow a user to override the system's exchange rate for a specific currency.

**Flow:**
1.  **Start:** The user navigates to the currency list.
2.  **User Action:** The user decides the rate for a currency (e.g., `EUR`) is incorrect and wants to change it. They select the option to edit the rate.
3.  **User Action:** The user provides the new rate. For example, they set `1 EUR = 1.15 USD`.
4.  **System Response:** The UI calls the `PUT /currencies/{id}/rate` endpoint (where `{id}` is the ID of the EUR currency). The payload (`ChangeRateForm`) contains the base currency (`"base": "USD"`) and the new rate (`"rate": 1.15`).
5.  **Backend Logic:**
    *   The `CurrencyService` receives the request.
    *   It finds the `CurrencyDetails` object for EUR in the in-memory list.
    *   It calculates the new rate relative to the system's base (USD). In this case, the form provides the rate against USD directly. The service updates the `rate` property of the EUR `CurrencyDetails` object to `1.15`.
    *   This change is **not persistent** and will be lost on application restart or when the automatic refresh runs.
6.  **End:** The exchange rate is updated for the current application session.

---

### Journey 5.4: System-Driven Exchange Rate Refresh

**Objective:** To keep exchange rates up-to-date automatically.

**Flow:**
1.  **Start (Trigger):** The application starts up, or a user triggers a manual refresh via `POST /currencies/refresh`.
2.  **System Action:** The `CurrencyRemoteDataLoader` (on startup) or `CurrencyController` (on manual request) calls `currencyService.refreshCurrency()`.
3.  **Backend Logic:**
    *   The `CurrencyService` makes an HTTP GET request to an external API (`https://api.exchangerate-api.com/v4/latest/USD`).
    *   It parses the response, which contains a map of currency codes to their rates against USD.
    *   It iterates through the currencies it manages in memory. For each currency, if it exists in the response from the external API, its `rate` property is updated.
4.  **Error Handling:** If the external API call fails, the existing rates are preserved. The method returns `false`.
5.  **End:** The in-memory exchange rates are updated with the latest values from the external provider.

## 2. Detailed Object Level Data Structures

### `CurrencyDetails` (In-Memory Object)
This object is not a JPA entity and is not stored in the database. It is loaded from `currency.json` and held in an application-scoped bean.

| Attribute Name | Data Type | Constraints/Properties | Description |
| :--- | :--- | :--- | :--- |
| `id` | `Integer` | | Unique identifier from the JSON file. |
| `name` | `String` | | The 3-letter currency code (e.g., "USD", "EUR"). |
| `description` | `String` | | A human-readable description of the currency. |
| `rate` | `Double` | | The exchange rate of this currency against the base currency (USD). |
| `rate2` | `Double` | (transient) | Used to hold a calculated rate against a user-specified base currency for display purposes. |

### `Book` (JPA Entity)
This entity represents a user's ledger or book.

| Attribute Name | Data Type | Constraints/Properties | Description |
| :--- | :--- | :--- | :--- |
| `defaultCurrencyCode` | `string` | `NOT NULL`, `length=8` | The base currency for this book. All financial reports for this book are in this currency. |

### `Account` (JPA Entity)
This entity represents a financial account (e.g., bank account, credit card).

| Attribute Name | Data Type | Constraints/Properties | Description |
| :--- | :--- | :--- | :--- |
| `currencyCode` | `string` | `NOT NULL`, `length=8` | The currency of this account. |

### `BalanceFlow` (JPA Entity)
This entity represents a single transaction or flow of money.

| Attribute Name | Data Type | Constraints/Properties | Description |
| :--- | :--- | :--- | :--- |
| `amount` | `BigDecimal` | `NOT NULL` | The original amount of the transaction in the account's currency. |
| `convertedAmount` | `BigDecimal` | | The transaction amount converted to the book's `defaultCurrencyCode`. Used for reporting. |

## 3. Database Tables to be Updated

The currency management system is primarily in-memory and does not have its own dedicated database table. However, it impacts the following tables:

*   **`t_user_book`**:
    *   **Read**: The `defaultCurrencyCode` is read when performing currency conversions for transactions within that book.
    *   **Write**: The `defaultCurrencyCode` is set when a new book is created.
*   **`t_user_account`**:
    *   **Read**: The `currencyCode` is read to determine the currency of a transaction.
    *   **Write**: The `currencyCode` is set when a new account is created.
*   **`t_user_balance_flow`**:
    *   **Write**: When a transaction is created, the `amount` and `convertedAmount` are written. The `convertedAmount` is calculated based on the exchange rates managed by the `CurrencyService`.

## 4. Business Rules and Functionality (Detailed)

| Rule Name/Identifier | Description | Triggering Event | Logic/Conditions | Outcome/Action |
| :--- | :--- | :--- | :--- | :--- |
| **Currency Code Validation** | Ensures that any provided currency code is one of the supported currencies. | Any operation involving a currency code (e.g., creating an account, setting book currency). | `CurrencyService.checkCode(code)` is called. It checks if the code exists in the in-memory list of currencies. | If the code is not found, a `FailureMessageException` is thrown. |
| **Transaction Conversion** | Automatically converts a transaction amount to the book's base currency if the transaction's account has a different currency. | A `BalanceFlow` (transaction) is created or updated. | `if (!account.currencyCode.equals(book.defaultCurrencyCode))` | The `convertedAmount` field on the `BalanceFlow` is calculated and stored using `CurrencyService.convert(amount, account.currencyCode, book.defaultCurrencyCode)`. |
| **Rate Calculation** | Calculates the exchange rate between any two currencies. | `GET /currencies/rate`, `GET /currencies/calc`, or internal `convert` calls. | The calculation uses USD as the pivot currency: `Rate(A->B) = Rate(USD->B) / Rate(USD->A)`. | Returns the calculated `BigDecimal` rate. |
| **Rate Refresh** | Updates all currency rates from an external provider. | Application startup or `POST /currencies/refresh`. | An HTTP GET request is made to `api.exchangerate-api.com`. | The in-memory `rate` for each currency is updated. The changes are not saved to the `currency.json` file. |

## 5. Detailed Test Cases

| Test Case ID | Feature Being Tested | Preconditions | Test Steps | Test Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-CUR-01 | View Currencies (Happy Path) | System is running. | 1. Make a GET request to `/currencies`. | `base=CNY` | A 200 OK response with a JSON list of currencies. Each currency should have a `rate2` field showing its value against CNY. |
| TC-CUR-02 | Calculate Conversion (Happy Path) | System is running. Rates are loaded. | 1. Make a GET request to `/currencies/calc`. | `from=USD`, `to=JPY`, `amount=10` | A 200 OK response with the calculated amount in JPY (e.g., `1349.5`). |
| TC-CUR-03 | Create Foreign Currency Transaction | A book exists with `defaultCurrencyCode` = `CNY`. An account exists with `currencyCode` = `USD`. | 1. POST to `/balance-flows`. | `amount`: 100, `account`: (ID of USD account), `book`: (ID of CNY book). | The `BalanceFlow` is created. The `amount` field is 100. The `convertedAmount` field is correctly calculated to the CNY equivalent (e.g., ~710). |
| TC-CUR-04 | Manual Rate Update | System is running. A currency with ID 47 (EUR) exists. | 1. PUT to `/currencies/47/rate`. | `{"base": "USD", "rate": 1.20}` | 200 OK. A subsequent GET to `/currencies/rate?from=EUR&to=USD` should return `1.20`. |
| TC-CUR-05 | Invalid Currency Code | System is running. | 1. Create an account with an invalid currency code. | `currencyCode`: "XYZ" | The API should return a validation error (e.g., 400 Bad Request) with a message like "valid.fail". |
| TC-CUR-06 | Rate Refresh Failure | External API `api.exchangerate-api.com` is unreachable. | 1. POST to `/currencies/refresh`. | - | The call should fail gracefully (return `false` internally). The existing currency rates in memory should remain unchanged. |

## 6. State Any Assumptions

*   **External API Dependency:** The system assumes the external exchange rate API at `https://api.exchangerate-api.com/v4/latest/USD` is available, reliable, and will continue to provide data in the expected JSON format with USD as the base.
*   **In-Memory State:** It is assumed that having currency rates stored only in-memory is an acceptable design choice. This means that any manual rate changes are temporary and will be overwritten by the automatic refresh or lost on restart.
*   **`currency.json` as Source of Truth:** The initial list of supported currencies is defined entirely by `currency.json`. The system assumes this file is present, correctly formatted, and contains all currencies the application is intended to support.
*   **USD as Base Rate:** The application logic is built around the assumption that all rates loaded from `currency.json` and the external API are relative to USD. This is crucial for the `convert` function to work correctly.
