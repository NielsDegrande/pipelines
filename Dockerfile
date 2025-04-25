FROM python:3.12 AS base_bare

LABEL NAME=pipelines
LABEL VERSION=1.0.0

WORKDIR /app/

# Install uv, do this before copying files for caching purposes.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir uv

# Copy pyproject.toml, uv.lock and README.md files.
COPY pyproject.toml uv.lock README.md ./
COPY pipelines/__init__.py pipelines/__init__.py

# Install dependencies.
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync

ENTRYPOINT [ "bash" ]


FROM base_bare AS base

# Copy all other files here to optimize caching.
COPY ./ ./


FROM base_bare AS test

# Dependencies for pre-commit.
RUN apt-get update \
    && apt-get install shellcheck -y \
    && apt-get clean

# Install dependencies with dev and test extras.
RUN uv sync --group dev --group test
COPY .pre-commit-config.yaml .pre-commit-config.yaml

# Install pre-commit hooks.
RUN git init .
RUN pre-commit install-hooks
RUN git config --global --add safe.directory /app
