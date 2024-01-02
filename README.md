# ETL Data Pipeline

## Objective

Create a data pipeline that ingests user data via an API, processes and stores it, and then retrieves it in a serialized format.

## Components

1. **Data Source**: Random API for fake user data
2. **Python & Pandas**: For programming and data manipulation.
3. **Redis**: Caching recent data for quick access.
4. **Postgres**: Long-term data storage.
5. **Serialization/Deserialization**: JSON or another format for data serialization during retrieval.
6. **FastAPI** For an API endpoint for data retrieval
7. **Docker**: Containerization of the entire pipeline.

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
4. **Data Retrieval and Serialization**:
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
- Data serialization/deserialization.

## Further Enhancements

- Front-end dashboard for data display.
- Additional data sources for comparative analysis.
- Advanced data processing features.
