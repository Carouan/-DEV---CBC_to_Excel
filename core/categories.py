"""Category tree utilities for CBC transaction classification."""

from __future__ import annotations

import csv
from typing import Iterable


class CategoryNode:
    """Binary tree node storing a category and its operations."""

    def __init__(self, category_name: str) -> None:
        self.name = category_name
        self.left: CategoryNode | None = None
        self.right: CategoryNode | None = None
        self.operations: set[str] = set()

    def add_operation(self, operation: str) -> None:
        """Add a new operation label to this category."""
        self.operations.add(operation)

    def search_category(self, operation: str) -> str | None:
        """Search for the category containing the given operation.

        The tree is ordered by category name, so we must traverse all nodes
        when searching by operation.
        """
        if operation in self.operations:
            return self.name
        if self.left:
            found = self.left.search_category(operation)
            if found:
                return found
        if self.right:
            found = self.right.search_category(operation)
            if found:
                return found
        return None


class CategoryTree:
    """Binary search tree that maps operations to categories."""

    def __init__(self) -> None:
        self.root: CategoryNode | None = None

    def insert(self, category_name: str, operations: Iterable[str]) -> None:
        """Insert a new category and associated operations."""
        if not self.root:
            self.root = CategoryNode(category_name)
            self.root.operations.update(operations)
        else:
            self._insert_node(self.root, category_name, operations)

    def _insert_node(
        self, node: CategoryNode, category_name: str, operations: Iterable[str]
    ) -> None:
        """Recursive helper to insert nodes in the tree."""
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

    def search(self, operation: str) -> str | None:
        """Return the category for the operation, if present."""
        if self.root:
            return self.root.search_category(operation)
        return None

    def find_node(self, category_name: str) -> CategoryNode | None:
        """Return the node that matches a category name."""
        current = self.root
        while current:
            if category_name == current.name:
                return current
            if category_name < current.name:
                current = current.left
            else:
                current = current.right
        return None


def build_category_tree_from_csv(file_path: str) -> CategoryTree:
    """Load categories and operations from a CSV file into a tree.

    Args:
        file_path: Path to the CSV file containing category definitions.

    Returns:
        CategoryTree populated with the CSV content.
    """
    tree = CategoryTree()

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            category = row["Catégorie"]
            operations = row["Opérations"].split(",")
            tree.insert(category, operations)
    return tree
