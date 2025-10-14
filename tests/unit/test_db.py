import pytest
from datetime import date, timedelta
from src.db import increment_visits
from unittest.mock import Mock, patch

DB_PATH = "data/stats.db"


@pytest.fixture
def mock_db():
    # Mock the sqlite3 connection and cursor
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor

    # Mock the database response for fetching stats
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    today = date.today().isoformat()
    mock_cursor.fetchone.return_value = (10, 5, yesterday)

    return mock_conn, mock_cursor, today


@pytest.mark.unit
def test_increment_visits(mock_db):
    mock_conn, mock_cursor, today = mock_db

    # Patch the sqlite3.connect method to use the mock connection
    with patch("sqlite3.connect", return_value=mock_conn):
        stats = increment_visits()

    # Assert that the stats were incremented correctly
    assert stats["total_visits"] == 11, "Total visits should increment by 1"
    assert stats["today_visits"] == 1, \
        "Today's visits should reset and increment to 1"

    # Verify that the last_updated value was changed to today
    expected_query = (
        "UPDATE visit_stats SET total_visits = ?, "
        "today_visits = ?, last_updated = ? WHERE id = 1"
    )
    expected_params = (11, 1, today)

    # Normalize queries to ignore formatting differences
    def normalize_query(query):
        return " ".join(query.split())

    executed_queries = [
        (
            normalize_query(call[0][0]),
            call[0][1] if len(call[0]) > 1 else None
        )
        for call in mock_cursor.execute.call_args_list
    ]

    matching_query = any(
        normalize_query(expected_query) == query and
        expected_params == params
        for query, params in executed_queries
    )

    assert matching_query, (
        f"Expected query '{expected_query}' with params "
        f"{expected_params} not found in executed queries: "
        f"{executed_queries}"
    )

    # Verify that the connection was committed
    mock_conn.commit.assert_called_once()


@pytest.mark.unit
def test_increment_visits_atomicity(mock_db):
    mock_conn, mock_cursor, today = mock_db

    # Patch the sqlite3.connect method to use the mock connection
    with patch("sqlite3.connect", return_value=mock_conn):
        # Simulate a failure during the transaction
        def fail_on_update(*args, **kwargs):
            if "UPDATE visit_stats" in args[0]:
                raise Exception("Simulated failure")

        mock_cursor.execute.side_effect = fail_on_update

        # Fetch initial stats with yesterday's date
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        initial_stats = (10, 5, yesterday)
        mock_cursor.fetchone.return_value = initial_stats

        # Attempt to increment visits and expect failure
        with pytest.raises(Exception, match="Simulated failure"):
            increment_visits()

        # Verify that no changes were committed
        mock_conn.commit.assert_not_called()
        mock_conn.rollback.assert_called_once()

        # Ensure the database state remains unchanged
        mock_cursor.execute.assert_any_call(
            "SELECT total_visits, today_visits, last_updated FROM visit_stats WHERE id = 1"
        )
        assert mock_cursor.fetchone.return_value == initial_stats, (
            "Database state should remain unchanged after failure"
        )


@pytest.mark.unit
def test_persistence_across_restarts(mock_db):
    mock_conn, mock_cursor, today = mock_db

    # Patch the sqlite3.connect method to use the mock connection
    with patch("sqlite3.connect", return_value=mock_conn):
        # Initial stats
        initial_stats = (10, 5, today)
        mock_cursor.fetchone.return_value = initial_stats

        # Simulate first increment
        stats = increment_visits()
        assert stats["total_visits"] == 11
        assert stats["today_visits"] == 6

        # Simulate application restart by resetting the mock
        mock_cursor.reset_mock()
        mock_conn.reset_mock()

        # Simulate fetching the same data after restart
        mock_cursor.fetchone.return_value = (11, 6, today)

        # Simulate second increment after restart
        stats = increment_visits()
        assert stats["total_visits"] == 12
        assert stats["today_visits"] == 7

        # Verify that the database retains state across restarts
        mock_cursor.execute.assert_any_call(
            "SELECT total_visits, today_visits, last_updated "
            "FROM visit_stats WHERE id = 1"
        )
        mock_conn.commit.assert_called()
