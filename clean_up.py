""" Data clean up

Function using Pandas to clean up the JSON data and drop cols from the created DataFrame

Typical usage example:

    data_clean_up is passed the JSON object
"""

import logging

import pandas as pd
import tomli
from simple_chalk import green, red

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(filename)s - %(module)s  %(message)s",
)

with open("config.toml", "rb") as f:
    c = tomli.load(f)


def data_clean_up(data: dict) -> pd.DataFrame:
    """Cleaning of JSON object

    Set up to drop unrequired columns from the created DataFrame

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
