""" Data Validation.

Validates each key in the JSON generated from get_data.py before allowing the 
cleaning of data. 

Typical usage:
    a single call to validate_json() is only require this function will validate the 
    JSON objected pulled from get_data.py

    if validate_json():
        do something...
"""

import re
from typing import Literal
from uuid import UUID


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def is_valid_email(email: str):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)


def is_valid_url(url: str):
    pattern = (
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    return re.match(pattern, url)


def is_valid_date(date_text: str):
    pattern = r"\d{4}-\d{2}-\d{2}"
    return re.match(pattern, date_text)


def validate_json(data: dict) -> Literal[True]:
    """Validates passed JSON object

    Validates the JSON object passed to it before it can be cleaned

    Agrs:
        data: JSON dict

    Returns:
        Literal True if all validation methods have passed

    Raises:
        ValueError: if incorrect types are found
    """
    for entry in data:
        if not isinstance(entry.get("id"), int):
            raise ValueError("Invalid 'id': must be an integer.")
        if not is_valid_uuid(entry.get("uid")):
            raise ValueError("Invalid 'uid': must be a valid UUID.")
        if any(
            not isinstance(entry.get(key), str)
            for key in [
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
        ):
            raise ValueError(
                "One or more fields are invalid: all specified fields must be strings."
            )
        if not is_valid_email(entry.get("email")):
            raise ValueError("Invalid 'email': must be in a valid email format.")
        if not is_valid_url(entry.get("avatar")):
            raise ValueError("Invalid 'avatar': must be a valid URL.")
        if not is_valid_date(entry.get("date_of_birth")):
            raise ValueError("Invalid 'date_of_birth': must be in 'YYYY-MM-DD' format.")
        if any(
            key not in entry.get("address", {})
            or not isinstance(entry["address"].get(key), str)
            for key in [
                "city",
                "street_name",
                "street_address",
                "zip_code",
                "state",
                "country",
            ]
        ):
            raise ValueError("Invalid 'address': missing or invalid fields.")
        if any(
            key not in entry.get("address", {}).get("coordinates", {})
            or not isinstance(entry["address"]["coordinates"].get(key), float)
            for key in ["lat", "lng"]
        ):
            raise ValueError(
                "Invalid 'coordinates': 'lat' and 'lng' must be present and be floats."
            )
        if not isinstance(entry.get("credit_card", {}).get("cc_number"), str):
            raise ValueError("Invalid 'credit card number': must be a string.")

        # Validate Employment
        if not isinstance(entry.get("employment"), dict):
            raise ValueError("Invalid 'employment': must be an object.")
        for key in ["title", "key_skill"]:
            if key not in entry["employment"] or not isinstance(
                entry["employment"][key], str
            ):
                raise ValueError(f"Invalid 'employment': missing or invalid '{key}'.")

        # Validate Subscription
        if not isinstance(entry.get("subscription"), dict):
            raise ValueError("Invalid 'subscription': must be an object.")
        for key in ["plan", "status", "payment_method", "term"]:
            if key not in entry["subscription"] or not isinstance(
                entry["subscription"][key], str
            ):
                raise ValueError(f"Invalid 'subscription': missing or invalid '{key}'.")

        # Validate Address
        if not isinstance(entry.get("address"), dict):
            raise ValueError("Invalid 'address': must be an object.")
        for key in [
            "city",
            "street_name",
            "street_address",
            "zip_code",
            "state",
            "country",
        ]:
            if key not in entry["address"] or not isinstance(
                entry["address"][key], str
            ):
                raise ValueError(f"Invalid 'address': missing or invalid '{key}'.")
        if not isinstance(entry["address"].get("coordinates"), dict):
            raise ValueError("Invalid 'coordinates': must be an object.")
        for key in ["lat", "lng"]:
            if key not in entry["address"]["coordinates"] or not isinstance(
                entry["address"]["coordinates"][key], float
            ):
                raise ValueError(f"Invalid 'coordinates': missing or invalid '{key}'.")

        # Validate Credit Card
        if not isinstance(entry.get("credit_card"), dict):
            raise ValueError("Invalid 'credit card': must be an object.")
        if "cc_number" not in entry["credit_card"] or not isinstance(
            entry["credit_card"]["cc_number"], str
        ):
            raise ValueError("Invalid 'credit card': missing or invalid 'cc_number'.")

    return True
