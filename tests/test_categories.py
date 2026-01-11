from categories import build_category_tree_from_csv

def main():
    # Charger un arbre de test à partir d'un fichier CSV
    csv_file = "categories_test.csv"  # Le fichier de test doit exister
    tree = build_category_tree_from_csv(csv_file)

    # Tester la recherche de catégories
    test_operations = ["ACHAT", "COTISATION", "CARTE", "DON", "TRANSPORT"]
    for operation in test_operations:
        category = tree.search(operation)
        if category:
            print(f"Opération '{operation}' trouvée dans la catégorie : {category}")
        else:
            print(f"Opération '{operation}' n'est associée à aucune catégorie.")

if __name__ == "__main__":
    main()
