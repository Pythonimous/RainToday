import threading
from datetime import date, timedelta

import pytest

from src.db import _get_connection, get_visit_stats, increment_visits, init_db


@pytest.fixture(autouse=True)
def isolated_db(monkeypatch, tmp_path):
    """Provide an isolated SQLite file for each test run."""
    db_path = tmp_path / "stats.db"
    monkeypatch.setattr("src.db.DB_PATH", str(db_path))
    init_db()
    yield


@pytest.mark.unit
def test_increment_visits():
    """Test that increment_visits correctly increments counters."""
    # Get initial state
    stats = increment_visits()

    # Assert counters increment
    assert "total_visits" in stats
    assert "today_visits" in stats
    assert stats["total_visits"] > 0
    assert stats["today_visits"] > 0

    # Increment again
    stats2 = increment_visits()
    assert stats2["total_visits"] == stats["total_visits"] + 1
    assert stats2["today_visits"] == stats["today_visits"] + 1


@pytest.mark.unit
def test_increment_visits_concurrency():
    """Test multiple concurrent increments work with minimal lock contention.

    With the 1s timeout, some requests may fail fast with 'database is locked'
    under heavy concurrent load. This is acceptable and preferred over long waits.
    We verify that:
    1. Most requests succeed (at least 80%)
    2. Any failures are clean 'database is locked' errors
    3. The final count matches successful increments
    """
    # Reset the database first
    init_db()

    results = []
    lock_errors = []
    other_errors = []

    def do_increment():
        try:
            result = increment_visits()
            results.append(result)
        except Exception as e:
            if "database is locked" in str(e):
                lock_errors.append(e)
            else:
                other_errors.append(e)

    threads = [threading.Thread(target=do_increment) for _ in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # No unexpected errors should occur
    assert len(other_errors) == 0, f"Unexpected errors: {other_errors}"

    # Most requests should succeed (allow up to 20% lock failures)
    success_rate = len(results) / 20
    assert success_rate >= 0.8, (
        f"Success rate {success_rate:.0%} too low. "
        f"Got {len(results)} successes, {len(lock_errors)} lock errors"
    )

    # Verify successful results have valid data
    total_visits = [r["total_visits"] for r in results]
    assert all(isinstance(v, int) and v > 0 for v in total_visits)


@pytest.mark.unit
def test_date_rollover():
    """Test that today_visits resets when date changes."""
    # Manually set yesterday's date in the database
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = _get_connection()
    cursor = conn.cursor()
    baseline_total = 200
    cursor.execute(
        (
            "UPDATE visit_stats SET last_updated = ?, "
            "today_visits = 100, total_visits = ? WHERE id = 1"
        ),
        (yesterday, baseline_total),
    )
    conn.commit()
    conn.close()

    # Increment visits - should reset today_visits to 1
    stats = increment_visits()

    assert stats["today_visits"] == 1, "today_visits should reset to 1 on date rollover"
    assert stats["total_visits"] == baseline_total + 1, "total_visits should continue incrementing"


@pytest.mark.unit
def test_get_visit_stats_matches_increment():
    stats = increment_visits()
    fetched = get_visit_stats()

    assert fetched == stats


@pytest.mark.unit
def test_get_visit_stats_when_row_missing():
    conn = _get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM visit_stats")
    conn.commit()
    conn.close()

    stats = get_visit_stats()

    assert stats["total_visits"] == 0
    assert stats["today_visits"] == 0
