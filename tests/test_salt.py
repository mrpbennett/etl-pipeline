import pytest

from src.salt import hash_pii

# Test IDs for parametrization
HAPPY_PATH_ID = "happy_path"
EDGE_CASE_ID = "edge_case"
ERROR_CASE_ID = "error_case"

# Happy path test values
happy_path_values = [
    ("JohnDoe", f"{HAPPY_PATH_ID}_normal"),
    ("JaneDoe123", f"{HAPPY_PATH_ID}_with_numbers"),
    ("John_Doe@example.com", f"{HAPPY_PATH_ID}_email_format"),
    ("1234567890", f"{HAPPY_PATH_ID}_numeric"),
    ("!@#$%^&*()_+", f"{HAPPY_PATH_ID}_special_chars"),
]

# Edge case test values
edge_case_values = [
    ("a", f"{EDGE_CASE_ID}_single_char"),
    (" " * 10, f"{EDGE_CASE_ID}_whitespace"),
    ("John\nDoe", f"{EDGE_CASE_ID}_newline_in_string"),
    ("JohnDoe" * 1000, f"{EDGE_CASE_ID}_long_string"),
]

# Error case test values
error_case_values = [
    (123, f"{ERROR_CASE_ID}_non_string"),
    (None, f"{ERROR_CASE_ID}_none"),
    ("", f"{ERROR_CASE_ID}_empty_string"),
    ([], f"{ERROR_CASE_ID}_empty_list"),
    ({}, f"{ERROR_CASE_ID}_empty_dict"),
]


@pytest.mark.parametrize("pii, test_id", happy_path_values)
def test_hash_pii_happy_path(pii, test_id):
    # Act
    result = hash_pii(pii)

    # Assert
    assert isinstance(result, str), f"{test_id}: Result should be a string"
    assert result.isdigit(), f"{test_id}: Result should only contain digits"
    assert len(result) > 0, f"{test_id}: Result should not be empty"


@pytest.mark.parametrize("pii, test_id", edge_case_values)
def test_hash_pii_edge_cases(pii, test_id):
    # Act
    result = hash_pii(pii)

    # Assert
    assert isinstance(result, str), f"{test_id}: Result should be a string"
    assert result.isdigit(), f"{test_id}: Result should only contain digits"
    assert len(result) > 0, f"{test_id}: Result should not be empty"


@pytest.mark.parametrize("pii, test_id", error_case_values)
def test_hash_pii_error_cases(pii, test_id):
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        hash_pii(pii)
    assert "Invalid input" in str(
        exc_info.value
    ), f"{test_id}: ValueError should contain 'Invalid input'"
