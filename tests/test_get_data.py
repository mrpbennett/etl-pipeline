import contextlib
from unittest.mock import patch

import requests

from src.get_data import get_user_data


@patch("get_data.requests.get")
def test_get_user_data_success(mock_get):
    # Mock the response from the API
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {"name": {"first": "John", "last": "Doe"}},
            {"name": {"first": "Jane", "last": "Smith"}},
            # ... other user data
        ]
    }

    # Call the function
    data = get_user_data()

    # Assert that the API was called with the correct URL
    mock_get.assert_called_once_with(
        "https://random-data-api.com/api/v2/users?size=10&response_type=json"
    )

    # Assert that the returned data matches the mocked response
    assert data == {
        "results": [
            {"name": {"first": "John", "last": "Doe"}},
            {"name": {"first": "Jane", "last": "Smith"}},
            # ... other user data
        ]
    }


@patch("get_data.requests.get")
def test_get_user_data_http_error(mock_get):
    # Mock an HTTP error response from the API
    mock_response = mock_get.return_value
    mock_response.status_code = 404

    # Call the function and assert that it raises an HTTPError
    try:
        get_user_data()
        assert False, "Expected HTTPError to be raised"
    except requests.HTTPError as e:
        assert str(e) == "404 Client Error: Not Found"

    # Assert that the API was called with the correct URL
    mock_get.assert_called_once_with(
        "https://random-data-api.com/api/v2/users?size=10&response_type=json"
    )


@patch("get_data.requests.get")
def test_get_user_data_timeout(mock_get):
    # Mock a timeout error from the API
    mock_get.side_effect = requests.Timeout

    # Call the function and assert that it raises a Timeout
    with contextlib.suppress(requests.Timeout):
        get_user_data()
        assert False, "Expected Timeout to be raised"
    # Assert that the API was called with the correct URL
    mock_get.assert_called_once_with(
        "https://random-data-api.com/api/v2/users?size=10&response_type=json"
    )
