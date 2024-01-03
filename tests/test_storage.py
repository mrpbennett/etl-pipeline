from unittest.mock import MagicMock, patch

import pytest

from src.storage import create_user_table

# Constants for test readability
HAPPY_PATH_ID = "happy_path"
ERROR_CASE_ID = "error_case"


@pytest.mark.parametrize(
    "test_case_id",
    [
        (HAPPY_PATH_ID),
        (ERROR_CASE_ID),
    ],
)
def test_create_user_table(test_case_id):
    # Arrange
    mock_connect = MagicMock()
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_cursor_context = MagicMock()
    mock_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor_context
    mock_cursor_context.__enter__.return_value = mock_cursor

    # sourcery skip: no-conditionals-in-tests
    if test_case_id == ERROR_CASE_ID:
        mock_connect.side_effect = Exception("Connection failed")

    with patch("storage.psycopg2.connect", mock_connect):
        if test_case_id == HAPPY_PATH_ID:
            # Act
            result = create_user_table()

            # Assert
            assert result is True
            mock_connect.assert_called_once()
            mock_cursor.execute.assert_called_once()
            mock_connection.commit.assert_called_once()
        elif test_case_id == ERROR_CASE_ID:
            # Act & Assert
            with pytest.raises(Exception, match="Connection failed"):
                create_user_table()
            mock_connect.assert_called_once()
            mock_cursor.execute.assert_not_called()
            mock_connection.commit.assert_not_called()
