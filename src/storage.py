""" Storing data inside Postgres

Here we storage our user and user address data inside Postgres. There are two tables
one that stores user data with the users uid and another address table that stores the 
users address with the users uid. Allow the creation of relationships between the two
tables

Typical usage example:

        user_data = {}
        users_addresss_data = {}

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
"""
import logging
from datetime import datetime
from typing import Literal

import psycopg2
from simple_chalk import red

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - line:%(lineno)d - %(message)s",
)


def create_user_table() -> Literal[True]:
    """
    Create users table

    Returns:
        Literal True
    """
    try:
        with psycopg2.connect(
            dbname="postgres", user="postgres", password="password", host="postgres"
        ) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                        CREATE TABLE IF NOT EXISTS users
                            (
                                uid VARCHAR(255) PRIMARY KEY,
                                password VARCHAR(255),
                                first_name VARCHAR(255),
                                last_name VARCHAR(255),
                                username VARCHAR(255),
                                email VARCHAR(255),
                                phone_number VARCHAR(255),
                                social_insurance_number VARCHAR(255),
                                date_of_birth VARCHAR(255),
                                ts INT
                            );
                    """
                )

    except Exception as e:
        logging.error(red(e))

    return True


def create_address_table() -> Literal[True]:
    """
    Create users_address table

    Returns:
        Literal True
    """
    try:
        with psycopg2.connect(
            dbname="postgres", user="postgres", password="password", host="postgres"
        ) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                        CREATE TABLE IF NOT EXISTS users_address
                            (
                                uid VARCHAR(255),
                                city VARCHAR(255),
                                street_name VARCHAR(255),
                                street_address VARCHAR(255),
                                zip_code VARCHAR(255),
                                state VARCHAR(255),
                                country VARCHAR(255),
                                ts INT,

                                PRIMARY KEY (uid),
                                FOREIGN KEY (uid) REFERENCES users(uid)
                            );
                    """
                )

    except Exception as e:
        logging.error(red(e))

    return True


def check_table_exists(table_name):
    """Check if table exists"""
    try:
        with psycopg2.connect(
            dbname="postgres", user="postgres", password="password", host="postgres"
        ) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_schema = 'public' AND table_name = %s
                        );
                    """,
                    (table_name,),
                )
                result = curs.fetchone()
                return result[0] if result is not None else False
    except psycopg2.Error as e:
        logging.error(red(e))
        return False


def insert_into_user_table(user_data: dict) -> Literal[True]:
    """
    INSERT user data into users table

    Returns:
        Literal True
    """

    try:
        with psycopg2.connect(
            dbname="postgres", user="postgres", password="password", host="postgres"
        ) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                        INSERT INTO users (
                            uid, password, first_name, last_name, username, email, phone_number, social_insurance_number, date_of_birth, ts
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        );
                    """,
                    (
                        user_data["uid"],
                        user_data["password"],
                        user_data["first_name"],
                        user_data["last_name"],
                        user_data["username"],
                        user_data["email"],
                        user_data["phone_number"],
                        user_data["social_insurance_number"],
                        user_data["date_of_birth"],
                        int(datetime.timestamp(datetime.now())),
                    ),
                )

    except Exception as e:
        logging.error(red(e))

    return True


def insert_into_address_table(address_data: dict) -> Literal[True]:
    """
    INSERT users address data into users_address table

    Returns:
        Liternal True
    """
    try:
        with psycopg2.connect(
            dbname="postgres", user="postgres", password="password", host="postgres"
        ) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                        INSERT INTO users_address (
                            uid, city, street_name, street_address, zip_code, state, country, ts
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s
                        );
                    """,
                    (
                        address_data["uid"],
                        address_data["city"],
                        address_data["street_name"],
                        address_data["street_address"],
                        address_data["zip_code"],
                        address_data["state"],
                        address_data["country"],
                        int(datetime.timestamp(datetime.now())),
                    ),
                )

    except Exception as e:
        logging.error(red(e))

    return True
