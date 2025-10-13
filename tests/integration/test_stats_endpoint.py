import sqlite3
import pytest
from datetime import date
from fastapi.testclient import TestClient
from app.main import app
from app.db import DB_PATH

client = TestClient(app)


@pytest.mark.integration
def test_stats_endpoint_read_only():
    """Test that /stats endpoint returns current counts without incrementing."""
    # Backup current database state
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT total_visits, today_visits, last_updated "
        "FROM visit_stats WHERE id = 1"
    )
    original_data = cursor.fetchone()
    conn.close()

    try:
        # Set database to known state
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE visit_stats SET total_visits = 100, "
            "today_visits = 10, last_updated = ? WHERE id = 1",
            (date.today().isoformat(),)
        )
        conn.commit()
        conn.close()

        # Call /stats endpoint multiple times
        response1 = client.get("/stats")
        assert response1.status_code == 200
        data1 = response1.json()
        assert data1["total_visits"] == 100
        assert data1["today_visits"] == 10

        # Call again - counts should NOT change
        response2 = client.get("/stats")
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["total_visits"] == 100  # Should not increment
        assert data2["today_visits"] == 10   # Should not increment

    finally:
        # Restore original database state
        if original_data:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE visit_stats SET total_visits = ?, "
                "today_visits = ?, last_updated = ? WHERE id = 1",
                original_data
            )
            conn.commit()
            conn.close()


@pytest.mark.integration
def test_visit_endpoint_increments():
    """Test that /visit endpoint increments counters and returns new counts."""
    # Backup current database state
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT total_visits, today_visits, last_updated "
        "FROM visit_stats WHERE id = 1"
    )
    original_data = cursor.fetchone()
    conn.close()

    try:
        # Set database to known state
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE visit_stats SET total_visits = 50, "
            "today_visits = 5, last_updated = ? WHERE id = 1",
            (date.today().isoformat(),)
        )
        conn.commit()
        conn.close()

        # Call /visit endpoint
        response = client.post("/visit")
        assert response.status_code == 200
        data = response.json()
        assert data["total_visits"] == 51
        assert data["today_visits"] == 6

        # Call again
        response = client.post("/visit")
        assert response.status_code == 200
        data = response.json()
        assert data["total_visits"] == 52
        assert data["today_visits"] == 7

        # Verify /stats shows the updated counts
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_visits"] == 52
        assert data["today_visits"] == 7

    finally:
        # Restore original database state
        if original_data:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE visit_stats SET total_visits = ?, "
                "today_visits = ?, last_updated = ? WHERE id = 1",
                original_data
            )
            conn.commit()
            conn.close()
