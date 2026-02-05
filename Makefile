FNAME = a_maze_ing.py
FCONFIG = config.txt
MODULES = flake8 mypy


install:
	pip install $(MODULES)

debug:
	python3 -m pdb $(FNAME) $(FCONFIG)

clean:
	rm -rf __pycache__ .mypy_cache *.pyc

lint:
	flake8 .
	mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
