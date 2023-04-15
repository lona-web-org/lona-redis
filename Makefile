SHELL=/bin/bash
PYTHON=python3

PYTHON_ENV_ROOT=envs
PYTHON_DEV_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-dev
PYTHON_PACKAGING_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-packaging
PYTHON_TESTING_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-testing


.PHONY: all clean shell python-shell dist _release

clean:
	rm -rf $(PYTHON_ENV_ROOT)

# python ######################################################################
$(PYTHON_DEV_ENV): pyproject.toml
	rm -rf $(PYTHON_DEV_ENV) && \
	$(PYTHON) -m venv $(PYTHON_DEV_ENV) && \
	. $(PYTHON_DEV_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -e .

$(PYTHON_PACKAGING_ENV): pyproject.toml
	rm -rf $(PYTHON_PACKAGING_ENV) && \
	$(PYTHON) -m venv $(PYTHON_PACKAGING_ENV) && \
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install .[packaging]

$(PYTHON_TESTING_ENV): pyproject.toml
	rm -rf $(PYTHON_TESTING_ENV) && \
	$(PYTHON) -m venv $(PYTHON_TESTING_ENV) && \
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install .[testing]

# helper
shell: $(PYTHON_DEV_ENV)
	. $(PYTHON_DEV_ENV)/bin/activate && \
	/bin/bash

python-shell: $(PYTHON_DEV_ENV)
	. $(PYTHON_DEV_ENV)/bin/activate && \
	rlpython

# tests
test-script: $(PYTHON_DEV_ENV)
	. $(PYTHON_DEV_ENV)/bin/activate && \
	$(PYTHON) test-script/test_script.py $(args)

# packaging
dist: $(PYTHON_PACKAGING_ENV)
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	rm -rf dist *.egg-info && \
	python -m build

_release: dist
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	twine upload --config-file ~/.pypirc.fscherf dist/*

# tests #######################################################################
testclean:
	rm -rf $(PYTHON_ENV)
	rm -rf tests/.tox

test: | $(PYTHON_TESTING_ENV)
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	cd tests && \
	tox $(args)

