import pytest
from fastapi.testclient import TestClient

from src.api import app

client = TestClient(app)


# Happy path test with various realistic test values
@pytest.mark.parametrize(
    "expected_status, expected_response",
    [
        (200, {"message": "I am Root"}),  # Test ID: HP-1
    ],
)
def test_root_happy_path(expected_status, expected_response):
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == expected_status
    assert response.json() == expected_response


# Edge cases are not applicable here as the endpoint does not take any input or query parameters.

# Error cases are also not applicable in this context since the endpoint is static and does not involve any error handling.
