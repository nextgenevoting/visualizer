help:
	@echo "USAGE: make test"

test:
	python3 -m unittest discover -p '*.py' -v

.PHONY: help test
