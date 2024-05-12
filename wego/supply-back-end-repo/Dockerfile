# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.2
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr.
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install system dependencies required for GDAL
# This must be done before we switch to the non-privileged user
USER root
RUN apt-get update && apt-get install -y \
    libgdal-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Determine GDAL version and set as environment variable
RUN GDAL_VERSION=$(gdal-config --version) && \
    echo "GDAL version is $GDAL_VERSION" && \
    echo "GDAL_VERSION=$GDAL_VERSION" >> /etc/environment && \
    echo "GDAL_LIBRARY_PATH=/usr/lib/libgdal.so.$GDAL_VERSION" >> /etc/environment && \
    echo "GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so" >> /etc/environment

# Now set the ENV variables to ensure they persist
ENV GDAL_VERSION=$GDAL_VERSION
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so.$GDAL_VERSION
ENV GEOS_LIBRARY_PATH=/usr/lib/libgeos_c.so

# Install Python packages as root
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt,readonly \
    pip install -r requirements.txt

# Create a non-privileged user to run the application.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch back to the non-privileged user for the rest of the setup
USER appuser

# Copy the source code into the container.
# COPY --chown=appuser:appuser . .

# Expose the port that the application listens on.
EXPOSE 9000

# Run the application.
CMD python manage.py runserver 0.0.0.0:9000
