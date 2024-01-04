import psycopg2
import pytest
from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


def test_get_user_from_redis():
    # Mock the get_user_from_redis function to return user information
    # from Redis
    def mock_get_user_from_redis(user_id):
        return {
            "uid": user_id,
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            # ... other user information
        }

    # Monkey patch the get_user_from_redis function
    app.get_user_from_redis = mock_get_user_from_redis

    # Send a GET request to the API endpoint
    response = client.get("/api/datapipe/123")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response body matches the user information from Redis
    assert response.json() == {
        "uid": "123",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        # ... other user information
    }


def test_get_user_from_database():
    # Mock the get_user_from_redis function to return an empty dictionary
    # indicating that the user is not found in Redis
    def mock_get_user_from_redis(user_id):
        return {}

    # Monkey patch the get_user_from_redis function
    app.get_user_from_redis = mock_get_user_from_redis

    # Send a GET request to the API endpoint
    response = client.get("/api/datapipe/123")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response body matches the user information from the database
    assert response.json() == [
        "123",
        "John",
        "Doe",
        "johndoe",
        "johndoe@example.com",
        # ... other user information
    ]


def test_get_user_error():
    # Mock the get_user_from_redis function to return an empty dictionary
    # indicating that the user is not found in Redis
    def mock_get_user_from_redis(user_id):
        return {}

    # Monkey patch the get_user_from_redis function
    app.get_user_from_redis = mock_get_user_from_redis

    # Mock the psycopg2.connect function to raise an error
    def mock_psycopg2_connect(*args, **kwargs):
        raise psycopg2.Error("Database connection error")

    # Monkey patch the psycopg2.connect function
    app.psycopg2.connect = mock_psycopg2_connect

    # Send a GET request to the API endpoint
    response = client.get("/api/datapipe/123")

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Assert that the response body contains the error message
    assert response.json() == {"message": "Database connection error"}
