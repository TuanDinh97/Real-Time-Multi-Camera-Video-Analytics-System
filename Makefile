.PHONY: setup lint test

setup:  ## cài môi trường dev và git hook
	uv sync --all-extras
	uv run pre-commit install

lint:   ## kiểm tra style và kiểu dữ liệu
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy

test:   ## chạy test
	uv run pytest
