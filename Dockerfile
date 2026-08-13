FROM python:3.14-slim AS base_bare

LABEL NAME=pipelines
LABEL VERSION=1.0.0

WORKDIR /app/

# Install uv by copying the static binary from the official distroless image.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy the files required to resolve and install dependencies.
COPY pyproject.toml uv.lock README.md ./
COPY pipelines/__init__.py pipelines/__init__.py

# Install dependencies from the lockfile into the system environment.
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

# Create a non-root user owning the application directory.
RUN useradd --create-home app \
    && chown app:app /app

ENTRYPOINT [ "bash" ]


FROM base_bare AS base

# Copy all other files here to optimize caching.
COPY ./ ./

USER app


FROM base_bare AS test

# Install system dependencies:
# - git for pre-commit itself,
# - shellcheck for the shellcheck hook,
# - libatomic1 and libstdc++6 for the node runtime used by markdownlint and pyright.
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        git \
        libatomic1 \
        libstdc++6 \
        shellcheck \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies with dev and test groups.
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --group dev --group test
COPY .pre-commit-config.yaml .pre-commit-config.yaml

# Install pre-commit hooks.
# Run as root: CI bind-mounts the workspace, which requires broad write access.
# Mark /app as safe first, as it is owned by the non-root user.
RUN git config --global --add safe.directory /app
RUN git init .
RUN pre-commit install-hooks
