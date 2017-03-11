# CHVote #

## Unit tests ##

### Run all unit tests for a single file ###

```bash
python3 -m unittest -v FILE_WITHOUT_EXTENSION
```

Or simply:
```bash
python3 FILE.py -v
```

### Run all unit tests for all files ###

```bash
python3 -m unittest discover -p '*.py' -v
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



