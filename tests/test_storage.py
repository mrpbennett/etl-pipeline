from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.storage import insert_into_user_table


@patch("psycopg2.connect")
def test_insert_into_user_table_success(mock_connect):
    # Mock the psycopg2 connection and cursor
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor

    # Input data
    user_data = {
        "uid": 1,
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "social_insurance_number": "123-45-6789",
        "date_of_birth": "1990-01-01",
    }

    # Call the function
    result = insert_into_user_table(user_data)

    # Assert that the psycopg2 connect method is called with the correct parameters
    mock_connect.assert_called_once_with(
        dbname="postgres", user="postgres", password="password", host="localhost"
    )

    # Assert that the psycopg2 cursor method is called
    mock_connect.return_value.__enter__.return_value.cursor.assert_called_once()

    # Assert that the execute method is called with the correct SQL query and parameters
    mock_cursor.execute.assert_called_once_with(
        """
            INSERT INTO users (
                uid, password, first_name, last_name, username, email, phone_number, social_insurance_number, date_of_birth, ts
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
        """,
        (
            user_data["uid"],
            user_data["password"],
            user_data["first_name"],
            user_data["last_name"],
            user_data["username"],
            user_data["email"],
            user_data["phone_number"],
            user_data["social_insurance_number"],
            user_data["date_of_birth"],
            int(datetime.timestamp(datetime.now())),
        ),
    )

    # Assert that the function returns True
    assert result is True


@patch("psycopg2.connect")
def test_insert_into_user_table_exception(mock_connect):
    # Mock the psycopg2 connection and cursor
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor

    # Mock an exception during execution
    mock_cursor.execute.side_effect = Exception("Database error")

    # Input data
    user_data = {
        "uid": 1,
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "social_insurance_number": "123-45-6789",
        "date_of_birth": "1990-01-01",
    }

    # Call the function
    result = insert_into_user_table(user_data)

    # Assert that the psycopg2 connect method is called with the correct parameters
    mock_connect.assert_called_once_with(
        dbname="postgres", user="postgres", password="password", host="localhost"
    )

    # Assert that the psycopg2 cursor method is called
    mock_connect.return_value.__enter__.return_value.cursor.assert_called_once()

    # Assert that the execute method is called with the correct SQL query and parameters
    mock_cursor.execute.assert_called_once_with(
        """
            INSERT INTO users (
                uid, password, first_name, last_name, username, email, phone_number, social_insurance_number, date_of_birth, ts
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            );
        """,
        (
            user_data["uid"],
            user_data["password"],
            user_data["first_name"],
            user_data["last_name"],
            user_data["username"],
            user_data["email"],
            user_data["phone_number"],
            user_data["social_insurance_number"],
            user_data["date_of_birth"],
            int(datetime.timestamp(datetime.now())),
        ),
    )

    # Assert that the function returns True
    assert result is True
