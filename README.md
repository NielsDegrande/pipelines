# Pipelines

## Introduction

This repository holds various data science pipelines.

## Getting Started

Set up a virtual environment:

```shell
python3 -m venv venv
source venv/bin/activate
make install_dev
```

To run pipelines against test fixtures.
The below assumes you are in the repository root.

```shell
ln -s $PWD/data/fixtures/input $PWD/data/input
```

Run a pipeline with: `pipes --pipeline sample` or `python -m pipelines --pipeline sample`.

Run `pipes --help` to see all possible options.

## Services

This repository has one optional service, the database.
To run the database, run `docker-compose up --detach database`.

## Data Connectors

Data connectors allow to read or write from different data sources. Currently, we support the following connectors:

- Local file system.
- Google Cloud Storage.
- Database.

To interact with GCS, ensure you are logged into the `gcloud` CLI tool.
To interact with the database, ensure the following environment variables are available:

```shell
# Database.
echo 'DB_DIALECT=postgresql' >> .env
echo 'DB_HOST=localhost' >> .env
echo 'DB_NAME=annualaid' >> .env
echo 'DB_USER=user' >> .env
echo 'DB_PASSWORD=password' >> .env
```
