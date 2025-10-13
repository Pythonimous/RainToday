"""
Integration test for visit counter persistence across application restarts.

This test verifies that the SQLite database correctly persists visitor
counts when the application is stopped and restarted.
"""
import sqlite3
import pytest
from datetime import date
from app.db import increment_visits, DB_PATH


@pytest.mark.integration
def test_database_persistence_across_restarts():
    """
    Verify that visit counts persist in SQLite across simulated restarts.

    This test simulates application restarts by closing and reopening
    database connections, ensuring data persists on disk.
    """
    # Setup: Initialize a fresh database for this test
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Backup original state
    cursor.execute(
        "SELECT total_visits, today_visits, last_updated "
        "FROM visit_stats WHERE id = 1"
    )
    original_state = cursor.fetchone()
    conn.close()

    try:
        # Reset to known state
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE visit_stats SET total_visits = 100, "
            "today_visits = 10, last_updated = ? WHERE id = 1",
            (date.today().isoformat(),)
        )
        conn.commit()
        conn.close()

        # Simulate application restart: close all connections
        # (In real scenario, the app would stop here)

        # Simulate first visit after restart
        stats = increment_visits()
        assert stats["total_visits"] == 101
        assert stats["today_visits"] == 11

        # Simulate another application restart
        # Read directly from database to verify persistence
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT total_visits, today_visits FROM visit_stats WHERE id = 1"
        )
        persisted_total, persisted_today = cursor.fetchone()
        conn.close()

        # Verify data persisted correctly
        assert persisted_total == 101, \
            "Total visits should persist at 101 after restart"
        assert persisted_today == 11, \
            "Today visits should persist at 11 after restart"

        # Simulate another visit after second restart
        stats = increment_visits()
        assert stats["total_visits"] == 102
        assert stats["today_visits"] == 12

        # Final verification: ensure data is written to disk
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT total_visits, today_visits FROM visit_stats WHERE id = 1"
        )
        final_total, final_today = cursor.fetchone()
        conn.close()

        assert final_total == 102, \
            "Total visits should persist at 102 after multiple restarts"
        assert final_today == 12, \
            "Today visits should persist at 12 after multiple restarts"

    finally:
        # Restore original state
        if original_state:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE visit_stats SET total_visits = ?, "
                "today_visits = ?, last_updated = ? WHERE id = 1",
                original_state
            )
            conn.commit()
            conn.close()


@pytest.mark.integration
def test_database_survives_date_rollover():
    """
    Verify that today's visits reset when the date changes,
    while total visits continue to increment.
    """
    from datetime import timedelta

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Backup original state
    cursor.execute(
        "SELECT total_visits, today_visits, last_updated "
        "FROM visit_stats WHERE id = 1"
    )
    original_state = cursor.fetchone()
    conn.close()

    try:
        # Set to yesterday with some counts
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE visit_stats SET total_visits = 200, "
            "today_visits = 50, last_updated = ? WHERE id = 1",
            (yesterday,)
        )
        conn.commit()
        conn.close()

        # Increment visits (should detect date change)
        stats = increment_visits()

        # Total should increment, but today should reset to 1
        assert stats["total_visits"] == 201, \
            "Total visits should continue incrementing"
        assert stats["today_visits"] == 1, \
            "Today visits should reset to 1 on new day"

        # Verify persistence after date rollover
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT total_visits, today_visits, last_updated "
            "FROM visit_stats WHERE id = 1"
        )
        total, today, last_updated = cursor.fetchone()
        conn.close()

        assert total == 201
        assert today == 1
        assert last_updated == date.today().isoformat(), \
            "Date should update to today"

    finally:
        # Restore original state
        if original_state:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE visit_stats SET total_visits = ?, "
                "today_visits = ?, last_updated = ? WHERE id = 1",
                original_state
            )
            conn.commit()
            conn.close()
