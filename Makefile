SHELL:=/bin/bash
DOCKER_IMAGE?=mentorpal-classifier
DOCKER_CONTAINER=mentorpal-classifier
CLASSIFIER_ROOT=$(shell pwd)
PROJECT_ROOT?=$(shell git rev-parse --show-toplevel 2> /dev/null)
PWD=$(shell pwd)

docker-build:
	docker build -t $(DOCKER_IMAGE) .

# virtualenv used for pytest
TEST_VIRTUAL_ENV=.venv
$(TEST_VIRTUAL_ENV):
	$(MAKE) test-env-create

.PHONY: format
format: $(TEST_VIRTUAL_ENV)
	$(TEST_VIRTUAL_ENV)/bin/black mentorpal_classifier

PHONY: test
test: $(TEST_VIRTUAL_ENV)
	export PYTHONPATH=$(shell echo $${PYTHONPATH}):$(PWD)/src && \
	$(TEST_VIRTUAL_ENV)/bin/py.test -vv $(args)

.PHONY: test-env-create
test-env-create: virtualenv-installed
	[ -d $(TEST_VIRTUAL_ENV) ] || virtualenv -p python3 $(TEST_VIRTUAL_ENV)
	$(TEST_VIRTUAL_ENV)/bin/pip install --upgrade pip
	$(TEST_VIRTUAL_ENV)/bin/pip install -r ./requirements.test.txt

.PHONY: test-format
test-format: $(TEST_VIRTUAL_ENV)
	$(TEST_VIRTUAL_ENV)/bin/black --check mentorpal

.PHONY: test-lint
test-lint: $(TEST_VIRTUAL_ENV)
	$(TEST_VIRTUAL_ENV)/bin/flake8 .

test-all: test-format test-lint test

.PHONY: virtualenv-installed
virtualenv-installed:
	$(PROJECT_ROOT)/bin/virtualenv_ensure_installed.sh
