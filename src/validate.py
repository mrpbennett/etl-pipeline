"""
This module provides functions for validating various data fields and structures.

The functions in this module can be used to validate UUIDs, email addresses, URLs,
dates, and other data types. It also includes functions for validating basic fields
in an entry, address details, coordinates, employment details, subscription details,
and credit card details.

The main function in this module is `validate_json`, which takes a JSON object as input
and performs validation on the different fields and structures within the object.

By using the functions in this module, you can ensure that the data you are working with
meets the required format and is valid, helping to maintain data integrity and consistency
in your application.
"""
import re
from typing import Literal
from uuid import UUID


def is_valid_uuid(uuid_to_test, version=4):
    """Check if a UUID is valid.

    Args:
        uuid_to_test: The UUID to be tested.
        version: The UUID version to validate against. Defaults to 4.

    Returns:
        True if the UUID is valid and matches the specified version; False otherwise.
    """
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def is_valid_email(email: str):
    """Check if an email address is valid.

    Args:
        email: The email address to be checked.

    Returns:
        A match object if the email address matches the pattern; None otherwise.
    """
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)


def is_valid_url(url: str):
    """Check if a URL is valid.

    Args:
        url: The URL to be checked.

    Returns:
        A match object if the URL matches the pattern; None otherwise.
    """
    pattern = (
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    return re.match(pattern, url)


def is_valid_date(date_text: str):
    """Check if a date string is in the 'YYYY-MM-DD' format.

    Args:
        date_text: The date string to be checked.

    Returns:
        A match object if the date string matches the format; None otherwise.
    """
    pattern = r"\d{4}-\d{2}-\d{2}"
    return re.match(pattern, date_text)


def validate_basic_fields(entry: dict):
    """Validate basic fields in an entry.

    Args:
        entry: A dictionary representing an entry.

    Raises:
        ValueError: If any of the basic fields are missing or invalid.
    """
    required_fields = [
        "uid",
        "password",
        "first_name",
        "last_name",
        "username",
        "email",
        "avatar",
        "gender",
        "phone_number",
        "social_insurance_number",
        "date_of_birth",
    ]
    for field in required_fields:
        if field not in entry or not isinstance(entry[field], str):
            raise ValueError(f"Invalid '{field}': must be a string.")

    if not is_valid_uuid(entry["uid"]):
        raise ValueError("Invalid 'uid': must be a valid UUID.")
    if not is_valid_email(entry["email"]):
        raise ValueError("Invalid 'email': must be in a valid email format.")
    if not is_valid_url(entry["avatar"]):
        raise ValueError("Invalid 'avatar': must be a valid URL.")
    if not is_valid_date(entry["date_of_birth"]):
        raise ValueError("Invalid 'date_of_birth': must be in 'YYYY-MM-DD' format.")


def validate_address(address: dict):
    """Validate address details.

    Args:
        address: A dictionary containing address details.

    Raises:
        ValueError: If the address details are missing or invalid.
    """
    if not address:
        raise ValueError("Address is missing.")

    address_fields = [
        "city",
        "street_name",
        "street_address",
        "zip_code",
        "state",
        "country",
    ]
    for field in address_fields:
        if field not in address or not isinstance(address[field], str):
            raise ValueError(f"Invalid address '{field}': must be a string.")


def validate_coordinates(coordinates: dict):
    """Validate coordinates.

    Args:
        coordinates: A dictionary containing latitude and longitude.

    Raises:
        ValueError: If
    """
    if not coordinates:
        raise ValueError("Coordinates are missing.")

    for key in ["lat", "lng"]:
        if key not in coordinates or not isinstance(coordinates[key], float):
            raise ValueError(f"Invalid coordinates '{key}': must be a float.")


def validate_employment(employment: dict):
    """Validate employment details.

    Args:
        employment: A dictionary containing employment details.

    Raises:
        ValueError: If the employment details are missing or invalid.
    """
    if not employment:
        raise ValueError("Employment details are missing.")

    for key in ["title", "key_skill"]:
        if key not in employment or not isinstance(employment[key], str):
            raise ValueError(f"Invalid employment '{key}': must be a string.")


def validate_subscription(subscription: dict):
    """Validate subscription details.

    Args:
        subscription: A dictionary containing subscription details.

    Raises:
        ValueError: If the subscription details are missing or invalid.
    """
    if not subscription:
        raise ValueError("Subscription details are missing.")

    for key in ["plan", "status", "payment_method", "term"]:
        if key not in subscription or not isinstance(subscription[key], str):
            raise ValueError(f"Invalid subscription '{key}': must be a string.")


def validate_credit_card(credit_card: dict):
    """
    Validate credit card details.

    Args:
        credit_card: A dictionary containing credit card details.

    Raises:
        ValueError: If the credit card details are missing or invalid.
    """
    if not credit_card:
        raise ValueError("Credit card details are missing.")

    if "cc_number" not in credit_card or not isinstance(credit_card["cc_number"], str):
        raise ValueError("Invalid credit card: missing or invalid 'cc_number'.")


def validate_json(data: dict) -> Literal[True]:
    """Validates passed JSON object.

    Args:
        data: JSON dict.

    Returns:
        Literal True if all validation methods have passed.

    Raises:
        ValueError: if incorrect types are found.
    """
    for entry in data:
        validate_basic_fields(entry)
        validate_address(entry.get("address", {}))
        validate_coordinates(entry.get("address", {}).get("coordinates", {}))
        validate_employment(entry.get("employment", {}))
        validate_subscription(entry.get("subscription", {}))
        validate_credit_card(entry.get("credit_card", {}))

    return True
