import logging

from simple_chalk import green, red, yellow

from salt import hash_pii


def extract_user_data_for_storage(data: dict) -> list:
    """
    Extract users data to place inside another table

    Returns
        List of user dicts
    """

    user_data = []

    for u in data:
        try:
            user = {
                "uid": u["uid"],
                "password": u.get("password", "n/a"),
                "first_name": u.get("first_name", "n/a"),
                "last_name": u.get("last_name", "n/a"),
                "username": u.get("username", "n/a"),
                "email": u.get("email", "n/a"),
                "phone_number": u.get("phone_number", "n/a"),
                "social_insurance_number": hash_pii(
                    u.get("social_insurance_number", "n/a")
                ),
                "date_of_birth": u.get("date_of_birth", "n/a"),
            }

            user_data.append(user)

        except TypeError as e:
            # Handle incorrect data types
            logging.error(red(f"Type error: {e}"))
            raise red(e)

    return user_data


def extract_address_data_for_storage(data: dict) -> list:
    """
    Extract users address to place inside another table

    Returns
        List of users address dicts
    """
    address_data = []

    for a in data:
        try:
            address = {
                "uid": a.get("uid", "n/a"),
                "city": a.get("address", {}).get("city", "n/a"),
                "street_name": a.get("address", {}).get("street_name", "n/a"),
                "street_address": a.get("address", {}).get("street_address", "n/a"),
                "zip_code": a.get("address", {}).get("zip_code", "n/a"),
                "state": a.get("address", {}).get("state", "n/a"),
                "country": a.get("address", {}).get("country", "n/a"),
            }

            address_data.append(address)

        except TypeError as e:
            # Handle incorrect data types
            logging.error(red(f"Type error: {e}"))
            raise red(e)

    return address_data
