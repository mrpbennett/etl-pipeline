from unittest.mock import MagicMock

import pytest

from src.caching import add_user_to_redis


def test_add_user_to_redis(mocker):
    # Mock the Redis client
    redis_mock = mocker.MagicMock()
    mocker.patch("caching.redis", redis_mock)

    # Input data
    user_data = [
        {
            "uid": "123",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "social_insurance_number": "123-45-6789",
            "date_of_birth": "1990-01-01",
        }
    ]
    user_address_data = [
        {
            "uid": "123",
            "city": "New York",
            "street_name": "Broadway",
            "street_address": "123",
            "zip_code": "10001",
            "state": "NY",
            "country": "USA",
        }
    ]

    # Call the function
    add_user_to_redis(user_data, user_address_data)

    # Assert that the Redis client methods were called correctly
    redis_mock.hset.assert_called_once_with(
        "123",
        mapping={
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "social_insurance_number": "123-45-6789",
            "date_of_birth": "1990-01-01",
            "city": "New York",
            "street_name": "Broadway",
            "street_address": "123",
            "zip_code": "10001",
            "state": "NY",
            "country": "USA",
        },
    )
    redis_mock.expire.assert_called_once_with("123", 120)
    assert redis_mock.hset.call_count == 1
    assert redis_mock.expire.call_count == 1


def test_add_user_to_redis_empty_data(mocker):
    # Mock the Redis client
    redis_mock = mocker.MagicMock()
    mocker.patch("caching.redis", redis_mock)

    # Input data
    user_data = []
    user_address_data = []

    # Call the function
    add_user_to_redis(user_data, user_address_data)

    # Assert that the Redis client methods were not called
    assert redis_mock.hset.call_count == 0
    assert redis_mock.expire.call_count == 0


def test_add_user_to_redis_invalid_data(mocker):
    # Mock the Redis client
    redis_mock = mocker.MagicMock()
    mocker.patch("caching.redis", redis_mock)

    # Input data with missing uid
    user_data = [
        {
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "social_insurance_number": "123-45-6789",
            "date_of_birth": "1990-01-01",
        }
    ]
    user_address_data = [
        {
            "city": "New York",
            "street_name": "Broadway",
            "street_address": "123",
            "zip_code": "10001",
            "state": "NY",
            "country": "USA",
        }
    ]

    # Call the function and assert that it raises a ValueError
    with pytest.raises(ValueError):
        add_user_to_redis(user_data, user_address_data)
