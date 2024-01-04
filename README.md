# ETL Data Pipeline

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/mrpbennett/etl-pipeline?style=for-the-badge)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/mrpbennett/etl-pipeline/sourcery-pr.yml?style=for-the-badge&label=sourcery)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/mrpbennett/etl-pipeline/python-package.yml?style=for-the-badge&label=build)

![FastAPI](https://img.shields.io/badge/fastapi-009688.svg?&style=for-the-badge&logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458.svg?&style=for-the-badge&logo=pandas&logoColor=white)
![Redis](https://img.shields.io/badge/redis-DC382D.svg?&style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/postgresql-4169E1.svg?&style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED.svg?&style=for-the-badge&logo=docker&logoColor=white) ![React](https://img.shields.io/badge/react-35495e.svg?&style=for-the-badge&logo=react&logoColor=61DAFB)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-gray.svg?&style=for-the-badge&logo=tailwindcss&logoColor=06B6D4)

## Objective

Create a data pipeline that ingests user data via an API, processes and stores it, and then retrieves it in a serialized format.

### Components

1. **Data Source**: Random API for fake user data
2. **Python & Pandas**: For programming and data manipulation.
3. **Redis**: Caching recent data for quick access.
4. **Postgres**: Long-term data storage.
5. **FastAPI** For an API endpoint for data retrieval
6. **Docker**: Containerization of the entire pipeline.

### Steps

1. **Data Ingestion**:
   - Python script to fetch data random user data from an API.
     - `get_data.py`
   - Pandas for data cleaning and transformation.
     - `clean_up.py`
2. **Caching Layer**:
   - Redis setup for caching recent User data and set a TTL.
     - `caching.py`
   - Python logic for data retrieval from Redis and Postgres.
     - `api.py`
3. **Data Storage**:
   - Design and implement a Postgres database schema for the user data.
   - Store processed data into Postgres.
     - `storage.py`
4. **Data Retrieval**:
   - API endpoint (e.g., using FastAPI) for data retrieval.
     - `api.py`
5. **Dockerization**:
   - Dockerfile for the Python application.
     - `Dockerfile.main`
     - `Dockerfile.api`
   - Docker Compose for orchestrating Redis and Postgres services.
     - `docker-compose.yml`
6. **Testing and Deployment**:
   - Unit tests for pipeline components.
     - `./tests`

### Learning Outcomes

- Data pipeline architecture.
- Skills in Python, Pandas, Redis, Postgres, FastAPI and Docker.

### Further Enhancements

- ~~Front-end dashboard for data display.~~
- Advanced data processing features.

## How to test the project

Clone the repo

```bash
git clone https://github.com/mrpbennett/etl-pipeline.git
```

`cd` into the cloned repo and run `docker compose up`

```bash
docker compose up
```

Then head over to the URL to access the front end to see where the data is stored

```text
http://127.0.0.1:80/static/index.html
```
