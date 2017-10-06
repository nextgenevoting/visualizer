# CHVote #

### Installation

Install python 3.4
pip install gmpy2
pip install flask-socketio

## Unit tests ##

### Run all unit tests for a single file ###

```bash
python3 -m unittest -v FILE.py
# or
make test FILE.py
```

### Run all unit tests for all files ###

```bash
python3 -m unittest discover -p '*.py' -v
# or
make testall
```

## Sphinx Python Docs ##

### Installation ###
```bash
pip install sphinx
pip install sphinxcontrib-napoleon
```

### Add content ###
In "docs/source" modify crypto.rst and chvote.rts.

### Build ###
From directory docs, run:
```bash
make html
```
