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

## Build de l'exécutable Windows

Sur une machine Windows :

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
pyinstaller pyinstaller.spec
```

L'exécutable portable est généré dans `dist/cbc-to-excel.exe`.
