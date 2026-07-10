PYTHON = python3
VENV = venv
PIP = pip

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/$(PIP) install --upgrade pip
	$(VENV)/bin/$(PIP) install flake8 mypy pytest

run:
	./$(VENV)/bin/$(PYTHON) a_maze_ing.py config.txt

debug:
	./$(VENV)/bin/$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(VENV)

lint:
	./$(VENV)/bin/flake8 . --exclude=$(VENV)
	./$(VENV)/bin/mypy . --exclude=$(VENV) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	./$(VENV)/bin/flake8 . --exclude=$(VENV)
	./$(VENV)/bin/mypy . --exclude=$(VENV) --strict
