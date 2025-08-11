import sqlite3
from config import DB_NAME


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute(
        """
      CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT CHECK(status IN ('to_read', 'reading', 'read')) NOT NULL
);
    """
    )
    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (date('now')),
    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE
);
    """
    )

    conn.commit()
    conn.close()
