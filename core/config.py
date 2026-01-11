# config.py

# Valeurs de config :
DEFAULT_ENCODING = "latin-1"
DELIMITER = ";"

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
    "PAIEMENT CARBURANT PAR BANCONTACT"
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

# Liste des Catégories :
categories = {
    # S’il y a un 2ᵉ dictionnaire ou d’autres constantes
}
