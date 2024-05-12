# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install system dependencies required for MariaDB/MySQL Python packages
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    build-essential \ 
    # Clean up the apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install Python dependencies.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Switch to the non-privileged user.
USER appuser

# Expose the application port.
EXPOSE 10000

# Run the application.
CMD python manage.py runserver 0.0.0.0:10000