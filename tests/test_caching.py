from unittest.mock import MagicMock, patch

import pytest
import redis

from src.caching import get_user_from_redis

# Constants for test cases
EXISTING_KEY = "existing_user"
NON_EXISTING_KEY = "non_existing_user"
USER_DATA = {"name": "John", "age": "30"}

# Mock Redis client
mock_redis_client = MagicMock()

# Test cases for non-empty output
test_cases_non_empty = [
    ("happy_path_existing", EXISTING_KEY, USER_DATA),
]

# Test cases for empty output
test_cases_empty = [
    ("happy_path_empty", NON_EXISTING_KEY, {}),
    ("edge_case_empty_key", "", {}),
]

# Test cases with RedisError
test_cases_error = [
    ("error_case_redis_error", EXISTING_KEY, redis.RedisError),
]


@pytest.mark.parametrize("test_id, key, expected_output", test_cases_non_empty)
def test_get_user_from_redis_non_empty_output(test_id, key, expected_output):
    with patch("caching.redis", mock_redis_client):
        # Arrange
        mock_redis_client.exists.return_value = True
        mock_redis_client.hgetall.return_value = expected_output

        # Act
        result = get_user_from_redis(key)

        # Assert
        assert result == expected_output
        mock_redis_client.hgetall.assert_called_once_with(key)


@pytest.mark.parametrize("test_id, key, expected_output", test_cases_empty)
def test_get_user_from_redis_empty_output(test_id, key, expected_output):
    with patch("caching.redis", mock_redis_client):
        # Arrange
        mock_redis_client.exists.return_value = False
        mock_redis_client.hgetall.return_value = expected_output

        # Act
        result = get_user_from_redis(key)

        # Assert
        assert result == expected_output
        mock_redis_client.exists.assert_called_once_with(key)
        assert not mock_redis_client.hgetall.called


@pytest.mark.parametrize("test_id, key, exception", test_cases_error)
def test_get_user_from_redis_with_error(test_id, key, exception):
    with patch("caching.redis", mock_redis_client):
        # Arrange
        mock_redis_client.exists.side_effect = exception
        mock_redis_client.hgetall.side_effect = exception

        # Act & Assert
        with pytest.raises(redis.RedisError):
            get_user_from_redis(key)
