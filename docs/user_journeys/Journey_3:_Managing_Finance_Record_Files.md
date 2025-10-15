# User Journey Analysis: Journey 3: Managing Finance Record Files

### 1.0 Detailed User Journeys and Flows

This section outlines the step-by-step interactions a user has with the system to manage file attachments for their financial records.

**Flow 1: Attaching a New File to a Transaction**

1.  **Start Point:** The user is viewing the details of an existing transaction (e.g., an expense for a new laptop).
2.  **User Action:** The user clicks the "Add Attachment" or "Upload File" button within the transaction's detail view.
3.  **System Response:** The system presents a file selection dialog, allowing the user to browse their local device.
4.  **User Action:** The user selects a file (e.g., `receipt.pdf`) and confirms the selection.
5.  **System Response:** The file is uploaded to the server. The system validates the file based on pre-configured rules (file type and size).
    *   **Success Path:** If the file is valid, it is saved and linked to the transaction. The UI refreshes to show the newly attached file in a list of attachments for that transaction.
    *   **Error Path (Invalid Type/Size):** If the file is invalid (e.g., a `.zip` file or a file larger than 100MB), the system rejects the upload and displays an error message to the user (e.g., "File type not supported" or "File size exceeds limit").
6.  **End Point:** The user can see the file successfully attached to the transaction record.

**Flow 2: Viewing an Attached File**

1.  **Start Point:** The user is viewing the details of a transaction that has one or more files attached.
2.  **User Action:** The user clicks on the name or icon of an attached file they wish to view.
3.  **System Response:** The system serves the file content to the user's browser. The browser then either displays the file directly (for supported types like images and PDFs) or prompts the user to download it.
4.  **End Point:** The user has successfully viewed or downloaded the attached file.

**Flow 3: Deleting an Attached File**

1.  **Start Point:** The user is viewing the details of a transaction that has one or more files attached.
2.  **User Action:** The user clicks a "Delete" or "Remove" icon next to the specific file they want to remove.
3.  **System Response:** The system may ask for confirmation (e.g., "Are you sure you want to delete this file?").
4.  **User Action:** The user confirms the deletion.
5.  **System Response:** The system deletes the file from the database and removes its reference from the transaction. The UI refreshes the list of attachments, which no longer includes the deleted file.
6.  **End Point:** The file is permanently removed from the transaction record.

---

### 2.0 Detailed Object Level Data Structures

The primary data entity for this journey is `FlowFile`, which is stored in the `t_flow_file` table. It holds the binary data and metadata for each uploaded file and is directly linked to a financial transaction (`BalanceFlow`).

**Table: `t_flow_file`**

| Attribute | Data Type | Constraints & Description |
| :--- | :--- | :--- |
| `id` | `INTEGER` | **Primary Key**, Auto-incremented. |
| `flow_id` | `INTEGER` | **Foreign Key** -> `t_user_balance_flow(id)`. The transaction this file is attached to. |
| `original_name` | `VARCHAR(255)` | `NOT NULL`. The original filename as uploaded by the user (e.g., "receipt.jpg"). |
| `content_type` | `VARCHAR(255)` | `NOT NULL`. The MIME type of the file (e.g., "image/jpeg"). |
| `size` | `BIGINT` | `NOT NULL`. The size of the file in bytes. |
| `creator_id` | `INTEGER` | `NOT NULL`, **Foreign Key** -> `t_user_user(id)`. The user who uploaded the file. |
| `create_time` | `BIGINT` | `NOT NULL`. The timestamp (in milliseconds) when the file was uploaded. |
| `data` | `LONGBLOB` | `NOT NULL`. The binary content of the file itself. |

**Relationships:**

*   A `BalanceFlow` (transaction) can have a one-to-many relationship with `FlowFile`. One transaction can have multiple file attachments.
*   Each `FlowFile` has a many-to-one relationship with a single `BalanceFlow`.

---

### 3.0 Database Tables to be Updated

This user journey directly impacts the following database tables:

| Table Name | Operations Performed |
| :--- | :--- |
| **`t_flow_file`** | **`INSERT`**: A new record is created when a user uploads a file. <br> **`READ`**: Records are read to list attachments for a transaction or to retrieve file content for viewing. <br> **`DELETE`**: A record is deleted when a user removes an attachment. |
| **`t_user_balance_flow`** | **`READ`**: This table is read to identify the specific transaction to which a file should be attached or from which attachments should be listed. When a transaction is deleted, its associated files are also read to be deleted. |

---

### 4.0 Business Rules and Functionality (Detailed)

The system enforces several business rules to govern the management of finance record files.

