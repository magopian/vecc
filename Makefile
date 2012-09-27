proj = vecc


test:
	nosetests -x $(proj)

sdist:
	python setup.py sdist
