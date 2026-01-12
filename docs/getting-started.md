# Démarrage rapide

## Installation locale

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Lancer une conversion

Commande canonique (un fichier CSV) :

```bash
cbc-to-excel --input "path/to/file.csv" --output-dir "path/to/out"
```

Si `--output-dir` est omis, la sortie est écrite dans `data/out_xlsx/`.

## Options utiles

- `--categories` : chemin vers un fichier CSV de catégories personnalisé.
- `--no-categories` : désactive la catégorisation automatique.
- `--check-updates` : force la vérification de mise à jour.
- `--no-update-check` : désactive la vérification automatique.
- `--update` : télécharge l'exécutable Windows le plus récent (portable).

Par défaut, le fichier de catégories est embarqué dans le package. En environnement
de développement sans ressource embarquée, la valeur de repli est
`data/categories.csv`.

## Données

Les fichiers dans `data/` sont utilisés comme entrées et sorties locales. Ils ne sont pas
nécessaires pour exécuter la CI et ne sont pas inclus dans les distributions.
