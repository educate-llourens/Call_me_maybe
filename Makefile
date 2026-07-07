MAIN= call_me_maybe.py
VENV_DIR= .venv
BIN_DIR= $(VENV_DIR)/bin
PYTHON= $(BIN_DIR)/python3
PIP= $(BIN_DIR)/pip
ACTIVATE=$(BIN_DIR)activate
MYPY_FLAGS= --warn-return-any \
			--warn-unused-ignore \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs

all: run

install:
	uv venv
	uv sync
run:
	uv run src/__main__.py

debug:
	

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache

bonfire:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf $(VENV_DIR)
	rm -rf .pytest_cache

lint:
	flake8
	python3 -m mypy . $(MYPY_FLAGS)

lint-strict:
	flake8
	$(PYTHON) -m mypy . --strict