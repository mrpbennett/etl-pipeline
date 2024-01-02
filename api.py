""" Data Retrieval and Serialization """

import logging

import psycopg2
import tomli
from fastapi import FastAPI

from caching import get_user_from_redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(message)s",
)

app = FastAPI()

with open("config.toml", "rb") as f:
    c = tomli.load(f)


@app.get("/")
async def root():
    return {"message": "I am Root"}


@app.get("/api/datapipe/list-users")
async def list_users():
    try:
        with psycopg2.connect(**c["db"]) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    SELECT uid FROM users;
                    """
                )
                result = curs.fetchall()

                return {"postgres_data": result}

    except psycopg2.Error as e:
        return {"message": str(e)}


@app.get("/api/datapipe/{user_id}")
async def get_user(user_id: str):
    # Check length of Redis first before checking Postgres
    redis = get_user_from_redis(user_id)

    if len(redis) == 0:
        try:
            with psycopg2.connect(**c["db"]) as conn:
                with conn.cursor() as curs:
                    curs.execute(
                        """
                        SELECT
                            users.uid,
                            first_name,
                            last_name,
                            username,
                            email,
                            phone_number,
                            social_insurance_number,
                            date_of_birth,
                            city,
                            street_name,
                            street_address,
                            zip_code,
                            state,
                            country
                        FROM users
                        JOIN users_address UA ON users.uid = UA.uid
                        WHERE users.uid = %s;
                        """,
                        (user_id,),
                    )
                    result = curs.fetchall()

                    return {"postgres_data": result}

        except psycopg2.Error as e:
            return {"message": str(e)}
    else:
        return {"redis_data": redis}
