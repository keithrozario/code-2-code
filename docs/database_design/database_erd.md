erDiagram
    t_user_user {
        int id PK "User ID"
        string username
        string nickName
        string password
        string telephone
        string email
        string registerIp
        int defaultGroup_id FK "Default Group ID"
        int defaultBook_id FK "Default Book ID"
        boolean enable
        long registerTime
        string headimgurl
    }

    t_user_group {
        int id PK "Group ID"
        string name
    }

    t_user_book {
        int id PK "Book ID"
        string name
        int group_id FK "Group ID"
        string notes
        boolean enable
        int defaultExpenseAccount_id FK "FK to t_user_account"
        int defaultIncomeAccount_id FK "FK to t_user_account"
        int defaultTransferFromAccount_id FK "FK to t_user_account"
        int defaultTransferToAccount_id FK "FK to t_user_account"
        int defaultExpenseCategory_id FK "FK to t_user_category"
        int defaultIncomeCategory_id FK "FK to t_user_category"
        string defaultCurrencyCode
        long exportAt
        int sort
    }

    t_user_account {
        int id PK "Account ID"
        string name
        int group_id FK "Group ID"
        int type
        string notes
        boolean enable
        string no
        BigDecimal balance
        boolean include
        boolean canExpense
        boolean canIncome
        boolean canTransferFrom
        boolean canTransferTo
        string currencyCode
        BigDecimal initialBalance
        BigDecimal creditLimit
        int billDay
        BigDecimal apr
        int sort
    }

    t_user_balance_flow {
        int id PK "Balance Flow ID"
        int book_id FK "Book ID"
        int type
        BigDecimal amount
        BigDecimal convertedAmount
        int account_id FK "Account ID"
        long createTime
        string title
        string notes
        int creator_id FK "Creator User ID"
        int group_id FK "Group ID"
        int to_id FK "Destination Account ID"
        int payee_id FK "Payee ID"
        boolean confirm
        boolean include
        long insertAt
    }

    t_user_category {
        int id PK "Category ID"
        string name
        int parent_id FK "Parent Category ID"
        int book_id FK "Book ID"
        string notes
        boolean enable
        int type
        int sort
    }

    t_user_payee {
        int id PK "Payee ID"
        string name
        int book_id FK "Book ID"
        string notes
        boolean enable
        boolean canExpense
        boolean canIncome
        int sort
    }

    t_user_tag {
        int id PK "Tag ID"
        string name
        int parent_id FK "Parent Tag ID"
        int book_id FK "Book ID"
        string notes
        boolean enable
        boolean canExpense
        boolean canIncome
        boolean canTransfer
        int sort
    }

    t_flow_file {
        int id PK "File ID"
        byte[] data
        int creator_id FK "Creator User ID"
        int flow_id FK "Balance Flow ID"
        long createTime
        string contentType
        long size
        string originalName
    }

    t_user_category_relation {
        int id PK "Relation ID"
        int category_id FK "Category ID"
        int balanceFlow_id FK "Balance Flow ID"
        BigDecimal amount
        BigDecimal convertedAmount
    }

    t_user_tag_relation {
        int id PK "Relation ID"
        int tag_id FK "Tag ID"
        int balanceFlow_id FK "Balance Flow ID"
        BigDecimal amount
        BigDecimal convertedAmount
    }

    t_user_group }o--|| t_user_user : "is default for"
    t_user_book }o--|| t_user_user : "is default for"
    t_user_user ||--|{ t_user_balance_flow : "creates"
    t_user_user ||--|{ t_flow_file : "creates"

    t_user_group ||--|{ t_user_book : "contains"
    t_user_group ||--|{ t_user_account : "contains"
    t_user_group ||--|{ t_user_balance_flow : "contains"

    t_user_book ||--|{ t_user_balance_flow : "contains"
    t_user_book ||--|{ t_user_category : "defines"
    t_user_book ||--|{ t_user_payee : "defines"
    t_user_book ||--|{ t_user_tag : "defines"
    t_user_account }o--|| t_user_book : "is default for"
    t_user_category }o--|| t_user_book : "is default for"

    t_user_account ||--|{ t_user_balance_flow : "is source for"
    t_user_account }o--|| t_user_balance_flow : "is destination for"

    t_user_payee }o--|| t_user_balance_flow : "is payee for"

    t_user_balance_flow ||--|{ t_flow_file : "has"
    
    t_user_balance_flow }|--|| t_user_category_relation : "links to"
    t_user_category }|--|| t_user_category_relation : "linked via"

    t_user_balance_flow }|--|| t_user_tag_relation : "links to"
    t_user_tag }|--|| t_user_tag_relation : "linked via"

    t_user_category }o--|| t_user_category : "is parent of"
    t_user_tag }o--|| t_user_tag : "is parent of"
