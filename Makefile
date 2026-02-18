FNAME = a_maze_ing.py
FCONFIG = config.txt
MODULES = flake8 mypy pygame


run:
	python3 $(FNAME) $(FCONFIG)

install:
	pip install $(MODULES)

debug:
	python3 -m pdb $(FNAME) $(FCONFIG)

clean:
	rm -rf __pycache__ .mypy_cache *.pyc

lint:
	python3 -m flake8 . --exclude=venv
	python3 -m mypy . --warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude venv

lint-strict:
	python3 -m flake8 . --exclude=venv
	python3 -m mypy . --strict --exclude venv
