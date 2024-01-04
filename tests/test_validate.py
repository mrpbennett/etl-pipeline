from src.validate import validate_basic_fields


def test_validate_basic_fields_success():
    # Input data
    entry = {
        "uid": "123e4567-e89b-12d3-a456-426614174000",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "avatar": "https://example.com/avatar.jpg",
        "gender": "male",
        "phone_number": "1234567890",
        "social_insurance_number": "123-45-6789",
        "date_of_birth": "1990-01-01",
    }

    # Call the function
    validate_basic_fields(entry)


def test_validate_basic_fields_missing_field():
    # Input data with a missing field
    entry = {
        "uid": "123e4567-e89b-12d3-a456-426614174000",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "avatar": "https://example.com/avatar.jpg",
        "gender": "male",
        "phone_number": "1234567890",
        "social_insurance_number": "123-45-6789",
        # Missing 'date_of_birth' field
    }

    # Call the function and assert that it raises a ValueError
    try:
        validate_basic_fields(entry)
        assert False, "Expected ValueError to be raised."
    except ValueError as e:
        assert str(e) == "Invalid 'date_of_birth': must be in 'YYYY-MM-DD' format."


def test_validate_basic_fields_invalid_field():
    # Input data with an invalid field
    entry = {
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "avatar": "https://example.com/avatar.jpg",
        "gender": "male",
        "phone_number": "1234567890",
        "social_insurance_number": "123-45-6789",
        "date_of_birth": "1990-01-01",
        "uid": "invalid-uuid",
    }

    # Call the function and assert that it raises a ValueError
    try:
        validate_basic_fields(entry)
        assert False, "Expected ValueError to be raised."
    except ValueError as e:
        assert str(e) == "Invalid 'uid': must be a valid UUID."


# Add more test cases as needed
