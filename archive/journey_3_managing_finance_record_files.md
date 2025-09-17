# Journey 3: Managing Finance Record Files

This document details the user journey for attaching, viewing, and managing digital files (like receipts or invoices) associated with financial transactions.

## 1. Detailed User Journey and Flows

This journey focuses on the lifecycle of a file attachment linked to a `BalanceFlow` (transaction).

### Journey 1: Attaching a File to a Transaction

This is the primary flow where a user uploads a document and links it to an existing transaction record.

**User Flow:**
1.  The user is viewing the details of an existing transaction.
2.  They click an "Add Attachment" or "Upload File" button.
3.  A file picker dialog appears, allowing them to select a file from their local device.
4.  The user selects a file (e.g., `receipt.pdf`, `invoice.jpg`).
5.  The file is uploaded to the server.
6.  The UI updates to show the newly uploaded file in a list of attachments for that transaction.

### Journey 2: Viewing and Downloading an Attachment

This flow describes how a user accesses a previously uploaded file.

**User Flow:**
1.  The user is viewing the details of a transaction that has one or more files attached.
2.  They see a list of attachment filenames.
3.  The user clicks on the filename they wish to view.
4.  The system serves the file, which either opens in a new browser tab (for supported types like PDF and images) or downloads to the user's device.

### Journey 3: Deleting an Attachment

This flow allows a user to remove a file that was previously attached to a transaction.

**User Flow:**
1.  The user is viewing the list of attachments for a transaction.
2.  Next to each filename, there is a "Delete" or "Remove" icon/button.
3.  The user clicks the delete button for the file they want to remove.
4.  The system prompts for confirmation.
5.  Upon confirmation, the file is permanently deleted from the system, and the attachment list on the UI is updated.

## 2. Detailed Object-Level Data Structures

The core data structure for this journey is the `FlowFile` entity.

### `FlowFile` Entity (`t_flow_file` table)

This entity represents a single file attached to a transaction.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `data` | `byte[]` | The binary content of the file, stored as a `LONGBLOB`. |
| `creator` | `User` | (FK) The user who uploaded the file. |
| `flow` | `BalanceFlow` | (FK) The transaction this file is attached to. |
| `createTime` | `Long` | The timestamp (in milliseconds) when the file was uploaded. |
| `contentType` | `String` | The MIME type of the file (e.g., "application/pdf"). |
| `size` | `Long` | The size of the file in bytes. |
| `originalName` | `String` | The original filename on the user's device. |

### `FlowFileDetails` Data Structure

This DTO is used to send file metadata to the client, excluding the large binary `data`.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `createTime` | `Long` | Upload timestamp. |
| `contentType` | `String` | File MIME type. |
| `size` | `Long` | File size. |
| `originalName` | `String` | Original filename. |

### `FlowFileViewForm` Data Structure

This DTO is used for securely requesting a file's content.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | The ID of the file to view. |
| `createTime` | `Long` | The creation timestamp of the file, used as a security check. |

## 3. Database Tables to be Updated

-   **`t_flow_file`**:
    -   A new record is **inserted** when a file is uploaded.
    -   A record is **deleted** when a user removes an attachment.
    -   When a `BalanceFlow` record is deleted, all associated records in this table are also **deleted** (cascading delete).

## 4. API Calls

The interactions are handled by `BalanceFlowController` and `FlowFileController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/balance-flows/{id}/addFile` | Uploads a new file and attaches it to the `BalanceFlow` with the given `id`. |
| `GET` | `/balance-flows/{id}/files` | Retrieves a list of `FlowFileDetails` for a specific transaction. |
| `GET` | `/flow-files/view` | Securely serves the binary content of a file for viewing or downloading. |
| `DELETE` | `/flow-files/{id}` | Deletes a specific file attachment. |

## 5. Business Rules and Functionality

The logic is primarily managed by `BalanceFlowService` and `FlowFileService`.

