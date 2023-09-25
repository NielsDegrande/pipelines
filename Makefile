# No (file) targets are assumed for most Makefile commands.
.PHONY:
	install_poetry
	install
	install_dev
	build_base_bare
	build_base
	build_test
	build_latex
	run_pipeline
	run_pre_commit
	run_tests
	run_container
	compile_documentation

install_poetry:
	pip install --upgrade pip
	# Installing poetry if not installed...
	@python -m poetry --version || \
		pip install poetry

install: install_poetry
	poetry install

install_dev: install_poetry
	poetry install --with dev,test
	# Installs the pre-commit hook.
	pre-commit install

build_base_bare:
	docker build \
		--file Dockerfile \
		--target base_bare \
		--tag pipelines-bare \
		--cache-from=pipelines-bare \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

build_base:
	docker build \
		--file Dockerfile \
		--target base \
		--tag pipelines \
		--cache-from=pipelines-bare \
		--cache-from=pipelines \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

build_test:
	docker build \
		--file Dockerfile \
		--target test \
		--tag pipelines-test  \
		--cache-from=pipelines-bare \
		--cache-from=pipelines \
		--cache-from=pipelines-test \
		--build-arg BUILDKIT_INLINE_CACHE=1 \
		${PWD}

build_latex:
	docker build \
		--file ${PWD}/docs/LaTeX/Dockerfile \
		--tag latex \
		${PWD}

run_pipeline: build_base
	docker run --rm \
		--volume ${PWD}/logs:/app/logs \
		--volume ${PWD}/data/:/app/data \
		pipelines \
		-c "pipes --pipeline sample"

run_pre_commit: build_test
	docker run --rm \
		--volume ${PWD}:/app \
		pipelines-test \
		-c "pre-commit run --all-files"

run_tests: build_test
	docker run --rm \
		--volume ${PWD}:/app \
		pipelines-test \
		-c "pytest -n auto --durations=0 tests"

run_container: build_test
	docker run -it --rm \
		--volume ${PWD}/:/app/ \
		pipelines-test

compile_documentation: build_latex
	docker run --rm --volume ${PWD}/docs/LaTeX:/docs latex
