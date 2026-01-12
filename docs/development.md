# Développement

## Environnement

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Lint, format et tests

```bash
ruff format .
ruff check .
pytest
```

## Pré-commit

```bash
pre-commit install
pre-commit run --all-files
```

## Documentation

```bash
pip install -e ".[docs]"
mkdocs serve
```
