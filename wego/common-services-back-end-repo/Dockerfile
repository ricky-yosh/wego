# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files to avoid unnecessary disk I/O.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to ensure logs are emitted immediately.
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install system dependencies required for mysqlclient and other packages.
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user to enhance the container's security.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies separately to leverage Docker's layer caching.
# Utilize a cache mount to persist pip's cache across builds and a bind mount for requirements.txt.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user for running the application.
USER appuser

# In a development environment using Docker volumes, this COPY command is not needed.
# COPY . .

# Expose the application's port to enable access.
EXPOSE 8000

# Define the command to run the application.
CMD python manage.py runserver 0.0.0.0:8000