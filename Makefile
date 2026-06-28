ENTRY = a_maze_ing.py
CONFIG = config.txt

install:
	uv sync

run: install
	uv run python $(ENTRY) $(CONFIG)

debug: install
	uv run python -m pdb $(ENTRY) $(CONFIG)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +

lint:
	uv run flake8 src/ $(ENTRY)
	uv run mypy src/config src/mazegen
	uv run mypy $(ENTRY)

lint-strict:
	uv run flake8 src/ $(ENTRY)
	uv run mypy src/config src/mazegen --strict
	uv run mypy $(ENTRY) --strict
