# Pipelines

## Introduction

This repository holds various data science pipelines.

## Getting Started

```shell
python3 -m venv venv
source venv/bin/activate
make install_dev
# Assuming you are in the repo root and want to run against test fixtures.
ln -s $PWD/data/fixtures/input $PWD/data/input
```

Run a pipeline with: `pipes --pipeline sample` or `python -m pipelines --pipeline sample`.

## Initialization TODOs

- Decide if you need docs in this repository, else delete `docs`. If yes, then set up GitHub pages.
- Decide if the docs are for this repo alone, or for a larger project. If so, change the scoping of the docs.
- Add CD if relevant. See `.github/workflows` to get started.
- Add branch protection.
- Read through the `Initial Commit` you will make, and replace any remaining placeholders and dummy text.
