""" Data retrieval from a Random API source

Gets a JSON object of 100 users via an Random user API generator

Typical usage example:

    Call get_user_data() to return JSON object
"""

import logging

import requests
from requests.exceptions import HTTPError, Timeout
from simple_chalk import red

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(message)s",
)


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
