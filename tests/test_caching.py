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

# Test cases
test_cases = [
    # Happy path tests with various realistic test values
    ("happy_path_existing", EXISTING_KEY, USER_DATA, None),
    ("happy_path_empty", NON_EXISTING_KEY, {}, None),
    # Edge cases
    ("edge_case_empty_key", "", {}, None),
    # Error cases
    ("error_case_redis_error", EXISTING_KEY, {}, redis.RedisError),
]


@pytest.mark.parametrize("test_id, key, expected_output, side_effect", test_cases)
def test_get_user_from_redis(test_id, key, expected_output, side_effect):
    with patch("caching.redis", mock_redis_client):
        # Arrange
        mock_redis_client.exists.return_value = bool(expected_output)
        mock_redis_client.hgetall.return_value = expected_output
        # sourcery skip: no-conditionals-in-tests
        if side_effect:
            mock_redis_client.exists.side_effect = side_effect
            mock_redis_client.hgetall.side_effect = side_effect

            with pytest.raises(redis.RedisError):
                result = get_user_from_redis(key)
        else:
            result = get_user_from_redis(key)

        # Assert
        if not side_effect:
            assert result == expected_output
            if expected_output:
                mock_redis_client.hgetall.assert_called_once_with(key)
            else:
                mock_redis_client.exists.assert_called_once_with(key)
                assert not mock_redis_client.hgetall.called
