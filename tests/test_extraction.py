import pytest

from src.extraction import (
    extract_address_data_for_storage,
    extract_user_data_for_storage,
)
from src.salt import hash_pii


# Test cases for extract_user_data_for_storage
@pytest.mark.parametrize(
    "input_data, expected_output, test_id",
    [
        # Happy path tests
        (
            [
                {
                    "uid": 1,
                    "password": "pass123",
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "johndoe",
                    "email": "john@example.com",
                    "phone_number": "1234567890",
                    "social_insurance_number": "123456789",
                    "date_of_birth": "1990-01-01",
                }
            ],
            [
                {
                    "uid": 1,
                    "password": "pass123",
                    "first_name": "John",
                    "last_name": "Doe",
                    "username": "johndoe",
                    "email": "john@example.com",
                    "phone_number": "1234567890",
                    "social_insurance_number": hash_pii("123456789"),
                    "date_of_birth": "1990-01-01",
                }
            ],
            "happy_path_complete_data",
        ),
        (
            [{"uid": 2}],
            [
                {
                    "uid": 2,
                    "password": "n/a",
                    "first_name": "n/a",
                    "last_name": "n/a",
                    "username": "n/a",
                    "email": "n/a",
                    "phone_number": "n/a",
                    "social_insurance_number": hash_pii("n/a"),
                    "date_of_birth": "n/a",
                }
            ],
            "happy_path_minimum_data",
        ),
        # Edge cases
        (
            [{"uid": 3, "social_insurance_number": None}],
            [
                {
                    "uid": 3,
                    "password": "n/a",
                    "first_name": "n/a",
                    "last_name": "n/a",
                    "username": "n/a",
                    "email": "n/a",
                    "phone_number": "n/a",
                    "social_insurance_number": hash_pii("n/a"),
                    "date_of_birth": "n/a",
                }
            ],
            "edge_case_null_sin",
        ),
        # Error cases
        ([None], pytest.raises(TypeError), "error_case_none_input"),
        ("not a dict", pytest.raises(TypeError), "error_case_wrong_type"),
    ],
)
def test_extract_user_data_for_storage(input_data, expected_output, test_id):
    # Act
    if isinstance(expected_output, pytest.raises):
        with expected_output:
            extract_user_data_for_storage(input_data)
    else:
        result = extract_user_data_for_storage(input_data)
        # Assert
        assert result == expected_output, f"Failed test_id: {test_id}"


# Test cases for extract_address_data_for_storage
@pytest.mark.parametrize(
    "input_data, expected_output, test_id",
    [
        # Happy path tests
        (
            [
                {
                    "uid": 1,
                    "address": {
                        "city": "New York",
                        "street_name": "5th Ave",
                        "street_address": "711",
                        "zip_code": "10010",
                        "state": "NY",
                        "country": "USA",
                    },
                }
            ],
            [
                {
                    "uid": 1,
                    "city": "New York",
                    "street_name": "5th Ave",
                    "street_address": "711",
                    "zip_code": "10010",
                    "state": "NY",
                    "country": "USA",
                }
            ],
            "happy_path_complete_address",
        ),
        (
            [{"uid": 2}],
            [
                {
                    "uid": 2,
                    "city": "n/a",
                    "street_name": "n/a",
                    "street_address": "n/a",
                    "zip_code": "n/a",
                    "state": "n/a",
                    "country": "n/a",
                }
            ],
            "happy_path_minimum_address",
        ),
        # Edge cases
        (
            [{"uid": 3, "address": {}}],
            [
                {
                    "uid": 3,
                    "city": "n/a",
                    "street_name": "n/a",
                    "street_address": "n/a",
                    "zip_code": "n/a",
                    "state": "n/a",
                    "country": "n/a",
                }
            ],
            "edge_case_empty_address_dict",
        ),
        # Error cases
        ([None], pytest.raises(TypeError), "error_case_none_input"),
        ("not a dict", pytest.raises(TypeError), "error_case_wrong_type"),
    ],
)
def test_extract_address_data_for_storage(input_data, expected_output, test_id):
    # Act
    # sourcery skip: no-conditionals-in-tests
    if isinstance(expected_output, pytest.raises):
        with expected_output:
            extract_address_data_for_storage(input_data)
    else:
        result = extract_address_data_for_storage(input_data)
        # Assert
        assert result == expected_output, f"Failed test_id: {test_id}"
