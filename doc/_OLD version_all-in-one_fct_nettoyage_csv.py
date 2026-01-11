import pandas as pd

# Charger le fichier CSV fourni
file_path = "export test 10-24 FDD pour script.csv"  # Chemin vers votre fichier
df = pd.read_csv(file_path, encoding='latin-1', delimiter=';')  # Adapter le délimiteur si besoin

#Etape 1 - Supprimer des colonnes inutiles
#Etape 2 - Création des nouvelles colonnes
#Etape 3 - Renommer colonnes
#Etape 4 - Réordonner les colonnes
#Etape 5 - Exécuter fonction "find_operation_type"
#Etape 6 - Exécuter fonction "fill_contrepartie"
#Etape 7 - Exécuter fonction "fill_objFact"
#Etape 8 - Supprimer colonne "Description"
#Etape 9 - Exécuter fonction "categorie"
#Etape 10 - Générer le fichier Excel


def step1_clean_columns(df):
    """
    Étape 1 : Suppression des colonnes inutiles
    """
    columns_to_remove = [
        "Numéro de compte", "Nom de la rubrique", "Nom", "Devise",
        "Date", "Solde", "crédit", "débit",
        "numéro de compte contrepartie", "BIC contrepartie",
        "Adresse contrepartie", "communication structurée"
    ]
    df = df.drop(columns=columns_to_remove, errors='ignore')
    return df

def step2_create_new_columns(df):
    """
    Étape 2 : Création des nouvelles colonnes
    """
    df["Type d'opération"] = ""
    df["Projet"] = ""
    df["Catégorie"] = ""
    df["Couvert par le subside"] = ""
    df["Lien document"] = ""
    df["Pièce n°"] = ""
    df["Remarque"] = ""
    return df

def step3_rename_columns(df):
    """
    Étape 3 : Renommage des colonnes existantes
    """
    df = df.rename(columns={
        "Numéro de l'extrait": "N°extrait",
        "Valeur": "Date",
        "Nom contrepartie": "Contrepartie",
        "Communication libre": "Objet de l’opération"
    })
    return df

def step4_reorder_columns(df):
    """
    Étape 4 : Réorganisation de l'ordre des colonnes
    """
    columns_order = [
        "N°extrait", "Date", "Type d'opération", "Contrepartie",
        "Objet de l’opération", "Catégorie", "Projet", "Montant",
        "Couvert par le subside", "Pièce n°", "Lien document", "Remarque", "Description"
    ]
    # Éviter les KeyError si certaines colonnes n’existent pas
    columns_order = [col for col in columns_order if col in df.columns]
    df = df[columns_order]
    return df

def step5_find_operation_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Étape 5 : Exécuter fonction "find_operation_type
    """
    def match_op_type(description: str) -> str:
        # Pas besoin de .upper() si la colonne 'Description' est déjà en MAJUSCULES.
        for op_type in operation_types:
            if op_type in description:
                return op_type
        return "*** NOT FIND ***"
    
    df["Type d’opération"] = df["Description"].apply(match_op_type)
    return df

# Fonction pour extraire des informations spécifiques selon le type d'opération
def extract_additional_info(desc_str, operation_type):
    desc_str = desc_str.upper()  # Insensibilité à la casse
    extracted_info = ""
    card_num = ""

    if operation_type == "DOMICILIATION EUROPEENNE":
        if "CREANCIER" in desc_str:
            extracted_info = desc_str.split("CREANCIER")[1].split(":")[1].strip()
    elif operation_type == "ORDRE PERMANENT":
        if "BANQUIER BENEFICIAIRE" in desc_str:
            extracted_info = desc_str.split("BANQUIER BENEFICIAIRE:")[1].strip()
    elif operation_type == "PAIEMENT PAR BANCONTACT":
        if "AVEC" in desc_str:
            extracted_info = desc_str.split("AVEC")[1].strip()
        if "TITULAIRE:" in desc_str:
            card_num = desc_str.split("TITULAIRE:")[1].strip()
    elif operation_type == "VIREMENT DE":
        if "BANQUIER DONNEUR D'ORDRE:" in desc_str:
            extracted_info = desc_str.split("BANQUIER DONNEUR D'ORDRE:")[1].strip()
    elif operation_type == "VIREMENT INSTANTANE VERS":
        if "BANQUIER BENEFICIAIRE:" in desc_str:
            extracted_info = desc_str.split("BANQUIER BENEFICIAIRE:")[1].strip()
    return extracted_info, card_num

# Appliquer les extractions
if "Description" in df.columns:
    df["TYPE OPERATION"] = df["Description"].apply(find_operation_type)
    df["CONTREPARTIE"] = df.apply(
        lambda row: extract_additional_info(row["Description"], row["TYPE OPERATION"])[0], axis=1
    )
    df["OBJET DE LA FACTURE"] = df.apply(
        lambda row: extract_additional_info(row["Description"], row["TYPE OPERATION"])[0], axis=1
    )


#Etape 8 - Supprimer colonne "Description"
df = df.drop(columns=["Description"], errors="ignore")


# Afficher un aperçu des résultats
print(df[["TYPE OPERATION", "CONTREPARTIE", "OBJET DE LA FACTURE"]])

# Exporter les résultats vers un fichier Excel pour vérification

# Création du nom de fichier de sortie.


# Analyser le nom du csv et la colonne date.

output_path = "fichier_nettoye_test.xlsx"  # Chemin de sortie
df.to_excel(output_path, index=False)

print(f"Le fichier nettoyé a été exporté sous le nom : {output_path}")


# Exemple d’utilisation avec un DataFrame df :
# df = pd.read_csv("votre_fichier.csv", sep=";")
df = step1_clean_columns(df)      # Étape 1
df = step2_create_new_columns(df) # Étape 2
df = step3_rename_columns(df)     # Étape 3
df = step4_reorder_columns(df)    # Étape 4







"""
(( exemple de noms de fichiers csv
export_BE50732047041718_20250106_1105
export_Mastercard Business Blue CBC_20241230_1428
export_BE92732062203323_20240909_1414
export_BE41732062192310_20240909_1413
export_Carte de crédit CBC_20250109_1059
))
"""
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
"""
Analyse du formatage du nom de fichier du csv
    - Commence toujours par "export_"
    - Puis numéro ou nom de la carte
    --> Rechercher correspondance dans le dictionnaire cptsCBC
    - "_"
    - Date de génération du fichier (format anglais - yyyymmdd)
    - "_"
    - Heure de génération du fichier (hhmm)


