# Template

## Introduction

Write a good introduction.

## Getting Started

```shell
python3 -m venv venv
source venv/bin/activate
make install_dev
# Assuming you are in the repo root and want to run against test fixtures.
ln -s $PWD/data/fixtures/input $PWD/data/input
```

Run the pipeline with: `temp` or `python -m template`.

## Initialization TODOs

- Search for 'template' or 'Template', and replace all occurrences.
- Decide if you need docs in this repository, else delete `docs`. If yes, then set up GitHub pages.
- Add CD if relevant. See `.github/workflows` to get started.
- Add branch protection.
- Read through the `Initial Commit` you will make, and replace any remaining placeholders and dummy text.