-   **File Upload and Storage**: The `BalanceFlowService.addFile` method handles the `MultipartFile` upload. It reads the file's bytes and metadata, populates a `FlowFile` entity, and saves it to the database.

    ```java
    // In BalanceFlowService.java
    public FlowFileDetails addFile(Integer id, MultipartFile file) {
        FlowFile flowFile = new FlowFile();
        try {
            flowFile.setData(file.getBytes());
        } catch (IOException e) {
            throw new FailureMessageException("add.flow.file.fail");
        }
        flowFile.setCreator(sessionUtil.getCurrentUser());
        flowFile.setFlow(baseService.findFlowById(id));
        flowFile.setCreateTime(System.currentTimeMillis());
        flowFile.setSize(file.getSize());
        flowFile.setContentType(file.getContentType());
        flowFile.setOriginalName(file.getOriginalFilename());
        flowFileRepository.save(flowFile);
        return FlowFileMapper.toDetails(flowFile);
    }
    ```

-   **File Validation**: The system uses a custom validator (`@ValidFile`) that checks the content type of the uploaded file. Only specific MIME types are allowed.

    ```java
    // In FileValidator.java
    private boolean isSupportedContentType(String contentType) {
        return contentType.equals("application/pdf")
                || contentType.equals("image/png")
                || contentType.equals("image/jpg")
                || contentType.equals("image/jpeg");
    }
    ```

-   **File Size Limit**: The maximum allowed size for an uploaded file and the overall request is configured in `application.properties` to be 100MB.

    ```properties
    # In application.properties
    spring.servlet.multipart.max-request-size=100MB
    spring.servlet.multipart.max-file-size=100MB
    ```

-   **Secure Viewing**: To prevent unauthorized access or enumeration of files, the `/flow-files/view` endpoint requires both the file's `id` and its `createTime`. The service layer validates that both parameters match the record in the database before returning the file data.

    ```java
    // In FlowFileService.java
    public FlowFile getFile(FlowFileViewForm form) {
        FlowFile flowFile =  flowFileRepository.getReferenceById(form.getId());
        if (!flowFile.getCreateTime().equals(form.getCreateTime())) {
            throw new FailureMessageException();
        }
        return flowFile;
    }
    ```

-   **Cascading Deletes**: When a `BalanceFlow` transaction is deleted, the `BalanceFlowService.remove()` method explicitly deletes all associated `FlowFile` records to prevent orphaned files in the database.

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-FILE-01** | Upload a valid file (`.pdf`, 1MB) to an existing transaction. | The API returns a 200 OK with the file details. A new record is created in the `t_flow_file` table. |
| **TC-FILE-02** | Attempt to upload an unsupported file type (e.g., `.exe`, `.zip`). | The API should return a validation error (400 Bad Request). No file record is created. |
| **TC-FILE-03** | Attempt to upload a file larger than the 100MB limit. | The API should return an error indicating the file size exceeds the limit. No file is saved. |
| **TC-FILE-04** | Request to view a file with the correct `id` and `createTime`. | The API returns a 200 OK with the file's binary data and the correct `Content-Type` header. |
| **TC-FILE-05** | Request to view a file with a correct `id` but an incorrect `createTime`. | The API should return an error (e.g., 400 Bad Request or 404 Not Found) and not serve the file. |
| **TC-FILE-06** | Delete an existing file attachment. | The API returns a 200 OK. The corresponding record in `t_flow_file` is deleted. |
| **TC-FILE-07** | Delete a `BalanceFlow` transaction that has two file attachments. | The `BalanceFlow` record and both associated `FlowFile` records are deleted from the database. |

## 7. State any Assumptions

*   The user is authenticated and has the necessary permissions to view and modify the transaction they are attaching files to.
*   Storing file binaries directly in the database (`LONGBLOB`) is an accepted design decision, though it may have performance and scalability implications compared to storing files in a dedicated object store like S3 or Google Cloud Storage.
*   The 4-second `Thread.sleep(4000)` in the `BalanceFlowController.handleAddFile` method is assumed to be a temporary debugging or testing artifact and not an intentional business requirement.
*   The security model for file viewing (requiring `id` and `createTime`) is considered sufficient for the application's needs.

