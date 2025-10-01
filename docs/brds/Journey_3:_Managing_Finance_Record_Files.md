# Business Requirement Document: Managing Finance Record Files

## 1.0 Summary
This document outlines the business requirements for managing file attachments associated with financial transactions within the MoneyNote application. The system provides capabilities for users to upload, view, and delete supporting documents (e.g., receipts, invoices) for their transaction records. This functionality enhances record-keeping by allowing users to maintain a complete and verifiable history of their financial activities. All file data is stored directly within the application's primary database.

---

## 2.0 Project Scope
### 2.1 In-Scope
*   **FR-001:** A user must be able to upload a file and associate it with a specific financial transaction.
*   **FR-002:** A user must be able to view the content of an uploaded file.
*   **FR-003:** A user must be able to delete a file that is associated with a financial transaction.
*   **FR-004:** The system must enforce a maximum file size for uploads.
*   **FR-005:** The system must restrict file access to authorized users.

### 2.2 Out-of-Scope
*   Editing or modifying the content of a file after it has been uploaded.
*   Uploading multiple files in a single transaction.
*   Storing files in an external object store (e.g., S3, Google Cloud Storage). All files are stored as BLOBs in the database.
*   Advanced file versioning or history.

---

## 3.0 Business Requirements
The following business requirements define the core capabilities of the file management feature.

**BR-001:** The system must provide a mechanism for users to attach digital files to individual financial records to serve as supporting documentation. This is achieved by allowing file uploads against a specific `BalanceFlow` entity, which are then stored as `FlowFile` entities. This is critical for maintaining accurate and auditable financial records.

**BR-002:** The system must ensure that only authorized users can view or delete files. Access control is managed by linking file ownership to the ownership of the parent financial transaction, preventing unauthorized data exposure.

**BR-003:** The system must enforce resource limits to maintain system performance and control storage costs. This includes a strict file size limit on all uploads.

### 3.1 Functional Requirements
The functional requirements below are derived from the user journeys and are directly traceable to the application's source code.

**FR-001: File Upload**
*   **Requirement:** The system must allow an authenticated user to upload a single file attachment to a specific financial transaction (`BalanceFlow`). The file's content, original name, size, and content type must be stored. Success is measured by the creation of a `FlowFile` record in the database, linked to the correct `BalanceFlow`. This is implemented in the `BalanceFlowService.addFile` method, which is exposed via the `POST /balance-flows/{id}/addFile` endpoint. This functionality is targeted for all users and is currently active in the system.

**FR-002: File Viewing**
*   **Requirement:** The system must allow a user to view the content of a previously uploaded file. To prevent unauthorized access, the viewing mechanism must require both the file's unique ID and its creation timestamp. The system must return the file's binary data with the correct `Content-Type` header within 2 seconds of a valid request. Success is measured by the successful retrieval and rendering of the file content. This is implemented in the `FlowFileService.getFile` method and exposed via the `GET /flow-files/view` endpoint. This functionality is targeted for all users and is currently active.

**FR-003: File Deletion**
*   **Requirement:** The system must allow a user to permanently delete a file attachment from a financial transaction. The system must verify that the user making the request has the authority to delete the file by checking their permissions on the associated `BalanceFlow`. Success is measured by the removal of the `FlowFile` record from the database. This is implemented in the `FlowFileService.remove` method and exposed via the `DELETE /flow-files/{id}` endpoint. This functionality is targeted for all users and is currently active.

**FR-004: File Size Constraint**
*   **Requirement:** The system must reject any file upload that exceeds a maximum size of 100MB. This limit is enforced at the application server level to prevent excessive resource consumption. Success is measured by the system returning a "Bad Request" error for oversized files. This is configured in the `application.properties` file via the `spring.servlet.multipart.max-file-size=100MB` setting. This constraint is active system-wide.

**FR-005: File View Authorization**
*   **Requirement:** The system must ensure that a user cannot access a file simply by guessing its ID. File access requests must include both the file `id` and its `createTime` as parameters. The system will validate that the provided `createTime` matches the timestamp stored in the database for that file ID. 99.9% of unauthorized access attempts must be blocked. This is implemented in the `FlowFileService.getFile` method. This security measure is active for all file view requests.

---
## 4.0 Assumptions, Constraints, and Dependencies
### 4.1 Assumptions
*   Users have the necessary permissions to modify the financial transactions to which they are uploading files.
*   The client-side application is responsible for correctly constructing the file view URL, including the required `id` and `createTime` parameters.

### 4.2 Dependencies
*   The file management functionality is dependent on the core `BalanceFlow` (transaction) module. Files cannot exist without being associated with a transaction.
*   The system relies on the Spring Framework's multipart file handling capabilities for processing uploads.
