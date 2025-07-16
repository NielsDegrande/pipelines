#!/usr/bin/make

## help: Print help.
.PHONY: help
help:
	@echo Possible commands:
	@cat Makefile | grep '##' | grep -v "Makefile" | sed -e 's/^##/  -/'

## install: Install dependencies.
.PHONY: install
install:
	uv venv
	. .venv/bin/activate
	uv sync --no-dev

## install_dev: Install dependencies for development.
.PHONY: install_dev
install_dev:
	uv venv
	. .venv/bin/activate && uv sync --group dev --group test
	# Installs the pre-commit hook.
	. .venv/bin/activate && pre-commit install

## build_base_bare: Build the base image without any dependencies.
.PHONY: build_base_bare
build_base_bare:
	docker build \
		--file Dockerfile \
		--target base_bare \
		--tag pipelines-bare \
		--cache-from=pipelines-bare \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

## build_base: Build the base image.
.PHONY: build_base
build_base:
	docker build \
		--file Dockerfile \
		--target base \
		--tag pipelines \
		--cache-from=pipelines-bare \
		--cache-from=pipelines \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

## build_test: Build the test image.
.PHONY: build_test
build_test:
	docker build \
		--file Dockerfile \
		--target test \
		--tag pipelines-test \
		--cache-from=pipelines-bare \
		--cache-from=pipelines \
		--cache-from=pipelines-test \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

## run_pipeline: Run a pipeline.
.PHONY: run_pipeline
run_pipeline: build_base
	docker run --rm \
		--volume ${PWD}/logs:/app/logs \
		--volume ${PWD}/data/:/app/data \
		pipelines \
		-c "pipes --pipeline sample"

## run_pre_commit: Run pre-commit.
.PHONY: run_pre_commit
run_pre_commit: build_test
	docker run --rm \
		--volume ${PWD}:/app \
		pipelines-test \
		-c "pre-commit run --all-files"

## run_tests: Run tests.
.PHONY: run_tests
run_tests: build_test
	docker run --rm \
		--volume ${PWD}:/app \
		pipelines-test \
		-c "pytest -n auto -rf --durations=0 tests"

## run_container: Run container.
.PHONY: run_container
run_container: build_test
	docker run -it --rm \
		--volume ${PWD}/:/app/ \
		pipelines-test
