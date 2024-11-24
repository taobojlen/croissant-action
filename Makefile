test:
	uv run pytest -s --tb=native --random-order --junit-xml=./testresults.xml $(ARGS)

format-check:
	uv run ruff format --check && ruff check

format:
	uv run ruff format && uv run ruff check --fix
