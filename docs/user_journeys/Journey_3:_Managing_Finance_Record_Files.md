# Journey 3: Managing Finance Record Files

This document details the user journey and technical specifications for managing file attachments related to financial transactions within the MoneyNote application.

## 1. Detailed User Journeys and Flows

This section captures the step-by-step interactions a user has with the system to attach, view, and manage files associated with their financial records.

### User Journey: Attaching a Receipt to an Expense

The primary goal for the user is to maintain a complete and verifiable record of their transactions by attaching relevant documents, suchs as receipts, invoices, or warranties.

**Start Point:** The user is viewing the details of a specific transaction they have already recorded.

**End Point:** The user has successfully attached a file to the transaction and can see it listed as an attachment.

#### Step-by-Step Flow:

1.  **Navigate to Transaction:** The user locates and opens the details page of a specific financial transaction (a `BalanceFlow`), for example, an expense for a new laptop.
2.  **Initiate File Upload:** On the transaction details screen, the user finds and clicks an "Add Attachment" or "Upload File" button.
3.  **Select File:** This action opens the user's local device file explorer. The user navigates their file system, selects the desired file (e.g., `laptop_receipt.pdf`), and confirms the selection.
4.  **Upload Process:** The selected file is uploaded to the server. The system validates the file against predefined business rules (file type, size).
5.  **System Response (Success):** Upon successful upload and validation, the transaction details page refreshes or updates to display the newly attached file in a list of attachments. The list shows the filename and may include other metadata like file size or upload date.
6.  **System Response (Failure):** If the upload fails (e.g., invalid file type, file too large), the system displays an error message to the user, and no file is attached.

#### Alternative Paths:

*   **Viewing an Attachment:** From the transaction details page, the user can click on the name of any listed attachment. The system will then open the file in a new browser tab for viewing or trigger a download.
*   **Deleting an Attachment:** The user can click a "Delete" or "Remove" icon next to a file in the attachments list. The system will ask for confirmation and, upon receiving it, will permanently delete the file and remove it from the list.

#### Visual Representation (Flowchart):

```mermaid
graph TD
    A[Start: User on Transaction Details Page] --> B{Find "Add Attachment" button};
    B --> C[Click Button];
    C --> D[Open Local File Explorer];
    D --> E[User Selects File];
    E --> F{Upload File to Server};
    F --> G{System Validates File};
    G -- Valid --> H[Store File & Link to Transaction];
    H --> I[Display File in Attachments List];
    I --> J[End: File Attached];
    G -- Invalid --> K[Display Error Message];
    K --> J;

    subgraph "Alternative Flows"
        L[User clicks on attachment name] --> M[System serves file for viewing/download];
        N[User clicks "Delete" on attachment] --> O{Confirm Deletion};
        O -- Yes --> P[System deletes file];
    end

    I --> L;
    I --> N;
```

## 2. Detailed Object Level Data Structures

The core data entity for managing file attachments is `FlowFile`.

### Entity: `FlowFile`

This entity represents a single file attached to a `BalanceFlow` transaction.

