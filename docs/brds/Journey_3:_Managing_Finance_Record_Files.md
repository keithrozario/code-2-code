# Business Requirement Document: Managing Finance Record Files

## 1.0 Summary
This document outlines the business requirements for the management of financial record files within the MoneyNote application. The core business objective is to allow users to attach, view, and manage digital files (such as receipts, invoices, or contracts) associated with their financial transactions. This provides a complete, verifiable audit trail for each record, enhancing data integrity and user confidence. The existing system implements this by allowing users to upload a single file per transaction, which is then stored directly within the application's primary database as a Binary Large Object (BLOB).

---

## 2.0 Project Scope
### 2.1 In-Scope
The scope of this BRD is limited to the existing functionality for managing finance record files, as traced from the source code and system analysis.
*   **FR-001: Attach a Single File to a Transaction:** Users can upload one file and link it to a single financial transaction (`BalanceFlow`).
*   **FR-002: View an Attached File:** Users can retrieve and view a file previously attached to a transaction.
*   **FR-003: Delete an Attached File:** Users can remove a file attachment from a transaction.

### 2.2 Out-of-Scope
The following functionalities are not covered by this document as they are not part of the existing implementation:
*   Attaching multiple files to a single transaction.
*   Editing, annotating, or otherwise modifying an attached file.
*   Bulk import or export of file attachments independent of their associated transactions.
*   Attaching files to entities other than financial transactions (e.g., accounts, categories).

---

## 3.0 Business Requirements

**BR-001: Verifiable Transaction Records:** The system must provide a mechanism for users to associate a single digital file with a financial transaction record to maintain a complete and verifiable financial history. This ensures that for any given expense, income, or transfer, supporting documentation can be stored and retrieved directly within the application.

### 3.1 Functional Requirements

**FR-001: Upload and Attach File**
*   **Requirement:** The system must provide a feature for users to upload a single file, up to a maximum size of 100MB, and associate it with a single financial transaction (`BalanceFlow`).
*   **Measure:** Success will be verified by a 100% success rate during User Acceptance Testing (UAT) for valid file uploads. The file data must be correctly persisted as a `LONGBLOB` in the `t_flow_file` table and linked to the correct `t_user_balance_flow` record.
*   **Agreed Upon:** This requirement reflects the existing, validated functionality.
*   **Realistic:** The functionality is already implemented and proven.
*   **Traceability:** This is implemented in the `BalanceFlowService.addFile` method, with the size constraint defined in the `application.properties` file (`spring.servlet.multipart.max-file-size=100MB`). The `FlowFile` entity (`cn/biq/mn/flowfile/FlowFile.java`) models the database storage.

**FR-002: View Attached File**
*   **Requirement:** The system must provide an endpoint for users to retrieve and view the content of a previously uploaded file associated with a transaction.
*   **Measure:** Success is defined as the file being viewable in the client application within 3 seconds of the request for files under 10MB. The system must serve the binary data with the correct content type to enable proper rendering.
*   **Agreed Upon:** This is a core feature for accessing stored documentation.
*   **Realistic:** The functionality is currently implemented and in use.
*   **Traceability:** This is implemented in the `FlowFileController.handleView` endpoint, which serves the `byte[]` data from the `FlowFile` entity.

**FR-003: Delete Attached File**
*   **Requirement:** The system must allow a user to permanently remove a file attachment from a financial transaction record.
*   **Measure:** Success will be measured by the successful removal of the corresponding `FlowFile` database entry upon user action, confirmed via functional testing. The file must no longer be accessible via the view endpoint (FR-002).
*   **Agreed Upon:** This is an essential management function for correcting errors or removing sensitive data.
*   **Realistic:** The functionality is achievable via standard database delete operations on the `FlowFile` entity.
*   **Traceability:** This action is handled within the service layer responsible for `BalanceFlow` and `FlowFile` modifications, which deletes the `FlowFile` entity record associated with a `BalanceFlow`.

---
## 4.0 Assumptions, Constraints, and Dependencies
### 4.1 Assumptions
*   Users performing file management operations have the necessary permissions to view and modify the parent financial transaction record.
*   The client-side application is responsible for providing the user interface for file upload, view, and delete actions.

### 4.2 Constraints
*   **Database Storage:** All attached files are stored directly in the primary MySQL database as `LONGBLOB` data types. This is a hard constraint of the current architecture. (Source: CodMod Report, `FlowFile.java`)
*   **Single File per Transaction:** The data model supports only one file attachment per `BalanceFlow` record. (Source: CodMod Report, Data Model analysis)
*   **File Size Limit:** The system imposes a hard limit of 100MB for any single file upload. (Source: CodMod Report, `application.properties`)

### 4.3 Dependencies
*   The file attachment functionality is entirely dependent on the existence of the core transaction module (`BalanceFlow`). A file cannot exist without being associated with a transaction.
*   The underlying database must support `LONGBLOB` data types for the functionality to work as designed.
