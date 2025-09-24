import sqlite3

DB_NAME = "moneynote.db"

SQL_SCHEMA = """
-- User Table
CREATE TABLE IF NOT EXISTS t_user (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- User Group Table
CREATE TABLE IF NOT EXISTS t_user_group (
    id INTEGER PRIMARY KEY,
    name TEXT,
    defaultCurrencyCode TEXT
);

-- Book Table
CREATE TABLE IF NOT EXISTS t_user_book (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    group_id INTEGER,
    notes TEXT,
    enable INTEGER NOT NULL,
    defaultExpenseAccount_id INTEGER,
    defaultIncomeAccount_id INTEGER,
    defaultTransferFromAccount_id INTEGER,
    defaultTransferToAccount_id INTEGER,
    defaultCurrencyCode TEXT NOT NULL,
    sort INTEGER,
    FOREIGN KEY (group_id) REFERENCES t_user_group (id),
    FOREIGN KEY (defaultExpenseAccount_id) REFERENCES t_user_account (id),
    FOREIGN KEY (defaultIncomeAccount_id) REFERENCES t_user_account (id),
    FOREIGN KEY (defaultTransferFromAccount_id) REFERENCES t_user_account (id),
    FOREIGN KEY (defaultTransferToAccount_id) REFERENCES t_user_account (id)
);

-- Account Table
CREATE TABLE IF NOT EXISTS t_user_account (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    group_id INTEGER,
    type TEXT NOT NULL,
    notes TEXT,
    enable INTEGER NOT NULL,
    no TEXT,
    balance REAL NOT NULL,
    include INTEGER NOT NULL,
    currencyCode TEXT NOT NULL,
    initialBalance REAL,
    creditLimit REAL,
    FOREIGN KEY (group_id) REFERENCES t_user_group (id)
);

-- Category Table
CREATE TABLE IF NOT EXISTS t_user_category (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    book_id INTEGER,
    type TEXT NOT NULL,
    parent_id INTEGER,
    enable INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES t_user_book (id),
    FOREIGN KEY (parent_id) REFERENCES t_user_category (id)
);

-- Payee Table
CREATE TABLE IF NOT EXISTS t_user_payee (
    id INTEGER PRIMARY KEY,
    name TEXT,
    book_id INTEGER,
    enable INTEGER,
    FOREIGN KEY (book_id) REFERENCES t_user_book (id)
);

-- Tag Table
CREATE TABLE IF NOT EXISTS t_tag (
    id INTEGER PRIMARY KEY,
    name TEXT,
    book_id INTEGER,
    enable INTEGER,
    FOREIGN KEY (book_id) REFERENCES t_user_book (id)
);

-- Balance Flow Table
CREATE TABLE IF NOT EXISTS t_user_balance_flow (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    type TEXT,
    amount REAL,
    convertedAmount REAL,
    account_id INTEGER,
    to_account_id INTEGER,
    createTime INTEGER,
    title TEXT,
    notes TEXT,
    creator_id INTEGER,
    group_id INTEGER,
    payee_id INTEGER,
    confirm INTEGER,
    include INTEGER,
    insertAt INTEGER,
    FOREIGN KEY (book_id) REFERENCES t_user_book (id),
    FOREIGN KEY (account_id) REFERENCES t_user_account (id),
    FOREIGN KEY (to_account_id) REFERENCES t_user_account (id),
    FOREIGN KEY (creator_id) REFERENCES t_user (id),
    FOREIGN KEY (group_id) REFERENCES t_user_group (id),
    FOREIGN KEY (payee_id) REFERENCES t_user_payee (id)
);

-- Category Relation Table
CREATE TABLE IF NOT EXISTS t_category_relation (
    id INTEGER PRIMARY KEY,
    flow_id INTEGER,
    category_id INTEGER,
    amount REAL,
    convertedAmount REAL,
    FOREIGN KEY (flow_id) REFERENCES t_user_balance_flow (id),
    FOREIGN KEY (category_id) REFERENCES t_user_category (id)
);

-- Tag Relation Table
CREATE TABLE IF NOT EXISTS t_tag_relation (
    id INTEGER PRIMARY KEY,
    flow_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (flow_id) REFERENCES t_user_balance_flow (id),
    FOREIGN KEY (tag_id) REFERENCES t_tag (id)
);

-- Flow File Table
CREATE TABLE IF NOT EXISTS t_flow_file (
    id INTEGER PRIMARY KEY,
    data BLOB,
    creator_id INTEGER,
    flow_id INTEGER,
    createTime INTEGER,
    contentType TEXT,
    size INTEGER,
    originalName TEXT,
    FOREIGN KEY (creator_id) REFERENCES t_user (id),
    FOREIGN KEY (flow_id) REFERENCES t_user_balance_flow (id)
);
"""


def create_database():
    """Creates the SQLite database and tables based on the schema."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.executescript(SQL_SCHEMA)
        conn.commit()
        print(f"Database '{DB_NAME}' created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    create_database()
