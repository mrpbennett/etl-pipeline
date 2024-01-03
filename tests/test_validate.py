import pytest

from src.validate import is_valid_uuid


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "uuid_to_test, version, expected",
    [
        # UUID version 4 tests
        ("123e4567-e89b-12d3-a456-426614174000", 4, True, "happy-uuidv4-valid"),
        ("00000000-0000-4000-8000-000000000000", 4, True, "happy-uuidv4-min"),
        ("ffffffff-ffff-4fff-bfff-ffffffffffff", 4, True, "happy-uuidv4-max"),
        # UUID version 1 tests
        ("2d6f8c1c-8d2f-11eb-8dcd-0242ac130003", 1, True, "happy-uuidv1-valid"),
        # UUID version 5 tests
        ("fdda765f-fc57-5604-a269-52a7df8164ec", 5, True, "happy-uuidv5-valid"),
    ],
)
def test_is_valid_uuid_happy_path(uuid_to_test, version, expected):
    # Act
    result = is_valid_uuid(uuid_to_test, version)

    # Assert
    assert result == expected, f"Test failed for UUID: {uuid_to_test}"


# Edge case tests
@pytest.mark.parametrize(
    "uuid_to_test, version, expected",
    [
        # UUID with all zeros should fail for version 4
        ("00000000-0000-0000-0000-000000000000", 4, False, "edge-uuidv4-all-zeros"),
        # UUID with invalid version number
        ("123e4567-e89b-12d3-a456-426614174000", 5, False, "edge-uuidv4-wrong-version"),
        # UUID with uppercase letters
        ("123E4567-E89B-12D3-A456-426614174000", 4, True, "edge-uuidv4-uppercase"),
    ],
)
def test_is_valid_uuid_edge_cases(uuid_to_test, version, expected):
    # Act
    result = is_valid_uuid(uuid_to_test, version)

    # Assert
    assert result == expected, f"Test failed for UUID: {uuid_to_test}"


# Error case tests
@pytest.mark.parametrize(
    "uuid_to_test, version, expected",
    [
        # Invalid UUID format
        ("invalid-uuid-format", 4, False, "error-invalid-format"),
        # Incorrect UUID version
        ("123e4567-e89b-12d3-a456-426614174000", 3, False, "error-incorrect-version"),
        # Non-string input
        (123, 4, False, "error-non-string-input"),
        # None input
        (None, 4, False, "error-none-input"),
        # Empty string
        ("", 4, False, "error-empty-string"),
    ],
)
def test_is_valid_uuid_error_cases(uuid_to_test, version, expected):
    # Act
    result = is_valid_uuid(uuid_to_test, version)

    # Assert
    assert result == expected, f"Test failed for UUID: {uuid_to_test}"
