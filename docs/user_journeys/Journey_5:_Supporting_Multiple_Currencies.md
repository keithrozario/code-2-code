# User Journey Analysis: Journey 5: Supporting Multiple Currencies

### 1.0 Detailed User Journeys and Flows
This journey describes how a user who deals with more than one currency manages their accounts and transactions.

**User Flow 1: Setting up a Foreign Currency Account**
1.  **Start:** The user decides to add a new bank account that is denominated in a foreign currency (e.g., a EUR account while their primary currency is USD).
2.  The user navigates to the "Accounts" section and clicks "Add Account".
3.  In the account creation form, the user enters the account name (e.g., "My European Bank").
4.  The user selects the currency for the account from a dropdown list of available world currencies (e.g., "EUR").
5.  The user saves the account.
6.  **End:** The new account now appears in their list of accounts, clearly marked with its currency.

**User Flow 2: Recording an Expense in a Foreign Currency**
1.  **Start:** The user makes a purchase in a foreign currency (e.g., buys a coffee for €3.50 in Berlin) using their foreign currency account.
2.  The user opens the MoneyNote app to record the expense.
3.  They create a new "Expense" transaction.
4.  They select their "My European Bank" (EUR) account.
5.  They enter the amount: `3.50`.
6.  **System Response:** The system detects that the account's currency (EUR) is different from the book's default currency (USD).
7.  The UI displays an additional field, "Converted Amount (USD)", and may suggest a value based on the current exchange rate (e.g., "$3.78").
8.  The user can accept the suggested conversion or manually enter the precise amount from their bank statement.
9.  The user fills in the rest of the transaction details (category, payee) and saves.
10. **End:** The transaction is recorded. The balance of the EUR account is reduced by €3.50, and for reporting purposes, the expense is logged as $3.78.

**User Flow 3: Transferring Funds Between Different Currency Accounts**
1.  **Start:** The user wants to transfer money from their primary USD account to their EUR account.
2.  The user creates a new "Transfer" transaction.
3.  For the "From" account, they select their "US Checking" (USD).
4.  For the "To" account, they select their "My European Bank" (EUR).
5.  They enter the amount to send: `100` (USD).
6.  **System Response:** The system requires the user to enter the final amount received in the destination currency.
7.  The user enters the received amount: `92.50` (EUR), based on the bank's transfer record.
8.  The user saves the transfer.
9.  **End:** The balance of the "US Checking" account is reduced by $100, and the balance of the "My European Bank" account is increased by €92.50.

**Error Handling:**
*   If a user tries to save a transaction with an invalid or unsupported currency code, the system will reject it with a validation error.
*   If the external exchange rate API is unavailable, the system will fall back to the rates stored locally in `currency.json`.

---

### 2.0 Detailed Object Level Data Structures

**`Account` Entity (`t_user_account` table)**
Represents a financial account.
| Attribute | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key | Unique identifier for the account. |
| `currencyCode` | `VARCHAR(8)` | `NOT NULL` | The ISO currency code for the account (e.g., "USD", "EUR"). |
| `balance` | `DECIMAL(20,2)` | `NOT NULL` | The current balance in the account's specified currency. |

**`Book` Entity (`t_user_book` table)**
Represents a ledger for recording transactions.
| Attribute | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key | Unique identifier for the book. |
| `defaultCurrencyCode` | `VARCHAR(8)` | `NOT NULL` | The default currency for the book, used for all reporting. |

**`BalanceFlow` Entity (`t_user_balance_flow` table)**
The central transaction entity.
| Attribute | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key | Unique identifier for the transaction. |
| `amount` | `DECIMAL(15,2)` | `NOT NULL` | The transaction amount in the original currency of the transaction/account. |
| `convertedAmount` | `DECIMAL(15,2)` | `Nullable` | The transaction amount converted to the book's default currency. Required if the transaction currency differs from the book's default. |

**`CurrencyDetails` (In-Memory Object)**
Represents a currency and its exchange rate, loaded from `currency.json` and an external API.
| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Unique identifier from the JSON file. |
| `name` | `String` | The ISO currency code (e.g., "USD"). |
| `description` | `String` | The full name of the currency. |
| `rate` | `Double` | The exchange rate relative to a base currency (USD). |

---

### 3.0 Database Tables to be Updated

This user journey primarily involves reading currency information and ensuring transaction data is correctly stored.

**Tables Read From:**
*   `t_user_account`: To get the `currencyCode` of an account involved in a transaction.
*   `t_user_book`: To get the `defaultCurrencyCode` to determine if a conversion is needed.

**Tables Written To (`INSERT`, `UPDATE`):**
*   **`t_user_balance_flow`**:
    *   `INSERT`: A new transaction record is created.
    *   The `amount` field is populated with the value in the transaction's original currency.
    *   The `convertedAmount` field is populated if the transaction's currency is different from the book's default currency.
*   **`t_user_account`**:
    *   `UPDATE`: The `balance` of the associated account(s) is updated when a transaction is confirmed. The update is always in the currency of the account itself.

---

### 4.0 Business Rules and Functionality (Detailed)

