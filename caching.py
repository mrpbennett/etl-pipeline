""" Caching into Redis

Combine the two extracted lists of JSON objects and cache inside Redis

Typical usage example:

    add_user_to_redis() pass the two lists as arguments
"""
import logging

import redis
import tomli
from redis import RedisError
from simple_chalk import blue, red

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(message)s",
)

with open("config.toml", "rb") as f:
    c = tomli.load(f)


# REDIS connection
redis = redis.Redis(host="localhost", port=6379, decode_responses=True)


def add_user_to_redis(user_data: list, user_address_data: list) -> None:
    """Add user to Redis for caching

    Combine the user and users address data into one dictonary to cache into Redis
    under the same uid. A TTL of 2mins is also set to each key to keep the Redis cache
    as fresh as possible.

    Agrs:
        user_data: A list of a JSON dicts
        users_address_data: A list of JSON dicts

    Returns:
        Nothing

    Raises:
        ValueError: If any values are incorrect
    """
    try:
        for ud, uad in zip(user_data, user_address_data):
            uid: str = ud.get("uid")
            users_data: dict = {
                "password": ud.get("password", "n/a"),
                "first_name": ud.get("first_name", "n/a"),
                "last_name": ud.get("last_name", "n/a"),
                "username": ud.get("username", "n/a"),
                "email": ud.get("email", "n/a"),
                "phone_number": ud.get("phone_number", "n/a"),
                "social_insurance_number": ud.get("social_insurance_number", "n/a"),
                "date_of_birth": ud.get("date_of_birth", "n/a"),
            }

            address_data: dict = {
                "city": uad.get("city", "n/a"),
                "street_name": uad.get("street_name", "n/a"),
                "street_address": uad.get("street_address", "n/a"),
                "zip_code": uad.get("zip_code", "n/a"),
                "state": uad.get("state", "n/a"),
                "country": uad.get("country", "n/a"),
            }

            full_user_data: dict = {**users_data, **address_data}

            # Add user to Redis
            redis.hset(uid, mapping=full_user_data)

            # Set TTL in Redis for 2 min
            redis.expire(uid, 120)

        logging.info(
            f"{red(len(user_data))} Users have been cached in Redis, with a TTL of {red("2 mins")}."
        )

    except ValueError as e:
        raise e


def get_user_from_redis(key: str) -> dict:
    """
    Retrieve user data from Redis based on the given key.

    Args:
        key (str): The key to look up in Redis.

    Returns:
        dict: The user data if the key exists; otherwise, an empty dictionary.

    Raises:
        redis.RedisError: If there's an error in executing the Redis command.
    """
    try:
        data = {}

        # TODO: Set TTL to 5mins

        if redis.exists(key):
            data: dict = redis.hgetall(key)
        else:
            logging.error(f"Key {red(key)} not found in Redis. Trying Postgres...")

        return data

    except RedisError as e:
        logging.error(f"General Redis error: {e}")
        raise e
