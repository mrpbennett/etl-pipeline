""" Data Retrieval and Serialization """
import json
import logging

import psycopg2
import tomli
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from caching import get_user_from_redis

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(message)s",
)

with open("config.toml", "rb") as f:
    c = tomli.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the Frontend
app.mount("/static", StaticFiles(directory="./static/dist"), name="static")


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
                    SELECT uid FROM users ORDER BY ts DESC;
                    """
                )
                user_list = curs.fetchall()

                return user_list

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

                    postgres = curs.fetchall()

                    return postgres

        except psycopg2.Error as e:
            return {"message": str(e)}
    else:
        return redis
