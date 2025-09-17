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
