""" Data Retrieval and Serialization """

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "I am Root"}


@app.get("/api/datapipe/{user_id}")
async def get_weather(date: str):
    """
    #TODO:
    Check data from Redis and return if cached.
    """

    """
    #TODO:
    If no data is present in Redis. Get from Postgres.
    """
    pass
