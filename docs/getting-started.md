# Démarrage rapide

## Installation locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Lancer une conversion

```bash
python -m core.main --input data/in_csv/mon_export.csv
```

## Données

Les fichiers dans `data/` sont utilisés comme entrées et sorties locales. Ils ne sont pas
nécessaires pour exécuter la CI et ne sont pas inclus dans les distributions.
