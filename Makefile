MAIN= src/__main__.py
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
	uv run python3 -m src

debug:
	$(PYTHON) -m pdb $(MAIN)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf data/output/
	rm -rf data/correction

bonfire: clean
	rm -rf $(VENV_DIR)

lint:
	uv run flake8 --exclude=.venv,testing,llm_sdk,moulinette
	uv run mypy --exclude '.venv/|testing/|llm_sdk/|moulinette/' --no-namespace-packages src $(MYPY_FLAGS)

lint-strict:
	uv run flake8 --exclude=.venv,testing,llm_sdk,moulinette
	uv run mypy --exclude '.venv/|testing/|llm_sdk/moulinette/' --no-namespace-packages src $(MYPY_FLAGS)