help:
	@echo "USAGE: make testall | test | clean"

dev:
	source virtualenv/bin/activate; python backend_service.py

test: ${FILE}
	python3 -m unittest -v ${FILE}

testall:
	python3 -m unittest discover -p '*.py' -v

clean:
	find . -type f -name '*.pyc' -print -delete
	find . -type d -name __pycache__ -print -exec rm -rf {} \;

.PHONY: help testall test clean
