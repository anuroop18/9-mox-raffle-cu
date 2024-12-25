# Run the formatter
format:
    # Python
    uv run ruff check --select I --fix
    uv run ruff check . --fix
    # Vyper
    uv run mamushi contracts