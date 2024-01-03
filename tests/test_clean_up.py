import pandas as pd
import pytest

from src.clean_up import data_clean_up

# Test IDs for parametrization
happy_path_ids = ["minimal_data", "full_data", "extra_columns"]

edge_case_ids = ["empty_data", "single_row", "single_column"]

error_case_ids = ["non_dict_input", "non_json_serializable_input", "empty_dict"]

# Happy path test values
happy_path_values = [
    ({"name": ["Alice"], "age": [30]}, pd.DataFrame({"name": ["Alice"], "age": [30]})),
    (
        {
            "id": [1],
            "name": ["Bob"],
            "age": [25],
            "avatar": ["url"],
            "gender": ["M"],
            "employment": ["Unemployed"],
            "credit_card": ["1234-5678-9101-1121"],
            "subscription": ["none"],
        },
        pd.DataFrame({"name": ["Bob"], "age": [25]}),
    ),
    (
        {
            "id": [2],
            "name": ["Charlie"],
            "age": [40],
            "avatar": ["url"],
            "gender": ["M"],
            "employment": ["Employed"],
            "credit_card": ["2345-6789-1011-1213"],
            "subscription": ["premium"],
            "extra_column": ["extra_value"],
        },
        pd.DataFrame(
            {"name": ["Charlie"], "age": [40], "extra_column": ["extra_value"]}
        ),
    ),
]

# Edge case test values
edge_case_values = [
    ({}, pd.DataFrame()),
    ({"name": ["Dave"]}, pd.DataFrame({"name": ["Dave"]})),
    ({"name": ["Eve", "Frank"]}, pd.DataFrame({"name": ["Eve", "Frank"]})),
]

# Error case test values
error_case_values = [
    ("not_a_dict", TypeError),
    ([{"name": "Alice", "age": 30}], TypeError),
    ({}, TypeError),
]


@pytest.mark.parametrize("input_data,expected", happy_path_values, ids=happy_path_ids)
def test_happy_path(input_data, expected):
    # Act
    result = data_clean_up(input_data)

    # Assert
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize("input_data,expected", edge_case_values, ids=edge_case_ids)
def test_edge_cases(input_data, expected):
    # Act
    result = data_clean_up(input_data)

    # Assert
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "input_data,expected_exception", error_case_values, ids=error_case_ids
)
def test_error_cases(input_data, expected_exception):
    # Act & Assert
    with pytest.raises(expected_exception):
        data_clean_up(input_data)
