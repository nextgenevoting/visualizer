help:
	@echo "USAGE: make test | clean"

test:
	python3 -m unittest discover -p '*.py' -v

clean:
	rm -f *.pyc */*.pyc
	rm -rf __pycache__

.PHONY: help test
