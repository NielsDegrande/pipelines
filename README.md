# Pipelines

## Introduction

This repository holds various data science pipelines.

## Getting Started

Set up your development environment:

```shell
make install_dev
```

To run pipelines against test fixtures.
The below assumes you are in the repository root.

```shell
ln -s $PWD/data/fixtures/input $PWD/data/input
```

Run a pipeline with: `pipes --pipeline sample` or `python -m pipelines --pipeline sample`.

Run `pipes --help` to see all possible options.

## Configuration Management

This repository uses hierarchical configuration management.
That means that multiple configuration files will be loaded,
where the type and order determines how these files will be consolidated.

The following configuration files are loaded upon pipeline start:

- Main root config: `config.yaml`.
- Data connector configuration `data_connectors.yaml`.
- Any further root configs specified as command line argument with `--root_config`.
- Main pipeline config: `{pipeline}/config.yaml`.
- Any further pipeline configs specified as command line argument with `--pipeline_config`.
- Configuration specified as command line argument with `--cli_config`.

These files are combined in a single configuration object.
Previously unseen keys are appended to this object.
Conflicting keys are resolved by giving precedence to last loaded configuration file.

One can experiment with this functionality by running:

```shell
# Multiplier 5.
pipes --pipeline sample
# Multiplier 7.
pipes --pipeline sample --pipeline_config e2e_test
# Multiplier 10.
pipes --pipeline sample --pipeline_config production
# Multiplier 7 as `e2e_test` is specified last.
pipes --pipeline sample --pipeline_config production e2e_test
# Printed value is cli_pipeline_value.
pipes --pipeline sample --cli_config sample.key=cli_pipeline_value
```

Inspect the price column in `data/output/sample/products.csv` to see the result.

## Data Connectors

Data connectors allow to read or write from different data sources. Currently, we support the following connectors:

- Local file system.
- Google Cloud Storage.
- Database.

To interact with GCS, ensure you are logged into the `gcloud` CLI tool.
To interact with the database, copy the `.env.example` file to `.env` and fill in the values.

```shell
cp .env.example .env
```

To benefit from the data connector abstraction,
only read or write data using the functions provided in `data/reader.py` and `data/writer.py`.
Never import data connectors in a pipeline or step module.

## Services

This repository has one optional service, the database.
To run the database, run `docker-compose up --detach database`.
