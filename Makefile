SHELL:=/bin/bash
DOCKER_IMAGE?=mentor-classifier
DOCKER_CONTAINER=mentor-classifier
CLASSIFIER_ROOT=$(shell pwd)
PROJECT_ROOT?=$(shell git rev-parse --show-toplevel 2> /dev/null)
PWD=$(shell pwd)

# virtualenv used for pytest
VENV=.venv
$(VENV):
	$(MAKE) $(VENV)-update

.PHONY: $(VENV)-update
$(VENV)-update: virtualenv-installed
	[ -d $(VENV) ] || virtualenv -p python3 $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r ./requirements.test.txt

.PHONY: virtualenv-installed
virtualenv-installed:
	$(PROJECT_ROOT)/bin/virtualenv_ensure_installed.sh

.PHONY clean:
clean:
	rm -rf .venv

.PHONY docker-build:
docker-build:
	docker build -t $(DOCKER_IMAGE) .

.PHONY: format
format: $(VENV)
	$(VENV)/bin/black mentor_classifier

PHONY: test
test: $(VENV)
	export PYTHONPATH=$(shell echo $${PYTHONPATH}):$(PWD)/src && \
	$(VENV)/bin/py.test -vv $(args)

.PHONY: test-format
test-format: $(VENV)
	$(VENV)/bin/black --check mentor_classifier

.PHONY: test-lint
test-lint: $(VENV)
	$(VENV)/bin/flake8 .

test-all: test-format test-lint test-license test

LICENSE:
	@echo "you must have a LICENSE file" 1>&2
	exit 1

LICENSE_HEADER:
	@echo "you must have a LICENSE_HEADER file" 1>&2
	exit 1

.PHONY: license
license: LICENSE LICENSE_HEADER $(VENV)
	$(VENV)/bin/python3 -m licenseheaders -t LICENSE_HEADER -d bin
	$(VENV)/bin/python3 -m licenseheaders -t LICENSE_HEADER -d tests
	$(VENV)/bin/python3 -m licenseheaders -t LICENSE_HEADER -d mentor_classifier

.PHONY: test-license
test-license: LICENSE LICENSE_HEADER $(VENV)
	$(VENV)/bin/python3 -m licenseheaders -t LICENSE_HEADER -d bin --check
	$(VENV)/bin/python3 -m licenseheaders -t LICENSE_HEADER -d tests --check
	$(VENV)/bin/python3 -m licenseheaders -t LICENSE_HEADER -d mentor_classifier --check
