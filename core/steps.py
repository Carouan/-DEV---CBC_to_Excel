# steps.py

import re
import unicodedata
import pandas as pd
from config import operation_types
from categories import build_category_tree_from_csv
from naming import get_output_filename_and_period
from excel_styles import apply_styles

def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.upper()
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized

_OP_TYPE_PATTERNS = [
    (op_type, re.compile(re.escape(_normalize_text(op_type))))
    for op_type in operation_types
]

def step1_clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Étape 1 : Suppression des colonnes inutiles
    columns_to_remove = [
        "Numéro de compte", "Nom de la rubrique", "Nom", "Devise",
        "Date", "Solde", "crédit", "débit",
        "numéro de compte contrepartie", "BIC contrepartie",
        "Adresse contrepartie", "communication structurée"
    ]
    df = df.drop(columns=columns_to_remove, errors='ignore')
    return df        

def step2_create_new_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Étape 2 : Création des nouvelles colonnes
    df["Type d’opération"] = ""
    df["Projet"] = ""
    df["Catégorie"] = ""
    df["Couvert par le subside"] = ""
    df["Lien document"] = ""
    df["Pièce n°"] = ""
    df["Remarque"] = ""
    return df

def step3_rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Étape 3 : Renommage des colonnes existantes
    df = df.rename(columns={
        "Numéro de l'extrait": "N°extrait",
        "Valeur": "Date",
        "Nom contrepartie": "Contrepartie",
        "Communication libre": "Objet de l’opération"
    })
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df["Montant"] = (
    df["Montant"]
    .astype(str)                  # au cas où ce serait déjà un float
    .str.replace(",", ".", regex=False)   # remplacer virgule par un point
    .str.replace("\u00A0", "", regex=True)  # enlever espaces insécables
    )
    df["Montant"] = pd.to_numeric(df["Montant"], errors="coerce")
    return df

def step4_reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Étape 4 : Réorganisation de l'ordre des colonnes
    columns_order = [
        "N°extrait", "Date", "Type d’opération", "Contrepartie",
        "Objet de l’opération", "Catégorie", "Projet", "Montant",
        "Couvert par le subside", "Pièce n°", "Lien document", "Remarque", "Description"
    ]
    # Éviter les KeyError si certaines colonnes n’existent pas
    columns_order = [col for col in columns_order if col in df.columns]
    df = df[columns_order]
    return df

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def step5_find_operation_type(df: pd.DataFrame) -> pd.DataFrame:
    # Étape 5 : Exécuter fonction "find_operation_type
    if "Description" not in df.columns:
        return df

    normalized_descriptions = df["Description"].apply(_normalize_text)

    def match_op_type(normalized_description: str) -> str:
        for op_type, pattern in _OP_TYPE_PATTERNS:
            if pattern.search(normalized_description):
                return op_type
        return None
    df.loc[:, "Type d’opération"] = normalized_descriptions.apply(match_op_type)
    #df["Type d’opération"] = df["Description"].apply(match_op_type)
    return df

