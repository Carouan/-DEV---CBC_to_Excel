"""Interactive utility to manage category CSV files."""

from __future__ import annotations

import csv

from .categories import CategoryTree, build_category_tree_from_csv

CATEGORY_FILE = "categories.csv"


def display_menu() -> None:
    """Display the interactive menu."""
    print("\nGestion des Catégories")
    print("=======================")
    print("1. Afficher toutes les catégories")
    print("2. Rechercher une catégorie par opération")
    print("3. Ajouter une nouvelle catégorie")
    print("4. Ajouter une opération à une catégorie existante")
    print("5. Quitter")
    print("=======================")


def display_categories(tree: CategoryTree) -> None:
    """Print all categories stored in the tree."""
    print("\nListe des catégories :")

    def _traverse(node):
        if node:
            _traverse(node.left)
            print(f"- {node.name}: {', '.join(node.operations)}")
            _traverse(node.right)

    if tree.root:
        _traverse(tree.root)
    else:
        print("Aucune catégorie disponible.")


def search_category(tree: CategoryTree) -> None:
    """Prompt for an operation name and display the matching category."""
    operation = input("\nEntrez le type d'opération à rechercher : ").strip()
    category = tree.search(operation)
    if category:
        print(f"L'opération '{operation}' est associée à la catégorie : {category}")
    else:
        print(f"L'opération '{operation}' n'est associée à aucune catégorie.")


def add_new_category() -> tuple[str, list[str]]:
    """Prompt for a new category and its operations."""
    category_name = input("\nEntrez le nom de la nouvelle catégorie : ").strip()
    operations = (
        input("Entrez les types d'opérations associés, séparés par des virgules : ")
        .strip()
        .split(",")
    )
    return category_name, operations


def add_operation_to_category(tree: CategoryTree) -> tuple[str, list[str]]:
    """Prompt for a category and operations to append."""
    category_name = input("\nEntrez le nom de la catégorie existante : ").strip()
    new_operations = (
        input("Entrez les nouvelles opérations à ajouter, séparées par des virgules : ")
        .strip()
        .split(",")
    )
    return category_name, new_operations


def save_tree_to_csv(tree: CategoryTree, file_path: str) -> None:
    """Persist the category tree to a CSV file.

    Args:
        tree: Category tree to serialize.
        file_path: Destination CSV path.
    """
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Catégorie", "Opérations"])

        def _traverse_and_save(node):
            if node:
                _traverse_and_save(node.left)
                writer.writerow([node.name, ",".join(node.operations)])
                _traverse_and_save(node.right)

        _traverse_and_save(tree.root)


def main() -> None:
    """Run the interactive category manager."""
    try:
        tree = build_category_tree_from_csv(CATEGORY_FILE)
    except FileNotFoundError:
        print(f"\nFichier {CATEGORY_FILE} introuvable. Création d'un nouvel arbre...")
        tree = CategoryTree()

    while True:
        display_menu()
        choice = input("\nVotre choix : ").strip()

        if choice == "1":
            display_categories(tree)
        elif choice == "2":
            search_category(tree)
        elif choice == "3":
            category_name, operations = add_new_category()
            tree.insert(category_name, operations)
            print(f"\nCatégorie '{category_name}' ajoutée avec succès.")
        elif choice == "4":
            category_name, new_operations = add_operation_to_category(tree)
            existing_node = tree.find_node(category_name)
            if existing_node:
                for operation in new_operations:
                    existing_node.add_operation(operation)
                print(
                    f"\nOpérations ajoutées avec succès à la catégorie '{category_name}'."
                )
            else:
                print(f"\nLa catégorie '{category_name}' n'existe pas.")
        elif choice == "5":
            save_tree_to_csv(tree, CATEGORY_FILE)
            print("\nModifications sauvegardées. À bientôt !")
            break
        else:
            print("\nChoix invalide, veuillez réessayer.")


if __name__ == "__main__":
    main()
