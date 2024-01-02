""" ETL Pipeline

A project to learn how to build a successful ETL pipeline.

Here data is pulled from an API this API holds random user data, the data contains 100
random users in a JSON format. 

The data is then validated, raises a ValueError if not. It is then cleaned via Pandas
removing unwanted columns. Using pandas is easier to drop cols from big datasets, the 
same DataFrame is then converted back into a JSON string.

The data is then extracted from the JSON string and any PII is hashed using a salt method.
Once data is extracted and hashed it's then stored inside two Postgres tables.

The same data is also passed to Redis for caching for quicker retrival.
   
"""

import json
import logging

import tomli
from simple_chalk import blue, green, red, yellow

from clean_up import data_clean_up
from extaction import extract_address_data_for_storage, extract_user_data_for_storage
from get_data import get_user_data
from storage import (
    check_table_exists,
    create_address_table,
    create_user_table,
    insert_into_address_table,
    insert_into_user_table,
)
from validate import validate_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(message)s",
)

with open("config.toml", "rb") as f:
    c = tomli.load(f)


def main():
    # Get Data from API. Max requests = 100
    data_to_be_process = get_user_data()

    # Validate Data - validate_json: retuns True
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
        users_addresss_data = extract_address_data_for_storage(json_data)

        """
        Now data has been retrieved, validated and clean now INSERT data into Postgres
        tables users and users_address
        """

        # Check if users and users_addres tables exists already
        if check_table_exists("users") and check_table_exists("users_address"):
            for user in user_data:
                if insert_into_user_table(user):
                    logging.info(green(f"User: {user['uid']} added successfully"))

            for address in users_addresss_data:
                if insert_into_address_table(address):
                    logging.info(
                        green(f"Address for User: {address['uid']} added successfully")
                    )
        else:
            # IF tables do not exist create and add data
            if create_user_table():
                logging.info(blue("user table created"))
            if create_address_table():
                logging.info(blue("users_address table created"))

            for user in user_data:
                if insert_into_user_table(user):
                    logging.info(green(f"User: {user['uid']} added successfully"))

            for address in users_addresss_data:
                if insert_into_address_table(address):
                    logging.info(
                        green(f"Address for User: {address['uid']} added successfully")
                    )


if __name__ == "__main__":
    main()
