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

Initiate the environment for local development:

```shell
echo '# Database' >> .env
echo DB_DIALECT=postgresql >> .env
echo DB_HOST=localhost >> .env
echo DB_NAME=postgres >> .env
echo DB_USER=user >> .env
echo DB_PASSWORD=password >> .env
```

Run a pipeline with: `pipes --pipeline sample` or `python -m pipelines --pipeline sample`.

Run `pipes --help` to see all possible options.

## Initialization TODOs

- Add branch protection.
- Add CD if relevant. See `.github/workflows` to get started.
- Read through the `Initial Commit` you will make.

## Services

This repository has one optional service, the database.
To run the database, run `docker-compose up --detach database`.