Le nom de fichier de sortie doit être du format : nomCompte_Période couverte_date d'export

nomCompte = chercher correspondance dans le dictionnaire cptsCBC
Période couverte = rechercher dans la colonne "Date" les dates les plus ancienne et récente afin de déterminer la période.

Exemples : 
1) plus ancienne opération = 02/11/2023 et plus récente = 12/02/24  ==> Période = [02/11/2023-12/02/24]
2) plus ancienne opération = 02/01/2023 et plus récente = 27/11/23 ==> Période = [02/01-27/11(23)]
3) plus ancienne opération = 02/03/2023 et plus récente = 27/03/23 ==> Période = [02-27(03/23)]

date d'export = se baser sur la date provenant du nom du fichier et la convertir au format belge (dd/mm/yy)

Nommer la feuille contenant le tableau créé par le script avec la période concernée.





"""

#Etape 6 - Exctraction informations "fill_contrepartie_objFact"



IF description startwith CONSOMMATION OU FORFAIT
    Alors 
    (Contrepartie = "COMPTE D'ENTREPRISE CBC") ET (Objet de l'opération = "Frais bancaires")

ELIF description startwith DECOMPTE
    Alors 
    (Contrepartie = "MASTERCARD BUSINESS BLUE CBC") ET (Objet de l'opération = "Frais bancaires")

ELIF description startwith DOMICILIATION
    Alors 
    (Contrepartie = ce qui est entre "CREANCIER       : " et "REF.") ET (Objet de l'opération = ce qui viens après : "COMMUNICATION   :")
elif op_type.startswith("PAIEMENT"):
    # Ex: repérer la partie entre "HEURES " et " AVEC"
    if "HEURES " in desc and " AVEC" in desc:
        start = desc.index("HEURES ") + len("HEURES ")
        end = desc.index(" AVEC", start)
        current_contrepartie = desc[start:end].strip()






DOMICILIATION EUROPEENNE             01-10 CREANCIER       : BLAST LE SOUFFLE DE L'INFO REF. CREANCIER  : STR16NAQWVI2LVNQ4GRSSRANDISZAWT2AZ REFERENCE MANDAT: 95GA1LXVETSLGEE7 COMMUNICATION   : WWW.BLAST-INFO.FR
DOMICILIATION EUROPEENNE             01-10 CREANCIER       : EDF LUMINUS NV REF. CREANCIER  : D2024000777/196 REFERENCE MANDAT: 9000209407289 COMMUNICATION   : 6.812.912/CSM 2024 334.885
DOMICILIATION EUROPEENNE             09-10 CREANCIER       : LUMINUS SA REF. CREANCIER  : 002172964479 REFERENCE MANDAT: 0087005117182 COMMUNICATION   : LUMINUS ACOMPTE 7633842857
DOMICILIATION EUROPEENNE             28-10 CREANCIER       : PROXIMUS REF. CREANCIER  : 9011756537 REFERENCE MANDAT: B014262143 COMMUNICATION   : 007406328881


Sachant que pour les 4 lignes ci dessus il faut extraire respectivement pour :
Contrepartie | Objet de l'opération
- BLAST LE SOUFFLE DE L'INFO | WWW.BLAST-INFO.FR
- EDF LUMINUS NV | 6.812.912/CSM 2024 334.885
- LUMINUS SA | LUMINUS ACOMPTE 7633842857
- PROXIMUS | 007406328881


Donc pour la partie contrepartie il faut extraire ce qui est entre "CREANCIER       : " et "REF."
Et pour la partie objet de l'opération il faut prendre tout ce qui viens après : "COMMUNICATION   :"
