"""Configuration values for CBC to Excel."""

from __future__ import annotations

from importlib import resources

# Valeurs de config
DEFAULT_ENCODING = "latin-1"
DELIMITER = ";"
DEFAULT_OUTPUT_DIR = "data/out_xlsx"


def _default_category_file() -> str:
    """Return the default category CSV path bundled with the package.

    Falls back to the historical data/ path if package resources are missing.
    """
    try:
        return str(resources.files("core.resources").joinpath("categories.csv"))
    except (AttributeError, ModuleNotFoundError, FileNotFoundError):
        return "data/categories.csv"


DEFAULT_CATEGORY_FILE = _default_category_file()

# Liste des types d'opérations
operation_types = [
    "DOMICILIATION EUROPEENNE",
    "FORFAIT",
    "ORDRE PERMANENT",
    "PAIEMENT ACHAT PAR BANCONTACT",
    "PAIEMENT ACHATS PAR MAESTRO",
    "PAIEMENT PAR BANCONTACT",
    "PAIEMENT PAR MAESTRO",
    "PAYMENT MOBILE",
    "RETRAIT D'ESPECES",
    "VIREMENT DE",
    "VIREMENT INSTANTANE DE",
    "VIREMENT INSTANTANE VERS",
    "VIREMENT VERS",
    "VIREMENT EUROPEEN DE",
    "CONSOMMATION",
    "RETRAIT D'ARGENT",
    "INDEMNISATION SUITE AUX OPÉRATIONS",
    "DECOMPTE",
    "PAIEMENT CARBURANT PAR BANCONTACT",
]

# Dictionnaire de mapping pour les différents comptes en banque CBC (perso et FDD)
cptsCBC = {
    "BE50732047041718": "FDD",
    "Mastercard Business Blue CBC": "FDD_Visa",
    "BE92732062203323": "CBC_Seb",
    "BE41732062192310": "CBC_Commun",
    "BE67742045110287": "CBC_EpargneCom",
    "Carte de crédit CBC": "CBC_Visa",
    "BE06732062746422": "CBC_Mimi",
    "BE78742045110186": "CBC_EpargneMimi",
    "BE83734032485915": "KBC_Commun",
    "": "KBC_Visa",
}

# Liste des Catégories
categories: dict[str, list[str]] = {
    "Revenus": [
        "Salaire",
        "Remboursement",
        "Virement reçu",
        "Indemnisation",
    ],
    "Dépenses fixes": [
        "Loyer",
        "Électricité",
        "Eau",
        "Internet",
        "Téléphone",
        "Assurance",
        "Abonnement",
    ],
    "Courses": [
        "Supermarché",
        "Épicerie",
        "Alimentation",
    ],
    "Loisirs": [
        "Restaurant",
        "Café",
        "Cinéma",
        "Voyage",
        "Sport",
        "Jeux vidéo",
    ],
}