| Rule Name | Description | Trigger | Logic | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **Currency Data Loading** | The system must have a list of available world currencies and their exchange rates. | Application Startup | The `CurrencyDataLoader` reads `currency.json` to populate an in-memory list of currencies. The `CurrencyRemoteDataLoader` then calls an external API (`exchangerate-api.com`) to refresh these rates. | The `ApplicationScopeBean` holds a list of `CurrencyDetails` objects available for all sessions. |
| **Account Currency Assignment** | Every financial account must be assigned a specific currency. | Creating or Editing an `Account`. | The `Account` entity has a mandatory `currencyCode` field. The value must be a valid code from the system's currency list. | An account is permanently associated with a currency (e.g., "USD", "JPY"). |
| **Book Default Currency** | Every "book" must have a default currency for reporting. | Creating or Editing a `Book`. | The `Book` entity has a mandatory `defaultCurrencyCode` field. | All aggregated reports within that book will be presented in this currency. |
| **Cross-Currency Detection** | The system must detect when a transaction involves a currency mismatch. | Creating a new `BalanceFlow` (transaction). | The `BalanceFlowService` compares the `currencyCode` of the transaction's `Account` with the `defaultCurrencyCode` of the `Book`. | If the codes are different, the system requires the `convertedAmount` to be provided. |
| **Transfer Currency Handling** | For transfers between accounts with different currencies, both source and destination amounts must be captured. | Creating a `TRANSFER` type `BalanceFlow`. | The `BalanceFlowService.add()` logic requires both `amount` (source currency value) and `convertedAmount` (destination currency value) for cross-currency transfers. The `confirmBalance()` method then updates the two accounts accordingly. | The source account is debited by `amount`, and the destination account is credited by `convertedAmount`. |
| **Reporting Aggregation** | All financial reports must present data in a single, consistent currency. | Generating a report (e.g., `ReportService.reportCategory`). | The service uses the `convertedAmount` from `BalanceFlow` records for its calculations. If `convertedAmount` is null (meaning the transaction was in the default currency), it uses the `amount`. | Reports provide an accurate financial summary by comparing like-for-like currency values. |
| **On-the-Fly Conversion** | The system must provide a utility to calculate currency conversions. | API call to `/currencies/calc`. | The `CurrencyService.calc()` method uses the stored exchange rates to convert a given amount from a source currency to a target currency. | The API returns the calculated converted amount. |

---

### 5.0 Test Cases

| ID | Feature | Preconditions | Steps | Test Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-CUR-01 | Create Foreign Currency Account | User is logged in. A list of currencies exists. | 1. Navigate to "Accounts". 2. Click "Add Account". 3. Fill in the name. 4. Select a currency from the dropdown. 5. Save. | Name: "Euro Savings", Currency: "EUR" | The account is created successfully and displayed with the "EUR" currency code. |
| TC-CUR-02 | Record Expense in Foreign Currency | Book default is USD. An account "Euro Savings" exists with currency EUR. | 1. Create a new expense. 2. Select "Euro Savings" account. 3. Enter amount. 4. Enter converted amount. 5. Save. | Amount: 100 (EUR), Converted Amount: 108.00 (USD) | Transaction is saved. "Euro Savings" balance decreases by 100. Expense report shows an expense of $108.00. |
| TC-CUR-03 | Record Income in Foreign Currency | Book default is USD. An account "Euro Savings" exists with currency EUR. | 1. Create a new income. 2. Select "Euro Savings" account. 3. Enter amount. 4. Enter converted amount. 5. Save. | Amount: 200 (EUR), Converted Amount: 216.00 (USD) | Transaction is saved. "Euro Savings" balance increases by 200. Income report shows an income of $216.00. |
| TC-CUR-04 | Cross-Currency Transfer | Book default is USD. "US Checking" (USD) and "Euro Savings" (EUR) accounts exist. | 1. Create a new transfer. 2. From: "US Checking". 3. To: "Euro Savings". 4. Amount: 100 (USD). 5. Converted Amount: 92.00 (EUR). 6. Save. | Amount: 100, Converted Amount: 92 | "US Checking" balance decreases by $100. "Euro Savings" balance increases by €92. |
| TC-CUR-05 | Reporting Accuracy | Multiple transactions exist in different currencies (EUR, JPY), all with correct `convertedAmount` in USD. | 1. Navigate to "Reports". 2. Generate an "Expense by Category" report for the month. | - €50 expense (converted to $54).<br>- ¥1000 expense (converted to $7.40).<br>- $20 expense. | The report correctly sums the `convertedAmount` values. The total expense should be $81.40 (54 + 7.40 + 20). |
| TC-CUR-06 | Invalid Currency Code | User attempts to create an account with a non-existent currency code. | 1. Attempt to create an account via API. | `currencyCode`: "XYZ" | The API returns a validation error (`valid.fail`). The account is not created. |
| TC-CUR-07 | Same-Currency Transaction | Book default is USD. An expense is recorded from a USD account. | 1. Create a new expense from a USD account. 2. Enter amount. 3. Save. | Amount: 50 (USD) | The transaction is saved. The `convertedAmount` field in the database is `null`. The report uses the `amount` field for its calculation. |

---

### 6.0 Assumptions

*   **Base Currency is USD:** The system assumes that USD is the base currency against which all other exchange rates are calculated. The external API call in `CurrencyService.refreshCurrency()` is hardcoded to fetch rates against USD.
*   **User Provides Conversion for Transactions:** The system relies on the user to input the `convertedAmount` for expenses, incomes, and transfers. While it can suggest a rate, it does not enforce a calculated rate, allowing the user to enter the exact amount from a bank or credit card statement.
*   **Static Fallback Rates:** It is assumed that if the external exchange rate API fails, the rates loaded from the local `currency.json` file are acceptable for use, even if they are stale.
*   **Group-Level Default Currency:** While books have a default currency, the highest-level reporting (like the `AccountService.overview()`) aggregates to the `Group`'s default currency. It's assumed that the book's currency is primarily for display and that the group's currency is the ultimate source of truth for consolidation.