def step6_fill_contrepartie_ET_objFact(df: pd.DataFrame) -> pd.DataFrame:
    """
    Étape 6 :
    1) Si 'Contrepartie' est vide (ou juste des espaces),
       alors on regarde la 'Description' (et éventuellement 'Type d’opération')
       pour remplir 'Contrepartie' et 'Objet de l’opération'.
    2) Sinon, on laisse tout inchangé.
    """

    def fill_contrepartie_et_objet(row):
        # On part des valeurs existantes
        current_contrepartie = row.get("Contrepartie", "")
        current_objet = row.get("Objet de l’opération", "")

        # Sécurité : si ce ne sont pas des chaînes de caractères
        if not isinstance(current_contrepartie, str):
            current_contrepartie = ""
        if not isinstance(current_objet, str):
            current_objet = ""

        # Vérifie si Contrepartie est vide ou juste espaces
        if current_contrepartie.strip() == "":
            desc = row.get("Description", "")
            normalized_desc = _normalize_text(desc)
            # eventuellement, si tu as besoin du type
            # op_type = row.get("Type d'opération", "")

            # -- CAS 1 : CONSOMMATION ou FORFAIT
            #    => Contrepartie = "COMPTE D'ENTREPRISE CBC"
            #    => Objet de l’opération = "Frais bancaires"
            if normalized_desc.startswith("CONSOMMATION") or normalized_desc.startswith("FORFAIT"):
                current_contrepartie = "COMPTE D'ENTREPRISE CBC"
                current_objet = "Frais bancaires"

            # -- CAS 2 : DECOMPTE
            #    => Contrepartie = "MASTERCARD BUSINESS BLUE CBC"
            #    => Objet = "Frais bancaires"
            elif normalized_desc.startswith("DECOMPTE"):
                current_contrepartie = "MASTERCARD BUSINESS BLUE CBC"
                current_objet = "Frais bancaires"

            # -- CAS 3 : DOMICILIATION
            #    => Contrepartie = ce qui est entre "CREANCIER       : " et "REF."
            #    => Objet de l’opération = ce qui vient après "COMMUNICATION   :"
            elif normalized_desc.startswith("DOMICILIATION"):
                part_creancier = ""
                part_comm = ""

                # Chercher la zone CREANCIER
                marker_creancier = "CREANCIER       : "
                marker_ref = "REF."
                start_pos = desc.find(marker_creancier)
                if start_pos != -1:
                    start_creancier = start_pos + len(marker_creancier)
                    end_creancier = desc.find(marker_ref, start_creancier)
                    if end_creancier != -1:
                        part_creancier = desc[start_creancier:end_creancier].strip()

                # Chercher la zone COMMUNICATION
                marker_comm = "COMMUNICATION   :"
                pos_comm = desc.find(marker_comm)
                if pos_comm != -1:
                    # Tout ce qui vient après "COMMUNICATION   :"
                    part_comm = desc[pos_comm + len(marker_comm):].strip()

                if part_creancier:
                    current_contrepartie = part_creancier
                else:
                    current_contrepartie = "(Contrepartie DOM introuvable)"

                if part_comm:
                    current_objet = part_comm
                else:
                    current_objet = "(Communication DOM introuvable)"

            # -- CAS 4 : PAIEMENT*
            #    => On récupère la partie entre "HEURES " et " AVEC"
            elif normalized_desc.startswith("PAIEMENT"):
                if "HEURES " in desc and " AVEC" in desc:
                    start = desc.index("HEURES ") + len("HEURES ")
                    end = desc.index(" AVEC", start)
                    current_contrepartie = desc[start:end].strip()

                    # Exemple : on peut décider de mettre un objet par défaut 
                    if current_objet.strip() == "":
                        current_objet = "Achats"

                else:
                    current_contrepartie = "(Paiement non géré)"

            else:
                # Cas par défaut
                current_contrepartie = "(Non géré)"
                # On peut décider de laisser l'Objet tel quel ou le modifier
                if current_objet.strip() == "":
                    current_objet = "(Non géré)"

        # On retourne le tuple (Contrepartie, Objet)
        return (current_contrepartie, current_objet)

    # On applique la fonction à chaque ligne, et on répartit dans 2 colonnes
    df["Contrepartie"], df["Objet de l’opération"] = zip(
        *df.apply(fill_contrepartie_et_objet, axis=1)
    )

    return df

def step7_drop_description(df: pd.DataFrame) -> pd.DataFrame:
    """
    Étape 7 : Supprime la colonne 'Description' si elle existe encore.
    """
    df = df.drop(columns=["Description"], errors="ignore")
    return df

def step8_fill_categorie(df, category_tree_file):
    """
    Étape 8 : Associer des catégories à chaque ligne selon le type d'opération. 
    La contrepartie ou l'objet de l'opération.
    """
    # Charger l'arbre de catégories
    tree = build_category_tree_from_csv(category_tree_file)

    # Associer les catégories
    def assign_category(row):
        operation = row.get("Type d'opération", "")
        if not operation:
            return None
        category = tree.search(operation)
        if not category:
            # Déterminer si c'est une dépense (montant négatif) ou une recette
            montant = row.get("Montant", 0)
            if montant < 0:
                return "D-Autres"
            else:
                return "R-Autres"
        return category

    # Appliquer la fonction sur chaque ligne
    df["Catégorie"] = df.apply(assign_category, axis=1)
    return df


def step9_export_excel(df: pd.DataFrame, input_file: str) -> pd.DataFrame:
    """
    Étape 9 :
    1) Génère le nom du fichier Excel à partir du CSV d’entrée (via naming.py)
       et de la période calculée dans le df.
    2) Détermine aussi le nom de feuille (sheet_name) en se basant sur la période.
    3) Exporte le df en Excel.
    """
    out_file_name, period = get_output_filename_and_period(input_file, df)

# Nettoyons la 'period' pour qu’elle soit valide en nom de sheet (éviter [] ou /)
    sheet_name = period.replace("[", "").replace("]", "")
    sheet_name = sheet_name.replace("/", ".").replace("\\", ".")
    sheet_name = sheet_name[:31]  # Excel limite souvent les noms de feuille à 31 caractères max

    if "Type d’opération" in df.columns:
        df["Type d’opération"] = df["Type d’opération"].fillna("Non trouvé")

    df.to_excel(out_file_name, index=False, sheet_name=sheet_name, engine="xlsxwriter") #utiliser openpyxl ou xlsxwriter
    # Appliquer les styles Excel
    apply_styles(out_file_name, date_column=2, montant_column=8)
    
    print(f"Fichier Excel généré : {out_file_name} (feuille : {sheet_name})")

    return df
