from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError, Timeout

from src.get_data import get_user_data

# Constants for test cases
VALID_RESPONSE = {"users": [{"name": "John Doe"}, {"name": "Jane Doe"}]}
VALID_STATUS_CODE = 200
INVALID_STATUS_CODE = 500

# Test cases for parametrization
test_cases = [
    # Happy path tests with various realistic test values
    ("happy-path-valid-data", VALID_RESPONSE, VALID_STATUS_CODE, None),
    # Edge cases
    ("edge-case-empty-list", {"users": []}, VALID_STATUS_CODE, None),
    # Error cases
    (
        "error-case-http-error",
        {},
        INVALID_STATUS_CODE,
        HTTPError("HTTP Error occurred"),
    ),
    ("error-case-timeout", {}, VALID_STATUS_CODE, Timeout("Timeout occurred")),
]


@pytest.mark.parametrize(
    "test_id, expected_response, status_code, side_effect", test_cases
)
def test_get_user_data(test_id, expected_response, status_code, side_effect):
    with patch("requests.get") as mock_get:
        # Arrange
        mock_response = mock_get.return_value
        mock_response.json.return_value = expected_response
        mock_response.status_code = status_code
        mock_response.raise_for_status.side_effect = side_effect

        # sourcery skip: no-conditionals-in-tests
        if side_effect is None:
            # Act
            result = get_user_data()

            # Assert
            assert result == expected_response, f"Test Failed: {test_id}"
        else:
            # Act and Assert
            with pytest.raises(type(side_effect)) as exc_info:
                get_user_data()
            assert str(exc_info.value) == str(side_effect), f"Test Failed: {test_id}"
