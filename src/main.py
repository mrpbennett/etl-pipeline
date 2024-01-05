""" ETL Pipeline

A project to learn how to build a successful ETL pipeline.

Here data is pulled from an API this API holds random user data, the data contains 100
random users in a JSON format. 

The data is then validated, raises a ValueError if not. It is then cleaned via Pandas
removing unwanted columns. Using pandas is easier to drop cols from big datasets, the 
same DataFrame is then converted back into a JSON string.

The data is then extracted from the JSON string and any PII is hashed using a salt method.
Once data is extracted and hashed it's then stored inside two Postgres tables.

The same data is also passed to Redis for caching for quicker retrieval.

Order of module calls

1. get_data.py
2. validate.py
3. clean_up.py
4. extraction.py & salt.py
5. storage.py & caching.py

"""

import json
import logging
import time

import pandas as pd
import requests
from requests.exceptions import HTTPError, Timeout
from simple_chalk import blue, green, red, yellow

from salt import hash_pii
from storage import (
    add_user_to_redis,
    check_table_exists,
    create_address_table,
    create_user_table,
    insert_into_address_table,
    insert_into_user_table,
)
from validate import validate_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s:%(funcName)s -> %(message)s",
)

"""
EXTRACTION
"""


def get_user_data() -> dict:
    """Generate random user data from API call

    Calls a Random user generator API to collect data on 10 random users

    Returns:
        A JSON object of 100 random users

    Raises:
        HTTPError: if an HTTP error occurred
        Timeout: Encase a Timeout has occurred
    """
    try:
        # MAX requests is 100
        response = requests.get(
            "https://random-data-api.com/api/v2/users?size=10&response_type=json"
        )

        response.raise_for_status()

        data = {}

        if response.status_code == requests.codes.ok:
            data: dict = response.json()

        return data

    except (HTTPError, Timeout) as e:
        logging.warning(red(f"ERROR: {e}"))
        raise e


"""
TRANSFORM
"""


def data_clean_up(data: dict) -> pd.DataFrame:
    """Cleaning of JSON object

    Set up to drop unneeded columns from the created DataFrame

    Agrs:
        data: A JSON object

    Returns:
        Pandas DataFrame

    Raises:
        TypeError: If 'data' is not a dictionary or not convertible to a DataFrame.
    """

    try:
        df = pd.DataFrame(data)
        clean_up = df.drop(
            ["id", "avatar", "gender", "employment", "credit_card", "subscription"],
            axis=1,
        )

        logging.info(green("Data is now clean and ready for storage"))
        return clean_up
    except TypeError as e:
        logging.error(
            red(f"TypeError: The provided data is not in a valid format - {e}")
        )
        raise


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
            raise red(e) from e

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
            raise red(e) from e

    return address_data


def main():
    """
    Main function for processing daily data dumps.

    The function retrieves data from an API, validates and cleans the data, extracts relevant information,
    and inserts the data into relevant tables in Postgres and Redis for caching.
    The function runs in a loop, processing data dumps every 2 minutes.

    Returns:
        None
    """
    # Each loop will represent one daily data dump.
    max_count = 10
    # 24hrs = 2 mins- 10 days worth of data in 20 mins
    for _ in range(max_count):
        # Get Data from API. Max requests = 100
        data_to_be_process = get_user_data()

        # Validate Data - validate_json: returns True
        if validate_json(data_to_be_process):
            """
            Clean Data by removing certain cols using Pandas DataFrame returns pd.DataFrame
            that is then converted to JSON string for storage enabling extraction
            """

            json_data = json.loads(
                data_clean_up(data_to_be_process).to_json(orient="records")
            )

            """
            Now data has been retrieved, validated, cleaned and converted into JSON. 
            Now extract two objects of data to insert into relevant tables and Redis
            for caching.
            """

            # Extract user data and return a list of dicts
            user_data = extract_user_data_for_storage(json_data)

            # Extract users address data and return a list of dicts
            users_address_data = extract_address_data_for_storage(json_data)

            """
            LOAD - 
            
            Now data has been retrieved, validated and clean now insert into Redis
            for caching
            """

            add_user_to_redis(user_data, users_address_data)

            """
            INSERT data into Postgres tables users and users_address
            """

            if not check_table_exists("users") or not check_table_exists(
                "users_address"
            ):
                # IF tables do not exist create and add data
                if create_user_table():
                    logging.info(yellow("users table was created"))
                if create_address_table():
                    logging.info(yellow("users_address table was created"))

            for user in user_data:
                # Add user into Postgres for permanent storage
                if insert_into_user_table(user):
                    logging.info(
                        f"User: {blue(user['uid'])} added successfully into Postgres"
                    )

            for address in users_address_data:
                if insert_into_address_table(address):
                    logging.info(
                        f"User: {blue(address['uid'])} address has been added successfully into Postgres"
                    )
        time.sleep(120)  # Sleep for 2 minutes
        logging.info(yellow("Waiting for next batch of users to process..."))


if __name__ == "__main__":
    main()
