""" Caching Layer """
import logging

import redis
import tomli
from simple_chalk import red

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(message)s",
)

with open("config.toml", "rb") as f:
    c = tomli.load(f)


# REDIS connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
