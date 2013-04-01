.PHONY: docs test clean

bin/python:
	virtualenv .
	bin/python setup.py develop

test: bin/python
	bin/pip install tox
	bin/tox

clean:
	rm -rf bin .tox include/ lib/ man/ vecc.egg-info/ build/
