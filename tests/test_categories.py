import csv
from pathlib import Path

from core.categories import build_category_tree_from_csv


def test_build_category_tree_from_csv(tmp_path: Path) -> None:
    csv_path = tmp_path / "categories.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(["Catégorie", "Opérations"])
        writer.writerow(["D-Alimentaire", "ACHAT,CARTE,COURSES"])
        writer.writerow(["R-Cotisation", "COTISATION,DON"])
        writer.writerow(["Z-Autres", "AAA"])

    tree = build_category_tree_from_csv(str(csv_path))

    assert tree.search("ACHAT") == "D-Alimentaire"
    assert tree.search("DON") == "R-Cotisation"
    assert tree.search("AAA") == "Z-Autres"
    assert tree.search("INCONNU") is None
