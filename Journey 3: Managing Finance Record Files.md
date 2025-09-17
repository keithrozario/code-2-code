# Journey 3: Managing Finance Record Files

This document details the user journey for attaching, viewing, and managing digital files associated with financial transactions.

## 1. Detailed User Journey and Flows

This journey allows users to upload, view, and delete file attachments (e.g., receipts, invoices) for their transaction records.

### Journey: Attaching, Viewing, and Deleting a File

**User Flow:**
1.  The user is viewing the details of a specific transaction (`BalanceFlow`).
2.  They click an "Add Attachment" or "Upload File" button.
3.  A file selection dialog opens on their device. The user selects a file (e.g., a PDF, PNG, or JPG).
4.  The file is uploaded to the server. The system validates the file type and size.
5.  Upon successful upload, the file appears in a list of attachments for that transaction.
6.  The user can later click on the file's name to view it in the browser or download it.
7.  The user can also choose to delete an attachment, which removes the file from the system permanently.

## 2. Detailed Object-Level Data Structures

The primary data structure for this journey is the `FlowFile` entity.

### `FlowFile` Entity (`t_flow_file` table)

This entity represents a single file attached to a transaction.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | Primary Key. |
| `data` | `byte[]` | The binary content of the file, stored as a `LONGBLOB` in the database. It is lazily fetched for performance. |
| `creator` | `User` | (FK) The user who uploaded the file. |
| `flow` | `BalanceFlow` | (FK) The transaction this file is attached to. |
| `createTime` | `Long` | The timestamp when the file was uploaded. |
| `contentType` | `String` | The MIME type of the file (e.g., "application/pdf"). |
| `size` | `Long` | The size of the file in bytes. |
| `originalName` | `String` | The original filename from the user's device. |

### `FlowFileDetails` Data Structure

This is the DTO used for sending file metadata to the client. It omits the large `data` field.

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `id` | `Integer` | File ID. |
| `createTime` | `Long` | Upload timestamp. |
| `contentType` | `String` | File MIME type. |
| `size` | `Long` | File size. |
| `originalName` | `String` | Original filename. |

## 3. Database Tables to be Updated

-   **`t_flow_file`**:
    -   A new record is **inserted** when a file is uploaded.
    -   A record is **deleted** when a file is removed.
-   **`t_user_balance_flow`**: When a transaction is updated, the associated `FlowFile` records are re-linked to the new transaction record. When a transaction is deleted, all its associated `FlowFile` records are also deleted.

## 4. API Calls

The interactions are handled by `BalanceFlowController` and `FlowFileController`.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/balance-flows/{id}/addFile` | Uploads a file and attaches it to the transaction with the specified `id`. |
| `GET` | `/balance-flows/{id}/files` | Retrieves a list of all file attachments for the specified transaction. |
| `GET` | `/flow-files/view` | Serves the binary content of a file for viewing or downloading. Requires `id` and `createTime` for access. |
| `DELETE` | `/flow-files/{id}` | Deletes a specific file attachment. |

## 5. Business Rules and Functionality

The core logic is handled by `BalanceFlowService` and `FlowFileService`.

-   **File Upload and Association**: The `BalanceFlowService.addFile` method handles the `MultipartFile` upload. It creates a `FlowFile` entity, populates it with the file's binary data and metadata, and associates it with the correct `BalanceFlow` record.

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

-   **File Validation**: The system uses a custom validator (`@ValidFile`) that checks the `Content-Type` of the uploaded file. It only permits `application/pdf`, `image/png`, `image/jpg`, and `image/jpeg`. This is enforced at the controller level.

    ```java
    // In FileValidator.java
    private boolean isSupportedContentType(String contentType) {
        return contentType.equals("application/pdf")
                || contentType.equals("image/png")
                || contentType.equals("image/jpg")
                || contentType.equals("image/jpeg");
    }
    ```

-   **Secure File Viewing**: To prevent unauthorized access or simple enumeration of file URLs, the `/flow-files/view` endpoint requires both the file `id` and its `createTime` timestamp as parameters. The service layer validates that both match the record in the database before serving the file content.

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

-   **Cascading Deletes**: When a `BalanceFlow` transaction is deleted, the system explicitly deletes all associated `FlowFile` records to prevent orphaned files in the database.

    ```java
    // In BalanceFlowService.java
    public boolean remove(int id) {
        BalanceFlow entity = baseService.findFlowById(id);
        refundBalance(entity);
        // 要先删除文件 (Translation: Must delete files first)
        flowFileRepository.deleteByFlow(entity);
        balanceFlowRepository.delete(entity);
        return true;
    }
    ```

## 6. Detailed Test Cases

| Test Case ID | Description | Expected Result |
| :--- | :--- | :--- |
| **TC-FILE-01** | Upload a valid PDF file (`< 100MB`) to a transaction. | The API returns a 200 OK status. A new `FlowFile` record is created and linked to the transaction. |
| **TC-FILE-02** | Attempt to upload an unsupported file type (e.g., `.zip`, `.exe`). | The API should return a validation error (400 Bad Request). No file record is created. |
| **TC-FILE-03** | Attempt to upload a file larger than the configured limit (100MB). | The request should be rejected by the server, likely with a `MaxUploadSizeExceededException`. |
| **TC-FILE-04** | Retrieve the list of files for a transaction with two attachments. | The API returns a JSON array with two `FlowFileDetails` objects. |
| **TC-FILE-05** | View an attached file using the correct `id` and `createTime`. | The API returns the file's binary data with the correct `Content-Type` header. |
| **TC-FILE-06** | Attempt to view a file with the correct `id` but an incorrect `createTime`. | The API should return an error (e.g., 400 Bad Request or 404 Not Found). |
| **TC-FILE-07** | Delete a file attachment. | The `FlowFile` record is deleted from the database. The associated `BalanceFlow` transaction remains untouched. |
| **TC-FILE-08** | Delete a transaction that has file attachments. | The `BalanceFlow` record and all associated `FlowFile` records are deleted from the database. |

## 7. State any Assumptions

*   The user is authenticated and has permission to view and modify the transaction they are attaching files to.
*   The maximum file size is configured in `application.properties` (`spring.servlet.multipart.max-file-size=100MB`).
*   The frontend is responsible for constructing the correct URL for the `/flow-files/view` endpoint, including both the `id` and `createTime` parameters.
*   Storing binary files directly in the database (`LONGBLOB`) is an acceptable storage strategy for the scale of this application, though it can impact database performance and backup size.
