# CBC to Excel

Outil pour convertir des exports CSV de la banque CBC en un fichier Excel structuré,
avec enrichissement automatique (type d’opération, contrepartie, catégorie, etc.).

## Prérequis

- Python 3.11+
- Les dépendances Python listées ci-dessous

## Installation

```bash
pip install pandas openpyxl xlsxwriter
```

## Utilisation

Depuis la racine du dépôt :

```bash
python -m core.main --input data/in_csv/export_BE50732047041718_20250118_1200.csv
```

Options disponibles :

```bash
python -m core.main \
  --input data/in_csv/export_BE50732047041718_20250118_1200.csv \
  --encoding latin-1 \
  --delimiter ";" \
  --categories data/categories.csv
```

Pour désactiver l’association des catégories :

```bash
python -m core.main --input data/in_csv/export_BE50732047041718_20250118_1200.csv --no-categories
```

## Tests

```bash
pytest
```
