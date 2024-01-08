# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install pipenv and pipenv dependencies
COPY Pipfile Pipfile.lock /app/
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

# Install async-timeout and numpy
RUN pip install async-timeout numpy exceptiongroup

# Copy the rest of the application files into the container
COPY src /app/src
COPY static /app/static/

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

