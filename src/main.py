"""
This module represents an ETL (Extract, Transform, Load) pipeline for processing daily data dumps.
The pipeline retrieves data from an API, validates and cleans the data, extracts relevant information,
and inserts the data into relevant tables in Postgres and Redis for caching.

The main function runs in a loop, processing data dumps every 2 minutes. Each loop represents one daily data dump.
The maximum number of data dumps to process is defined by the 'max_count' variable.

The pipeline consists of the following steps:
1. Extraction:
    - The 'get_user_data' function makes an API call to a random user generator API and retrieves data on 10 random users.
    - If the API call is successful, the data is returned as a JSON object.

2. Transformation:
    - The 'data_clean_up' function takes the JSON object and cleans it by dropping unneeded columns using Pandas DataFrame.
    - The cleaned data is then converted back to a JSON string for storage.
    - The 'extract_user_data_for_storage' function extracts relevant user data from the cleaned JSON object and returns a list of user dictionaries.
    - The 'extract_address_data_for_storage' function extracts relevant address data from the cleaned JSON object and returns a list of address dictionaries.

3. Load:
    - The extracted user data and address data are stored in Redis for caching using the 'add_user_to_redis' function.
    - If the 'users' and 'users_address' tables do not exist in Postgres, they are created using the 'create_user_table' and 'create_address_table' functions.
    - The user data is inserted into the 'users' table using the 'insert_into_user_table' function.
    - The address data is inserted into the 'users_address' table using the 'insert_into_address_table' function.

The main function runs the ETL pipeline in a loop, processing data dumps every 2 minutes.
After each data dump is processed, the program sleeps for 2 minutes before processing the next data dump.

Note: This module requires the 'requests', 'pandas', 'simple_chalk', 'salt', and 'storage' modules to be imported.

Author: Paul Bennett
Date: 2024-01-05
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

# Rest of the code...
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


def main() -> None:
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
