import unittest
from unittest.mock import patch, MagicMock
from src.app.utils.db_utils import get_summaries, get_available_fields
from psycopg.sql import SQL, Identifier

def normalize_sql(sql):
    """Normalize SQL for consistent comparison by removing extra spaces."""
    return " ".join(str(sql).split())  # Split on whitespace and join with single spaces

class TestDatabaseOperations(unittest.TestCase):

    @patch("src.app.utils.db_utils.pool")
    def test_get_summaries(self, mock_pool):
        # Mock the connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_pool.connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Set up the mock cursor to return specific data
        mock_cursor.description = [("hex_id",), ("field1",), ("field2",)]
        mock_cursor.fetchall.return_value = [("hex_1", 100, 200)]

        fields = ["field1", "field2"]
        h3_ids = ["hex_1"]
        rows, colnames = get_summaries(fields, h3_ids)

        # Assert that the connection pool was used
        mock_pool.connection.assert_called_once()

        expected_sql_query = SQL(
            """
            SELECT {0}
            FROM {1}
            WHERE hex_id = ANY (%s)
            """
        ).format(
            SQL(", ").join([Identifier(c) for c in ["hex_id"] + fields]),
            Identifier("space2stats"),
        )

        actual_sql_query, actual_params = mock_cursor.execute.call_args[0]

        assert normalize_sql(expected_sql_query) == normalize_sql(actual_sql_query), "SQL query does not match"
        assert actual_params == [h3_ids], "Query parameters do not match"

        assert rows == [("hex_1", 100, 200)]
        assert colnames == ["hex_id", "field1", "field2"]

    @patch("src.app.utils.db_utils.pool")
    def test_get_available_fields(self, mock_pool):
        # Mock the connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_pool.connection.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        # Set up the mock cursor to return specific data
        mock_cursor.fetchall.return_value = [("field1",), ("field2",), ("field3",)]
        columns = get_available_fields()

        # Assert that the connection pool was used
        mock_pool.connection.assert_called_once()

        expected_sql_query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s
        """

        actual_sql_query, actual_params = mock_cursor.execute.call_args[0]

        assert normalize_sql(expected_sql_query) == normalize_sql(actual_sql_query), "SQL query does not match"
        assert actual_params == ["space2stats"], "Query parameters do not match"

        assert columns == ["field1", "field2", "field3"]

if __name__ == "__main__":
    unittest.main()