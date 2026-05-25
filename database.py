import sqlite3
from datetime import datetime

DATABASE_NAME = "cuan_tracker.db"


def get_connection():
    # Membuat koneksi ke database SQLite.
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Membuat tabel users dan transactions jika belum ada.
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        pin_hash TEXT NOT NULL,
        device_id TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_key TEXT NOT NULL,
        created_by_user_id INTEGER NOT NULL,
        created_by_username TEXT NOT NULL,
        transaction_type TEXT NOT NULL,
        category TEXT NOT NULL,
        amount INTEGER NOT NULL,
        transaction_date TEXT NOT NULL,
        department TEXT NOT NULL,
        payment_method TEXT NOT NULL,
        reference_number TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (created_by_user_id) REFERENCES users(user_id)
    );
    """)

    conn.commit()
    conn.close()


def get_current_timestamp():
    # Menghasilkan timestamp dalam format string.
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
