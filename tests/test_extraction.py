import pytest

from src.extaction import (
    extract_address_data_for_storage,
    extract_user_data_for_storage,
)
from src.salt import hash_pii


def test_extract_user_data_for_storage():
    data = {
        "uid": "1",
        "password": "password1",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "social_insurance_number": "123456789",
        "date_of_birth": "01-01-1990",
    }

    expected_output = {
        "uid": "1",
        "password": "password1",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "phone_number": "1234567890",
        "social_insurance_number": hash_pii("123456789"),
        "date_of_birth": "01-01-1990",
    }

    assert extract_user_data_for_storage(data) == expected_output


def test_extract_address_data_for_storage():
    data = {
        "uid": "1",
        "address": {
            "city": "New York",
            "street_name": "Broadway",
            "street_address": "123 Broadway",
            "zip_code": "10007",
            "state": "NY",
            "country": "USA",
        },
    }

    expected_output = {
        "uid": "1",
        "city": "New York",
        "street_name": "Broadway",
        "street_address": "123 Broadway",
        "zip_code": "10007",
        "state": "NY",
        "country": "USA",
    }

    assert extract_address_data_for_storage(data) == expected_output
