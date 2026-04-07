PYTHON ?= python3

.PHONY: test build-center

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

build-center:
	PYTHONPATH=src $(PYTHON) -m release_readiness_center.cli build --data-file data/releases.json --export-dir reports
