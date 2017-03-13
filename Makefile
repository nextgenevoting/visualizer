help:
	@echo "USAGE: make test | clean"

test:
	python3 -m unittest discover -p '*.py' -v

clean:
	find . -type f -name '*.pyc' -print -delete
	find . -type d -name __pycache__ -print -exec rm -rf {} \;

.PHONY: help test clean
