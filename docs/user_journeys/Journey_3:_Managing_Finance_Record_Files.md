
# Journey 3: Managing Finance Record Files

This document outlines the user journeys, data structures, business rules, and test cases related to managing finance record files within the moneynote-api system.

## 1. Detailed User Journeys and Flows

### Objective
To capture the step-by-step interactions a user has with the system to manage files associated with financial records.

---

### Journey 3.1: Uploading a Financial Record File

*   **Objective:** To attach a supporting file (e.g., a receipt, invoice) to a specific financial transaction (BalanceFlow).
*   **Start Point:** The user is viewing the details of a financial transaction.
*   **End Point:** The file is successfully uploaded and associated with the transaction.

**Flow:**

1.  **User Action:** From the transaction details screen, the user clicks the "Add File" or "Upload Attachment" button.
2.  **System Response:** The system displays a file selection dialog.
3.  **User Action:** The user selects a file from their local device and confirms the selection.
4.  **System Action:** The client-side application initiates a `POST` request to the `/balance-flows/{id}/addFile` endpoint, where `{id}` is the ID of the `BalanceFlow` transaction. The request includes the file as a multipart form data.
5.  **System Response (Backend):**
    *   The `BalanceFlowController` receives the request.
    *   The `balanceFlowService.addFile` method is called.
    *   A new `FlowFile` entity is created.
    *   The file's data, content type, size, and original name are stored in the `FlowFile` entity.
    *   The `FlowFile` is associated with the corresponding `BalanceFlow` entity.
    *   The new `FlowFile` entity is persisted to the `t_flow_file` table.
6.  **System Response (Frontend):** The UI is updated to show the newly uploaded file in the list of attachments for the transaction.

**Error Handling:**

*   If the file is empty or exceeds the maximum allowed size, the system will reject the upload and display an error message.
*   If the transaction (`BalanceFlow`) does not exist or the user does not have permission to modify it, the system will return an error.

---

### Journey 3.2: Viewing a Financial Record File

*   **Objective:** To view the content of a file attached to a financial transaction.
*   **Start Point:** The user is viewing the list of files attached to a transaction.
*   **End Point:** The content of the selected file is displayed to the user.

**Flow:**

1.  **User Action:** The user clicks on the name or icon of a file they wish to view.
2.  **System Action:** The client-side application initiates a `GET` request to the `/flow-files/view` endpoint, passing the `id` and `createTime` of the `FlowFile` as query parameters.
3.  **System Response (Backend):**
    *   The `FlowFileController` receives the request.
    *   The `flowFileService.getFile` method is called.
    *   The system verifies that the `createTime` matches the one stored in the database for the given `id`.
    *   The file's binary data and content type are retrieved from the `t_flow_file` table.
    *   The system returns the file's content in the HTTP response with the appropriate `Content-Type` header.
4.  **System Response (Frontend):** The browser renders the file content (e.g., displays an image, shows a PDF) or prompts the user to download it.

**Error Handling:**

*   If the `id` or `createTime` is invalid or mismatched, the system returns an error, preventing unauthorized access.
*   If the file record does not exist, the system returns a "Not Found" error.

---

### Journey 3.3: Deleting a Financial Record File

*   **Objective:** To remove a file that is no longer needed from a financial transaction.
*   **Start Point:** The user is viewing the list of files attached to a transaction.
*   **End Point:** The file is permanently deleted from the system.

**Flow:**

1.  **User Action:** The user clicks the "Delete" or "Remove" icon next to the file they want to delete.
2.  **System Response:** The system may ask for confirmation (e.g., "Are you sure you want to delete this file?").
3.  **User Action:** The user confirms the deletion.
4.  **System Action:** The client-side application initiates a `DELETE` request to the `/flow-files/{id}` endpoint, where `{id}` is the ID of the `FlowFile`.
5.  **System Response (Backend):**
    *   The `FlowFileController` receives the request.
    *   The `flowFileService.remove` method is called.
    *   The system verifies that the user has permission to delete the file (by checking ownership of the associated `BalanceFlow`).
    *   The `FlowFile` record is deleted from the `t_flow_file` table.
6.  **System Response (Frontend):** The UI is updated to remove the file from the list of attachments.

**Error Handling:**

*   If the user does not have permission to delete the file, the system returns an authorization error.
*   If the file record does not exist, the system returns a "Not Found" error.

## 2. Detailed Object Level Data Structures

### `FlowFile` Entity

This entity represents a file attached to a `BalanceFlow` transaction.

| Attribute | Data Type | Constraints/Properties | Description |
|---|---|---|---|
| `id` | `Integer` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique identifier for the file record. |
| `data` | `byte[]` | `NOT NULL`, `LONGBLOB` | The binary content of the file. |
| `creator` | `User` | `NOT NULL`, `FOREIGN KEY` (to `t_user`) | The user who uploaded the file. |
| `flow` | `BalanceFlow` | `FOREIGN KEY` (to `t_balance_flow`) | The financial transaction this file is associated with. |
| `createTime` | `Long` | `NOT NULL` | The timestamp (in milliseconds) when the file was uploaded. |
| `contentType` | `String` | `NOT NULL`, `maxLength=32` | The MIME type of the file (e.g., "image/png"). |
| `size` | `Long` | `NOT NULL` | The size of the file in bytes. |
| `originalName` | `String` | `NOT NULL`, `maxLength=512` | The original name of the file as uploaded by the user. |

