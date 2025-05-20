import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path("cache.db")
CACHE_LIFETIME_DAYS = 14

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Створення таблиці
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seen_messages (
            channel TEXT,
            message_id INTEGER,
            seen_at TEXT,
            PRIMARY KEY (channel, message_id)
        )
    """)

    # Очистка старих записів
    cutoff = datetime.utcnow() - timedelta(days=CACHE_LIFETIME_DAYS)
    cursor.execute("DELETE FROM seen_messages WHERE seen_at < ?", (cutoff.isoformat(),))

    conn.commit()
    conn.close()

def is_seen(channel: str, message_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM seen_messages WHERE channel = ? AND message_id = ?", (channel, message_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_seen(channel: str, message_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        now = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT OR REPLACE INTO seen_messages (channel, message_id, seen_at)
            VALUES (?, ?, ?)
        """, (channel, message_id, now))
        conn.commit()
    except sqlite3.Error as e:
        print(f"DB error: {e}")
    finally:
        conn.close()