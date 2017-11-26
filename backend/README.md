# CHVote #

### Setup

Install python 3.4

```sh
pip install virtualenv
virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt # pip install flask flask-socketio flask-cors eventlet pymongo gmpy2 jsonpointer
```

## Unit tests ##

### Run all unit tests for a single file ###

```sh
python3 -m unittest -v FILE.py
# or
make test FILE.py
```

### Run all unit tests for all files ###

```sh
python3 -m unittest discover -p '*.py' -v
# or
make testall
```

## Sphinx Python Docs ##

### Installation ###

```sh
pip install sphinx
pip install sphinxcontrib-napoleon
```

### Add content ###

In "docs/source" modify crypto.rst and chvote.rts.

### Build ###

From directory docs, run:
```sh
make html
```