| Rule Name | Description | Trigger | Logic | Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **File Association** | Users must be able to upload and associate one or more files with a balance flow transaction. | User initiates a file upload for a specific transaction. | The system links the uploaded `FlowFile` entity to the `BalanceFlow` entity via a foreign key (`flow_id`). | The file is permanently linked to the transaction unless explicitly deleted. |
| **File Type Validation** | File uploads must be restricted to a list of supported content types to ensure security and compatibility. | A file is submitted for upload. | The system checks the file's MIME type against a hardcoded list: `application/pdf`, `image/png`, `image/jpg`, `image/jpeg`. | If the type is supported, the upload proceeds. If not, the upload is rejected with an error. |
| **File Size Limit** | The system must enforce a maximum size for uploaded files. | A file is submitted for upload. | The application configuration (`application.properties`) sets a `max-file-size` limit, which defaults to 100MB. The system checks the incoming file's size against this limit. | If the file is within the size limit, the upload proceeds. If it is too large, the upload is rejected. |
| **Metadata Storage** | The system must store key metadata for each uploaded file. | A file is successfully uploaded. | The system extracts the file's original name, content type, and size and stores these attributes in the `t_flow_file` table along with the binary data. | The metadata is available for display in the UI and for serving the file with the correct headers. |
| **Attachment Deletion** | Users must be able to delete a previously uploaded file from a transaction. | User initiates the deletion of a specific file attachment. | The system identifies the `FlowFile` record by its ID and removes it from the `t_flow_file` table. | The file is permanently deleted, and the link to the transaction is removed. |
| **Secure File Viewing** | Access to view or download a file must be controlled. | User requests to view an attached file. | The file retrieval endpoint requires both the file's `id` and its `create_time` as query parameters. The system validates that a file with that ID and creation timestamp exists before serving the content. | This prevents simple enumeration of file IDs to guess and access unauthorized files. |

---

### 5.0 Test Cases

This section provides test cases to verify the functionality of managing finance record files.

| Test Case ID | Feature Tested | Preconditions | Steps | Test Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-FILE-01** | Happy Path: Upload Supported File | User is logged in and viewing a transaction. | 1. Click "Add Attachment". <br> 2. Select a valid file. <br> 3. Confirm upload. | File: `receipt.pdf` (Size: 50KB) | The file is uploaded successfully and appears in the transaction's attachment list. |
| **TC-FILE-02** | Negative Path: Upload Unsupported File Type | User is logged in and viewing a transaction. | 1. Click "Add Attachment". <br> 2. Select an unsupported file. <br> 3. Confirm upload. | File: `archive.zip` | The system displays an error message "File type not supported" and the upload fails. |
| **TC-FILE-03** | Negative Path: Upload Oversized File | User is logged in and viewing a transaction. | 1. Click "Add Attachment". <br> 2. Select a file larger than the limit. <br> 3. Confirm upload. | File: `large_video.mp4` (Size: 150MB) | The system displays an error message "File size exceeds limit" and the upload fails. |
| **TC-FILE-04** | Happy Path: View Attached File | A transaction has a file (`receipt.pdf`) attached. | 1. Navigate to the transaction details. <br> 2. Click on the link for `receipt.pdf`. | - | The PDF file is opened in a new browser tab or downloaded successfully. |
| **TC-FILE-05** | Happy Path: Delete Attached File | A transaction has a file attached. | 1. Navigate to the transaction details. <br> 2. Click the "Delete" icon next to the file. <br> 3. Confirm the deletion. | - | The file is removed from the attachment list and is no longer accessible. |
| **TC-FILE-06** | Boundary: Access File with Incorrect URL | A file with ID `101` exists. | 1. Attempt to access the file view URL with an incorrect `createTime` parameter (e.g., `/flow-files/view?id=101&createTime=0`). | URL with invalid `createTime`. | The system returns an error (e.g., 404 Not Found or 400 Bad Request) and does not serve the file. |
| **TC-FILE-07** | Data Integrity: Delete Transaction with Attachment | A transaction has a file attached. | 1. Delete the parent transaction record. | - | The associated `FlowFile` record is also deleted from the database (cascading delete). |

---

### 6.0 Assumptions

The following assumptions were made during the analysis of this user journey.

1.  **Analysis Based on Reports:** This document is synthesized primarily from the `customized_report_money_note_detailed_journeys.md` and `customized_report_money_note_data_layer.md` reports. The information and code references within these reports are assumed to be an accurate and complete representation of the source code's functionality.
2.  **Security of File Viewing Endpoint:** The use of `id` and `createTime` to secure the file viewing endpoint is a basic measure to prevent trivial URL guessing. It is assumed that this is considered sufficient for the application's security requirements and that no further authorization checks (beyond the initial session authentication) are performed at this specific endpoint.
3.  **Storage in Database:** The system stores file content directly in the database as a `LONGBLOB`. It is assumed that this design choice was intentional and acceptable for the application's expected scale and performance requirements, despite the common practice of using external object storage.
4.  **Error Message Content:** The exact content of user-facing error messages (e.g., "File type not supported") is assumed based on standard practice; the actual messages in the application may vary.

