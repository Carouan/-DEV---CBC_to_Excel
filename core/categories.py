class CategoryNode:
    def __init__(self, category_name):
        self.name = category_name
        self.left = None
        self.right = None
        self.operations = set()

    def add_operation(self, operation):
        self.operations.add(operation)

    def search_category(self, operation):
        if operation in self.operations:
            return self.name
        elif self.left and operation < self.name:
            return self.left.search_category(operation)
        elif self.right and operation > self.name:
            return self.right.search_category(operation)
        return None


class CategoryTree:
    def __init__(self):
        self.root = None

    def insert(self, category_name, operations):
        if not self.root:
            self.root = CategoryNode(category_name)
            self.root.operations.update(operations)
        else:
            self._insert_node(self.root, category_name, operations)

    def _insert_node(self, node, category_name, operations):
        if category_name < node.name:
            if not node.left:
                node.left = CategoryNode(category_name)
                node.left.operations.update(operations)
            else:
                self._insert_node(node.left, category_name, operations)
        elif category_name > node.name:
            if not node.right:
                node.right = CategoryNode(category_name)
                node.right.operations.update(operations)
            else:
                self._insert_node(node.right, category_name, operations)

    def search(self, operation):
        if self.root:
            return self.root.search_category(operation)
        return None

    def find_node(self, category_name):
        current = self.root
        while current:
            if category_name == current.name:
                return current
            if category_name < current.name:
                current = current.left
            else:
                current = current.right
        return None


def build_category_tree_from_csv(file_path):
    """
    Charge un arbre binaire à partir d'un fichier CSV contenant les catégories et leurs opérations associées.
    Exemple de fichier CSV :
    Catégorie;Opérations
    D-Alimentaire;ACHAT,CARTE,COURSES
    R-Cotisation;COTISATION,DON

    categories.csv
    """
    import csv
    tree = CategoryTree()


    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            category = row["Catégorie"]
            operations = row["Opérations"].split(",")
            tree.insert(category, operations)
    return tree
