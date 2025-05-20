import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import threading

DB_PATH = Path("cache.db")
CACHE_LIFETIME_DAYS = 14
_db_lock = threading.Lock()

def init_db():
    with _db_lock:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS seen_messages (
                channel TEXT,
                message_id INTEGER,
                seen_at TEXT,
                PRIMARY KEY (channel, message_id)
            )
        """)

        cutoff = datetime.utcnow() - timedelta(days=CACHE_LIFETIME_DAYS)
        cursor.execute("DELETE FROM seen_messages WHERE seen_at < ?", (cutoff.isoformat(),))
        conn.commit()
        conn.close()

def is_seen(channel: str, message_id: int) -> bool:
    with _db_lock:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM seen_messages WHERE channel = ? AND message_id = ?", (channel, message_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None

def mark_seen(channel: str, message_id: int):
    with _db_lock:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        cursor = conn.cursor()
        now = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT OR REPLACE INTO seen_messages (channel, message_id, seen_at)
            VALUES (?, ?, ?)
        """, (channel, message_id, now))
        conn.commit()
        conn.close()