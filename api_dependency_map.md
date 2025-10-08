# API Dependency Map
--------------------------------------------------
### Dependencies for: `EndpointPath`

**Upstream Dependencies (Calls made BY this API):**
The following outgoing HTTP client request was found:

File: `/Users/himakunisetty/Documents/Gemini Code Assist/AiDM/trial_4/moneynote-api/src/main/java/cn/biq/mn/currency/CurrencyService.java`
Line: 108
Request: `webUtils.get("https://api.exchangerate-api.com/v4/latest/USD")`
Destination URL: `https://api.exchangerate-api.com/v4/latest/USD`

**Downstream Consumers (Potential callers OF this API):**
I couldn't find any files containing the string "EndpointPath". However, I did find that the application uses the `@RequestMapping` annotation to define endpoint paths.

Here are the files that use `@RequestMapping` and are potential callers:

*   `src/main/java/cn/biq/mn/group/GroupController.java`
*   `src/main/java/cn/biq/mn/category/CategoryController.java`
*   `src/main/java/cn/biq/mn/tag/TagController.java`
*   `src/main/java/cn/biq/mn/payee/PayeeController.java`
*   `src/main/java/cn/biq/mn/account/AccountController.java`
*   `src/main/java/cn/biq/mn/currency/CurrencyController.java`
*   `src/main/java/cn/biq/mn/TestController.java`
*   `src/main/java/cn/biq/mn/report/ReportController.java`
*   `src/main/java/cn/biq/mn/user/UserController.java`
*   `src/main/java/cn/biq/mn/book/BookController.java`
*   `src/main/java/cn/biq/mn/book/tpl/BookTemplateController.java`
*   `src/main/java/cn/biq/mn/flowfile/FlowFileController.java`
*   `src/main/java/cn/biq/mn/noteday/NoteDayController.java`
*   `src/main/java/cn/biq/mn/balanceflow/BalanceFlowController.java`
*   `src/main/java/cn/biq/mn/tagrelation/TagRelationController.java`

