import sqlite3
from datetime import date
from typing import Dict

DB_PATH = "data/stats.db"


def _get_connection() -> sqlite3.Connection:
    """
    Create a database connection with optimal settings for concurrency.

    - WAL mode allows concurrent reads during writes
    - Short timeout (1s) fails fast instead of blocking
    - Each connection is short-lived (closed after each operation)
    """
    conn = sqlite3.connect(DB_PATH, timeout=1.0)
    conn.execute("PRAGMA busy_timeout = 1000")
    return conn


def init_db() -> None:
    """Initialize database schema with WAL mode for concurrency."""
    conn = _get_connection()
    # WAL mode is critical for concurrent access
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visit_stats (
            id INTEGER PRIMARY KEY,
            total_visits INTEGER NOT NULL,
            today_visits INTEGER NOT NULL,
            last_updated DATE NOT NULL
        )
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO visit_stats (id, total_visits, today_visits, last_updated)
        VALUES (1, 0, 0, ?)
    """, (date.today().isoformat(),))
    conn.commit()
    conn.close()


def increment_visits() -> Dict[str, int]:
    """
    Increment visit counters atomically using a single SQL statement.

    Key optimizations:
    - Single UPDATE statement with CASE for date rollover
    - No separate SELECT before UPDATE (eliminates race window)
    - WAL mode allows concurrent reads
    - SQLite busy_timeout handles lock contention automatically
    """
    today = date.today().isoformat()
    conn = _get_connection()

    try:
        cursor = conn.cursor()

        # Atomic increment with conditional date rollover in one statement
        # This eliminates the race condition between read and write
        cursor.execute(
            """
            UPDATE visit_stats
            SET total_visits = total_visits + 1,
                today_visits = CASE
                    WHEN last_updated = ? THEN today_visits + 1
                    ELSE 1
                END,
                last_updated = ?
            WHERE id = 1
            """,
            (today, today)
        )

        # Fetch the updated values
        cursor.execute(
            "SELECT total_visits, today_visits FROM visit_stats WHERE id = 1"
        )
        result = cursor.fetchone()

        conn.commit()
        return {"total_visits": result[0], "today_visits": result[1]}
    finally:
        conn.close()
