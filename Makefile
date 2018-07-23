SHELL := /bin/bash

all:	dist

dist:
	python setup.py sdist
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*

clean:
	rm -f *.html 
	rm -rf dist build  kaldi_adapt_lm.egg-info  

