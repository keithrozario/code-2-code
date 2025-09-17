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

