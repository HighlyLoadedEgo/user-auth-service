# Run all lints
lints:
    ruff check . && mypy . && black . && isort .

# Up anyone container
up CON_NAME='':
    docker compose up -d {{CON_NAME}}

# Create migration
migration MIGRATION_NAME='':
    alembic revision --autogenerate -m "{{MIGRATION_NAME}}"

# Upgrade migration
upgrade VERSION='head':
    alembic upgrade {{VERSION}}

# Downgrade migrations
downgrade VERSION='-1':
    alembic downgrade {{VERSION}}

# Run tests
test ARGS='tests':
    poetry run pytest -n 4 {{ARGS}}

run ARGS='':
    python -O {{ARGS}} main.py
