import pandas as pd
import pytest

from src.clean_up import data_clean_up


def test_data_clean_up_valid_data():
    # Input data
    data = {
        "id": [1, 2, 3],
        "name": ["John", "Jane", "Alice"],
        "age": [25, 30, 35],
        "city": ["New York", "London", "Paris"],
    }

    # Expected output
    expected_output = pd.DataFrame(
        {
            "name": ["John", "Jane", "Alice"],
            "age": [25, 30, 35],
            "city": ["New York", "London", "Paris"],
        }
    )

    # Call the function
    result = data_clean_up(data)

    # Assert the result
    assert result.equals(expected_output)


def test_data_clean_up_empty_data():
    # Input data
    data = {}

    # Call the function
    result = data_clean_up(data)

    # Assert that the result is an empty DataFrame
    assert result.empty


def test_data_clean_up_invalid_data():
    # Input data with invalid format (not a dictionary)
    data = "invalid_data"

    # Call the function and assert that it raises a TypeError
    with pytest.raises(TypeError):
        data_clean_up(data)
