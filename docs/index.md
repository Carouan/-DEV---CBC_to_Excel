# CBC to Excel

CBC to Excel transforme des exports CSV de la banque CBC en un fichier Excel structuré.
L'outil applique des règles de nettoyage, enrichit les données (type d’opération,
contrepartie, catégorie) puis génère un fichier `.xlsx` prêt à l’analyse.

## Points clés

- Pipeline de transformation en plusieurs étapes.
- Catégorisation configurable via un fichier CSV.
- Génération d'Excel avec styles applicables.
- Vérification des mises à jour via GitHub Releases pour l'exécutable portable.

## Pipeline CSV → Excel

1. Validation du schéma minimal (Description, Montant, Valeur).
2. Nettoyage et création des colonnes attendues.
3. Détection du type d’opération depuis la Description.
4. Enrichissement des contreparties et objets d’opération.
5. Catégorisation (optionnelle) via l’arbre de catégories.
6. Export Excel avec styles sur les dates et montants.

Pour plus de détails, consultez la référence API et le guide de démarrage rapide.
