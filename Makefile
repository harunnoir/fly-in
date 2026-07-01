.PHONY: install run debug clean lint lint-strict

install:
	uv install mypy flake8 colorama

run:
	uv run main.py

debug:
	python -m pdb main.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache *.pyc *.pyo venv .venv

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
