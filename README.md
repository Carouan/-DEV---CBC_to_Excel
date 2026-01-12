# CBC to Excel

Outil pour convertir des exports CSV de la banque CBC en un fichier Excel structuré,
avec enrichissement automatique (type d’opération, contrepartie, catégorie, etc.).

## Fonctionnalités

- Nettoyage et normalisation des colonnes CBC.
- Catégorisation automatique via un fichier de catégories.
- Génération d'un fichier Excel prêt à l'analyse.
- Exécutable Windows portable basé sur PyInstaller.

## Prérequis

- Python 3.12+ recommandé.
- Les dépendances sont gérées via le fichier `pyproject.toml`.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Utilisation

Commande canonique (un fichier CSV) :

```bash
cbc-to-excel --input "path/to/file.csv" --output-dir "path/to/out"
```

Si `--output-dir` est omis, la sortie est écrite dans `data/out_xlsx/`.

Exemple avec chemin complet :

```bash
cbc-to-excel --input data/in_csv/export.csv --output-dir data/out_xlsx
```

Options disponibles :

```bash
cbc-to-excel \
  --input data/in_csv/export.csv \
  --output-dir data/out_xlsx \
  --encoding latin-1 \
  --delimiter ";" \
  --categories data/categories.csv
```

Par défaut, l'outil charge un fichier de catégories embarqué dans le package. Si la
ressource n'est pas disponible, il utilise `data/categories.csv` du dépôt.

Pour désactiver l’association des catégories :

```bash
cbc-to-excel --input data/in_csv/export.csv --no-categories
```

Les CSV d'entrée locaux sont attendus sous `data/in_csv/` (ce dossier est ignoré par git).

## Exécutable Windows portable

- L'exécutable `cbc-to-excel.exe` peut être copié sur une clé USB.
- La commande `--check-updates` vérifie la dernière release GitHub.
- La commande `--update` télécharge `cbc-to-excel.new.exe` et génère `update.bat`.

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
