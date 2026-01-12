# CBC to Excel

Outil pour convertir des exports CSV de la banque CBC en un fichier Excel structuré,
avec enrichissement automatique (type d’opération, contrepartie, catégorie, etc.).

## Fonctionnalités

- Nettoyage et normalisation des colonnes CBC.
- Catégorisation automatique via un fichier de catégories.
- Génération d'un fichier Excel prêt à l'analyse.

## Prérequis

- Python 3.12+ recommandé.
- Les dépendances sont gérées via le fichier `pyproject.toml`.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Utilisation

Depuis la racine du dépôt :

```bash
python -m core.main --input data/in_csv/export_BE50732047041718_20250118_1200.csv
```

Avec le script console :

```bash
cbc-to-excel --input data/in_csv/export_BE50732047041718_20250118_1200.csv
```

Options disponibles :

```bash
python -m core.main \
  --input data/in_csv/export_BE50732047041718_20250118_1200.csv \
  --encoding latin-1 \
  --delimiter ";" \
  --categories data/categories.csv \
  --output data/out_xlsx/rapport.xlsx
```

Pour désactiver l’association des catégories :

```bash
python -m core.main --input data/in_csv/export_BE50732047041718_20250118_1200.csv --no-categories
```

Les CSV d'entrée locaux sont attendus sous `data/in_csv/` (ce dossier est ignoré par git).

## Développement

```bash
ruff check .
ruff format .
pytest
```

Pour la documentation locale :

```bash
pip install -e ".[docs]"
mkdocs serve
```

### Pré-commit

```bash
pre-commit install
pre-commit run --all-files
```

## Troubleshooting

- Ruff manquant : réinstallez les extras de dev avec `pip install -e ".[dev]"`.
- Problèmes d'encodage : essayez `--encoding latin-1` ou `--encoding utf-8` selon le CSV.

## Structure du dépôt

- `core/` : package principal.
- `tests/` : tests pytest.
- `data/` : fichiers d'entrée CSV et sorties Excel (non versionnés dans les artefacts).
- `doc/` : notes internes.

## CI & données

Les fichiers `data/`, `doc/` et les exports `.xlsx` ne sont pas inclus dans les distributions
et ne sont pas nécessaires pour exécuter la CI.
