# ETL Data Pipeline

![Python](https://img.shields.io/badge/python-3776AB.svg?&style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/fastapi-009688.svg?&style=for-the-badge&logo=fastapi&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458.svg?&style=for-the-badge&logo=pandas&logoColor=white)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

![Redis](https://img.shields.io/badge/redis-DC382D.svg?&style=for-the-badge&logo=redis&logoColor=white)
![Postgres](https://img.shields.io/badge/postgresql-4169E1.svg?&style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED.svg?&style=for-the-badge&logo=docker&logoColor=white)

![React](https://img.shields.io/badge/react-35495e.svg?&style=for-the-badge&logo=react&logoColor=61DAFB)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-gray.svg?&style=for-the-badge&logo=tailwindcss&logoColor=06B6D4)

## Objective

Create a data pipeline that ingests user data via an API, processes and stores it, and then retrieves it in a serialized format.

## Components

1. **Data Source**: Random API for fake user data
2. **Python & Pandas**: For programming and data manipulation.
3. **Redis**: Caching recent data for quick access.
4. **Postgres**: Long-term data storage.
5. **FastAPI** For an API endpoint for data retrieval
6. **Docker**: Containerization of the entire pipeline.

## Steps

1. **Data Ingestion**:
   - Python script to fetch data from the OpenWeatherMap API.
   - Pandas for data cleaning and transformation.
2. **Caching Layer**:
   - Redis setup for caching recent weather data.
   - Python logic for data retrieval from Redis and Postgres.
3. **Data Storage**:
   - Design and implement a Postgres database schema for weather data.
   - Store processed data from Pandas into Postgres.
4. **Data Retrieval**:
   - API endpoint (e.g., using Flask) for data retrieval.
   - Serialization of data in structured format (JSON).
5. **Dockerization**:
   - Dockerfile for the Python application.
   - Docker Compose for orchestrating Redis and Postgres services.
6. **Testing and Deployment**:
   - Unit tests for pipeline components.
   - Deployment on local/cloud platform.

## Learning Outcomes

- Data pipeline architecture.
- Skills in Python, Pandas, Redis, Postgres, FastAPI and Docker.

## Further Enhancements

- Front-end dashboard for data display.
- Additional data sources for comparative analysis.
- Advanced data processing features.