| Attribute Name | Data Type | Constraints & Properties | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY`, `AUTO_INCREMENT` | Unique identifier for the file record. |
| `flow` | `BalanceFlow` | `ManyToOne`, `NOT NULL`, `FOREIGN KEY` | The financial transaction this file is attached to. |
| `data` | `byte[]` | `@Lob`, `columnDefinition="LONGBLOB"`, `NOT NULL` | The binary content of the file itself. |
| `contentType` | `String` | `NOT NULL` | The MIME type of the file (e.g., "application/pdf"). |
| `size` | `Long` | `NOT NULL` | The size of the file in bytes. |
| `originalName` | `String` | `NOT NULL` | The original filename as it was on the user's device. |
| `creator` | `User` | `ManyToOne`, `NOT NULL`, `FOREIGN KEY` | The user who uploaded the file. |
| `createTime` | `Long` | `NOT NULL` | The timestamp (in milliseconds) when the file was uploaded. |
| `group` | `Group` | `ManyToOne`, `NOT NULL`, `FOREIGN KEY` | The group the transaction belongs to, for data scoping. |

## 3. Database Tables to be Updated

The file management journey directly impacts the `t_flow_file` table.

| Table Name | Operations Performed | Context |
| :--- | :--- | :--- |
| **`t_flow_file`** | `INSERT`, `SELECT`, `DELETE` | - **`INSERT`**: A new record is created when a user successfully uploads a file. <br>- **`SELECT`**: Records are read to list attachments for a transaction or to retrieve file content for viewing. <br>- **`DELETE`**: A record is deleted when a user removes an attachment. |
| **`t_user_balance_flow`** | `SELECT` | This table is read from to retrieve the context of the transaction to which a file is being attached or from which attachments are being listed. |

## 4. Business Rules and Functionality (Detailed)

This section details the specific logic and validations governing the file attachment feature.

| Rule Name/Identifier | Description | Triggering Event | Logic/Conditions | Outcome/Action |
| :--- | :--- | :--- | :--- | :--- |
| **File Type Validation** | Restricts uploads to a specific set of allowed file formats to ensure security and compatibility. | File Upload | The `contentType` of the uploaded `MultipartFile` is checked against a predefined list. | **Allowed:** `application/pdf`, `image/png`, `image/jpg`, `image/jpeg`. <br> **Rejected:** All other content types. An error is returned to the user. |
| **File Size Limit** | Prevents excessively large files from being uploaded, which could degrade database performance and consume significant storage. | File Upload | The size of the uploaded file is checked against a configured maximum limit. | **Allowed:** File size <= 100MB. <br> **Rejected:** File size > 100MB. An error is returned. This limit is set in `application.properties`. |
| **Attachment Deletion** | Governs the process of removing a file attachment from a transaction. | User clicks the "Delete" button for a file. | The system identifies the `FlowFile` record by its ID and deletes it from the database. | The record is permanently removed from the `t_flow_file` table. The associated `BalanceFlow` transaction is unaffected. |
| **Secure File Viewing** | Provides a layer of security to prevent unauthorized access to files via URL manipulation. | User requests to view/download a file. | The file retrieval endpoint (`/api/v1/flow-files/view`) requires both the file's `id` and its `createTime` as query parameters. | The system will only serve the file if both parameters match the record in the database. This makes it harder for an attacker to guess valid file URLs. |

### Validations

*   **Back-end Validations:**
    *   **Content Type Check:** Performed by `FileValidator.java`. If the MIME type is not in the allowed list, a `MethodArgumentNotValidException` is thrown.
    *   **File Size Check:** Enforced by Spring Boot's multipart configuration (`spring.servlet.multipart.max-file-size=100MB`). If a file exceeds this, a `MultipartException` is thrown.
    *   **Existence Check:** Before serving or deleting a file, the system first checks if a `FlowFile` with the given ID exists, preventing null pointer exceptions.

## 5. Test Cases

This section provides a set of test cases to verify the correct implementation of the file management journey.

| Test Case ID | Feature Being Tested | Preconditions | Test Steps | Test Data | Expected Result |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-FILE-01** | **Happy Path:** Upload PDF | User is logged in and viewing a transaction. | 1. Click "Add Attachment". <br> 2. Select a valid PDF file. <br> 3. Confirm upload. | A PDF file < 100MB. | File is uploaded successfully and appears in the attachments list. |
| **TC-FILE-02** | **Happy Path:** Upload JPG | User is logged in and viewing a transaction. | 1. Click "Add Attachment". <br> 2. Select a valid JPG file. <br> 3. Confirm upload. | A JPG file < 100MB. | File is uploaded successfully and appears in the attachments list. |
| **TC-FILE-03** | **Happy Path:** View Attachment | A file is already attached to a transaction. | 1. Click on the attached file's name. | N/A | The file is opened in a new browser tab or downloaded. |
| **TC-FILE-04** | **Happy Path:** Delete Attachment | A file is already attached to a transaction. | 1. Click the "Delete" icon for the file. <br> 2. Confirm the deletion. | N/A | The file is removed from the attachments list and deleted from the database. |
| **TC-FILE-05** | **Negative Path:** Invalid File Type | User is logged in and viewing a transaction. | 1. Click "Add Attachment". <br> 2. Select an executable file. <br> 3. Confirm upload. | An `.exe` or `.sh` file. | The system rejects the upload and displays an error message: "Invalid file type." |
| **TC-FILE-06** | **Negative Path:** File Too Large | User is logged in and viewing a transaction. | 1. Click "Add Attachment". <br> 2. Select a file larger than the limit. <br> 3. Confirm upload. | A video file of 150MB. | The system rejects the upload and displays an error message: "File size exceeds the 100MB limit." |
| **TC-FILE-07** | **Boundary Condition:** Max File Size | User is logged in and viewing a transaction. | 1. Click "Add Attachment". <br> 2. Select a file that is exactly 100MB. <br> 3. Confirm upload. | A file of size 100MB. | The file is uploaded successfully. |
| **TC-FILE-08** | **Error Handling:** Invalid View URL | User attempts to access a file directly. | 1. Craft a URL with a valid file ID but an incorrect `createTime`. <br> 2. Access the URL. | `GET /api/v1/flow-files/view?id=101&createTime=0` | The system returns a "File not found" error or an HTTP 404 status, not the file content. |

## 6. Assumptions

The following assumptions were made during the analysis of this user journey.

1.  **Database Storage is a Deliberate Choice:** The decision to store file binaries directly in the database (`LONGBLOB`) is assumed to be an intentional design choice for simplicity and to keep the application self-contained, despite the known performance and scalability drawbacks.
2.  **Security of File Content:** It is assumed that no security scanning (e.g., for malware) is performed on uploaded files. The system relies solely on content type validation for security.
3.  **URL Security is Sufficient:** The use of `id` and `createTime` in the viewing URL is assumed to be the only security measure to prevent unauthorized file access. There are no additional session-based or permission checks at this specific endpoint.
4.  **User Has Permissions:** It is assumed that any user who can view a transaction also has the implicit permission to view, add, or delete attachments for that transaction. There is no separate, granular permission model for file management.
