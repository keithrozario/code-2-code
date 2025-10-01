
import sqlite3

def create_database():
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # Create tables
    c.execute("""
    CREATE TABLE t_user_user (
        id INTEGER PRIMARY KEY,
        username TEXT,
        nickName TEXT,
        password TEXT,
        telephone TEXT,
        email TEXT,
        registerIp TEXT,
        defaultGroup_id INTEGER,
        defaultBook_id INTEGER,
        enable INTEGER,
        registerTime INTEGER,
        headimgurl TEXT,
        FOREIGN KEY (defaultGroup_id) REFERENCES t_user_group(id),
        FOREIGN KEY (defaultBook_id) REFERENCES t_user_book(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_user_group (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
    """)

    c.execute("""
    CREATE TABLE t_user_book (
        id INTEGER PRIMARY KEY,
        name TEXT,
        group_id INTEGER,
        notes TEXT,
        enable INTEGER,
        defaultExpenseAccount_id INTEGER,
        defaultIncomeAccount_id INTEGER,
        defaultTransferFromAccount_id INTEGER,
        defaultTransferToAccount_id INTEGER,
        defaultExpenseCategory_id INTEGER,
        defaultIncomeCategory_id INTEGER,
        defaultCurrencyCode TEXT,
        exportAt INTEGER,
        sort INTEGER,
        FOREIGN KEY (group_id) REFERENCES t_user_group(id),
        FOREIGN KEY (defaultExpenseAccount_id) REFERENCES t_user_account(id),
        FOREIGN KEY (defaultIncomeAccount_id) REFERENCES t_user_account(id),
        FOREIGN KEY (defaultTransferFromAccount_id) REFERENCES t_user_account(id),
        FOREIGN KEY (defaultTransferToAccount_id) REFERENCES t_user_account(id),
        FOREIGN KEY (defaultExpenseCategory_id) REFERENCES t_user_category(id),
        FOREIGN KEY (defaultIncomeCategory_id) REFERENCES t_user_category(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_user_account (
        id INTEGER PRIMARY KEY,
        name TEXT,
        group_id INTEGER,
        type INTEGER,
        notes TEXT,
        enable INTEGER,
        no TEXT,
        balance REAL,
        include INTEGER,
        canExpense INTEGER,
        canIncome INTEGER,
        canTransferFrom INTEGER,
        canTransferTo INTEGER,
        currencyCode TEXT,
        initialBalance REAL,
        creditLimit REAL,
        billDay INTEGER,
        apr REAL,
        sort INTEGER,
        FOREIGN KEY (group_id) REFERENCES t_user_group(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_user_balance_flow (
        id INTEGER PRIMARY KEY,
        book_id INTEGER,
        type INTEGER,
        amount REAL,
        convertedAmount REAL,
        account_id INTEGER,
        createTime INTEGER,
        title TEXT,
        notes TEXT,
        creator_id INTEGER,
        group_id INTEGER,
        to_id INTEGER,
        payee_id INTEGER,
        confirm INTEGER,
        include INTEGER,
        insertAt INTEGER,
        FOREIGN KEY (book_id) REFERENCES t_user_book(id),
        FOREIGN KEY (account_id) REFERENCES t_user_account(id),
        FOREIGN KEY (creator_id) REFERENCES t_user_user(id),
        FOREIGN KEY (group_id) REFERENCES t_user_group(id),
        FOREIGN KEY (to_id) REFERENCES t_user_account(id),
        FOREIGN KEY (payee_id) REFERENCES t_user_payee(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_user_category (
        id INTEGER PRIMARY KEY,
        name TEXT,
        parent_id INTEGER,
        book_id INTEGER,
        notes TEXT,
        enable INTEGER,
        type INTEGER,
        sort INTEGER,
        FOREIGN KEY (parent_id) REFERENCES t_user_category(id),
        FOREIGN KEY (book_id) REFERENCES t_user_book(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_user_payee (
        id INTEGER PRIMARY KEY,
        name TEXT,
        book_id INTEGER,
        notes TEXT,
        enable INTEGER,
        canExpense INTEGER,
        canIncome INTEGER,
        sort INTEGER,
        FOREIGN KEY (book_id) REFERENCES t_user_book(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_user_tag (
        id INTEGER PRIMARY KEY,
        name TEXT,
        parent_id INTEGER,
        book_id INTEGER,
        notes TEXT,
        enable INTEGER,
        canExpense INTEGER,
        canIncome INTEGER,
        canTransfer INTEGER,
        sort INTEGER,
        FOREIGN KEY (parent_id) REFERENCES t_user_tag(id),
        FOREIGN KEY (book_id) REFERENCES t_user_book(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_flow_file (
        id INTEGER PRIMARY KEY,
        data BLOB,
        creator_id INTEGER,
        flow_id INTEGER,
        createTime INTEGER,
        contentType TEXT,
        size INTEGER,
        originalName TEXT,
        FOREIGN KEY (creator_id) REFERENCES t_user_user(id),
        FOREIGN KEY (flow_id) REFERENCES t_user_balance_flow(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_user_category_relation (
        id INTEGER PRIMARY KEY,
        category_id INTEGER,
        balanceFlow_id INTEGER,
        amount REAL,
        convertedAmount REAL,
        FOREIGN KEY (category_id) REFERENCES t_user_category(id),
        FOREIGN KEY (balanceFlow_id) REFERENCES t_user_balance_flow(id)
    )
    """)

    c.execute("""
    CREATE TABLE t_user_tag_relation (
        id INTEGER PRIMARY KEY,
        tag_id INTEGER,
        balanceFlow_id INTEGER,
        amount REAL,
        convertedAmount REAL,
        FOREIGN KEY (tag_id) REFERENCES t_user_tag(id),
        FOREIGN KEY (balanceFlow_id) REFERENCES t_user_balance_flow(id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database 'example.db' created successfully.")
