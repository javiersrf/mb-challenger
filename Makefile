lint:
	uv run ruff check
	uv run ruff format --check

format:
	uv run ruff check --fix
	uv run ruff format .

test:
	PYTHONPATH=. uv run pytest

run:
	uv run main.py


migrate:
	uv run alembic upgrade head


build:
	uv export --format requirements.txt > requirements.txt
	docker build -t mb-api .