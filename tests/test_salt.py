import pytest

from src.salt import hash_pii


def test_hash_pii_valid_input():
    # Input data
    pii = "JohnDoe123"

    # Call the function
    result = hash_pii(pii)

    # Assert that the result is a non-empty string
    assert isinstance(result, str)
    assert result != ""


def test_hash_pii_empty_input():
    # Input data
    pii = ""

    # Call the function and assert that it raises a ValueError
    with pytest.raises(ValueError):
        hash_pii(pii)


def test_hash_pii_invalid_input():
    # Input data
    pii = 12345

    # Call the function and assert that it raises a ValueError
    with pytest.raises(ValueError):
        hash_pii(pii)
