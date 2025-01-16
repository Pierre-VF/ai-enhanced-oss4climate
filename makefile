

.PHONY: install
install:
	uv sync

.PHONY: test
test:
	uv run pytest src/.