import pandas as pd
from trie import CategoryTrie, load_categories_into_trie


def save_trie_to_csv(trie, output_file="categories.csv"):
    """
    Sauvegarde le contenu du Trie dans un fichier CSV.
    """
    rows = []
    def traverse(node, prefix=""):
        if node.category:
            rows.append({"Catégorie": node.category, "Associations": prefix})
        for char, child_node in node.children.items():
            traverse(child_node, prefix + char)

    traverse(trie.root)
    df = pd.DataFrame(rows)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Trie sauvegardé dans {output_file}")

def test_trie():
    """
    Script indépendant pour tester et enrichir le Trie.
    """
    # Charger le Trie à partir d'un fichier existant
    trie = load_categories_into_trie("categories.csv")

    while True:
        print("\nMenu :")
        print("1. Tester une contrepartie")
        print("2. Ajouter une nouvelle association")
        print("3. Sauvegarder et quitter")

        choice = input("Choisissez une option (1/2/3) : ").strip()
        if choice == "1":
            contrepartie = input("Entrez une contrepartie à tester : ").strip()
            category = trie.search(contrepartie)
            if category:
                print(f"Catégorie trouvée : {category}")
            else:
                print("Aucune catégorie trouvée pour cette contrepartie.")

        elif choice == "2":
            contrepartie = input("Entrez une nouvelle contrepartie : ").strip()
            category = input("Entrez la catégorie associée : ").strip()
            trie.insert(contrepartie, category)
            print(f"Association ajoutée : '{contrepartie}' -> '{category}'")

        elif choice == "3":
            save_trie_to_csv(trie)
            print("Fin du test.")
            break

        else:
            print("Option invalide. Veuillez choisir entre 1, 2 ou 3.")

if __name__ == "__main__":
    test_trie()