## 3. Database Tables to be Updated

### `t_flow_file`

*   **Read from:**
    *   When a user views a file (`/flow-files/view`).
    *   When a user lists the files for a transaction (`/balance-flows/{id}/files`).
*   **Written to:**
    *   `INSERT`: When a new file is uploaded (`/balance-flows/{id}/addFile`).
    *   `DELETE`: When a file is deleted (`/flow-files/{id}`).
*   **Updated:**
    *   Direct updates to the `t_flow_file` records are not exposed via the API, but would be possible at the database level.

## 4. Business Rules and Functionality (Detailed)

### Rule 1: File View Authorization

*   **Rule Name:** `ViewFileAccessControl`
*   **Description:** To prevent unauthorized users from accessing files by guessing their IDs, a time-based token mechanism is used.
*   **Triggering Event:** A `GET` request to `/flow-files/view`.
*   **Logic/Conditions:** The `createTime` provided in the request URL must exactly match the `createTime` stored in the `t_flow_file` record for the given `id`.
*   **Outcome/Action:**
    *   If `createTime` matches, the file data is returned.
    *   If `createTime` does not match, a `FailureMessageException` is thrown, resulting in an error response.

### Rule 2: File Deletion Authorization

*   **Rule Name:** `DeleteFileAccessControl`
*   **Description:** Ensures that only authorized users can delete a file.
*   **Triggering Event:** A `DELETE` request to `/flow-files/{id}`.
*   **Logic/Conditions:** The user making the request must be the owner of the `BalanceFlow` record associated with the `FlowFile`. The `flowFileService.remove` method retrieves the `BalanceFlow` and the system's security context implicitly enforces this.
*   **Outcome/Action:**
    *   If the user is authorized, the `FlowFile` is deleted.
    *   If the user is not authorized, a `FailureMessageException` is thrown with an "auth.error" message.

### Validations

*   **Back-end Validations:**
    *   **File Upload (`@ValidFile`):**
        *   **Rule:** The uploaded file must not be empty.
        *   **Consequence:** If the file is empty, a validation error is returned to the client.
    *   **File View (`FlowFileViewForm`):**
        *   **Rule:** The `id` and `createTime` must be provided.
        *   **Consequence:** If missing, a validation error is returned.

## 5. Detailed Test Cases

| Test Case ID | Feature Being Tested | Preconditions | Test Steps | Test Data | Expected Result |
|---|---|---|---|---|---|
| TC-FF-001 | Upload File (Happy Path) | User is authenticated. A `BalanceFlow` with ID `1` exists. | 1. Send `POST` to `/balance-flows/1/addFile`. | `file`: a valid, non-empty PNG file. | HTTP 200 OK. The response body contains the details of the new `FlowFile`. The file is present in the `t_flow_file` table. |
| TC-FF-002 | Upload File (Negative) | User is authenticated. | 1. Send `POST` to `/balance-flows/1/addFile`. | `file`: an empty file. | HTTP 400 Bad Request. Error message indicating the file is empty. |
| TC-FF-003 | View File (Happy Path) | A `FlowFile` with ID `10` and `createTime` `1678886400000` exists. | 1. Send `GET` to `/flow-files/view?id=10&createTime=1678886400000`. | - | HTTP 200 OK. The response body contains the binary data of the file with the correct `Content-Type`. |
| TC-FF-004 | View File (Negative) | A `FlowFile` with ID `10` and `createTime` `1678886400000` exists. | 1. Send `GET` to `/flow-files/view?id=10&createTime=1234567890000`. | - | HTTP 4xx/5xx error. An error message is returned due to the `createTime` mismatch. |
| TC-FF-005 | Delete File (Happy Path) | User is authenticated and owns the `BalanceFlow` associated with `FlowFile` ID `15`. | 1. Send `DELETE` to `/flow-files/15`. | - | HTTP 200 OK. The `FlowFile` with ID `15` is removed from the `t_flow_file` table. |
| TC-FF-006 | Delete File (Negative) | User is authenticated but does *not* own the `BalanceFlow` associated with `FlowFile` ID `15`. | 1. Send `DELETE` to `/flow-files/15`. | - | HTTP 4xx/5xx error. An "auth.error" message is returned. |

## 6. State Any Assumptions

*   It is assumed that the front-end application is responsible for constructing the correct URL for viewing files, including the `createTime` parameter.
*   It is assumed that the `@ValidFile` annotation correctly checks for empty files and potentially other constraints like file size or type, although the full implementation of this annotation was not reviewed.
*   It is assumed that the application's authentication and authorization mechanism (e.g., `SessionUtil`, `BaseService`) correctly identifies the current user and their permissions regarding `BalanceFlow` entities.
*   The `Thread.sleep(4000)` in `BalanceFlowController.handleAddFile` is assumed to be for debugging or simulating network latency and would be removed in a production environment.
