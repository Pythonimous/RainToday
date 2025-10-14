import sqlite3
from datetime import date
from typing import Dict

DB_PATH = "data/stats.db"


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = date.today().isoformat()

    try:
        # Begin transaction
        conn.execute("BEGIN TRANSACTION")

        # Fetch current stats
        cursor.execute(
            "SELECT total_visits, today_visits, last_updated "
            "FROM visit_stats WHERE id = 1"
        )
        total_visits, today_visits, last_updated = cursor.fetchone()

        # Reset today's visits if the date has changed
        if last_updated != today:
            today_visits = 0

        # Increment counts
        total_visits += 1
        today_visits += 1

        # Update the database
        cursor.execute(
            """
            UPDATE visit_stats
            SET total_visits = ?, today_visits = ?, last_updated = ?
            WHERE id = 1
            """,
            (total_visits, today_visits, today)
        )

        # Commit transaction
        conn.commit()
    except Exception as e:
        # Rollback transaction on failure
        conn.rollback()
        raise e
    finally:
        conn.close()

    return {"total_visits": total_visits, "today_visits": today_visits}
