.PHONY: install run debug clean lint lint-strict

run:
	@command -v uv >/dev/null 2>&1 || (curl -LsSf https://astral.sh/uv/install.sh | sh && export PATH="$$HOME/.local/bin:$$PATH")
	uv run main.py ./maps/challenger/01_the_impossible_dream.txt

install:
	uv add mypy flake8 colorama

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
