import hashlib
import logging
import random
import string
import struct

import pytest

from src.extraction import extract_user_data_for_storage


def hash_pii(pii: str) -> str:
    if not isinstance(pii, str) or not pii:
        raise ValueError("Invalid input: PII must be a non-empty string.")

    hash_object = hashlib.sha512(
        (pii + "".join(random.choices(string.ascii_letters, k=30))).encode("ascii")
    ).digest()
    number = struct.unpack(">Q", b"\x00" + hash_object[:7])[0]
    return str(number)


def test_extract_user_data_for_storage():
    # Test case 1: Valid input data
    data = [
        {
            "uid": "123",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "social_insurance_number": "123456789",
            "date_of_birth": "1990-01-01",
        },
        {
            "uid": "456",
            "password": "password456",
            "first_name": "Jane",
            "last_name": "Smith",
            "username": "janesmith",
            "email": "janesmith@example.com",
            "phone_number": "9876543210",
            "social_insurance_number": "987654321",
            "date_of_birth": "1995-05-05",
        },
    ]

    expected_output = [
        {
            "uid": "123",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "social_insurance_number": hash_pii("123456789"),
            "date_of_birth": "1990-01-01",
        },
        {
            "uid": "456",
            "password": "password456",
            "first_name": "Jane",
            "last_name": "Smith",
            "username": "janesmith",
            "email": "janesmith@example.com",
            "phone_number": "9876543210",
            "social_insurance_number": hash_pii("987654321"),
            "date_of_birth": "1995-05-05",
        },
    ]

    assert extract_user_data_for_storage(data) == expected_output

    # Test case 2: Empty input data
    data = []
    expected_output = []
    data = [
        {
            "uid": "123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
        },
        {
            "uid": "456",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "janesmith@example.com",
        },
    ]

    expected_output = [
        {
            "uid": "123",
            "password": "n/a",
            "first_name": "John",
            "last_name": "Doe",
            "username": "n/a",
            "email": "johndoe@example.com",
            "phone_number": "n/a",
            "social_insurance_number": hash_pii("n/a"),
            "date_of_birth": "n/a",
        },
        {
            "uid": "456",
            "password": "n/a",
            "first_name": "Jane",
            "last_name": "Smith",
            "username": "n/a",
            "email": "janesmith@example.com",
            "phone_number": "n/a",
            "social_insurance_number": hash_pii("n/a"),
            "date_of_birth": "n/a",
        },
    ]

    assert extract_user_data_for_storage(data) == expected_output

    # Test case 3: Input data with missing fields
    data = [
        {
            "uid": "123",
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@example.com",
        },
        {
            "uid": "456",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "janesmith@example.com",
        },
    ]

    expected_output = [
        {
            "uid": "123",
            "password": "n/a",
            "first_name": "John",
            "last_name": "Doe",
            "username": "n/a",
            "email": "johndoe@example.com",
            "phone_number": "n/a",
            "social_insurance_number": hash_pii("n/a"),
            "date_of_birth": "n/a",
        },
        {
            "uid": "456",
            "password": "n/a",
            "first_name": "Jane",
            "last_name": "Smith",
            "username": "n/a",
            "email": "janesmith@example.com",
            "phone_number": "n/a",
            "social_insurance_number": hash_pii("n/a"),
            "date_of_birth": "n/a",
        },
    ]

    assert extract_user_data_for_storage(data) == expected_output

    # Test case 4: Input data with incorrect data types
    data = [
        {
            "uid": "123",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "phone_number": "1234567890",
            "social_insurance_number": "123456789",
            "date_of_birth": 1990,  # Incorrect data type
        },
    ]

    with pytest.raises(TypeError):
        extract_user_data_for_storage(data)
        assert logging.error.called
