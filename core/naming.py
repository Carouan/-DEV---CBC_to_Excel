# naming.py
import os

import pandas as pd

from .config import cptsCBC

def parse_filename(file_name: str):
    base_name = os.path.basename(file_name)
    root, extension = os.path.splitext(base_name)
    parts = root.split("_", maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Nom de fichier non conforme : {file_name}")
    prefix = parts[0]        # "export"
    account_part = parts[1]  # "BE50732047041718" ou "Mastercard Business Blue CBC"
    date_part = parts[2]     # "20250106"
    time_part = parts[3]     # "1105"
    return account_part, date_part, time_part, extension

def format_export_date(date_yyyymmdd: str) -> str:
    year = date_yyyymmdd[0:4]
    month = date_yyyymmdd[4:6]
    day = date_yyyymmdd[6:8] 
    return f"{year}.{month}.{day}"

def build_period_string(df):
    if "Date" not in df.columns:
        return "[no date]"
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    if pd.isnull(min_date) or pd.isnull(max_date):
        return "[date non définie]"
    # Format complet
    fmt_full = "%d.%m.%Y"

    # Si min_date et max_date sont dans même année ET même mois 
    if (min_date.month == max_date.month) and (min_date.year == max_date.year):
        # 1er date : 02/03/2023 | 2eme date : 27/03/2023
        # ex: [02-27(03.2023)]
        day_min = min_date.day
        day_max = max_date.day
        month_year = min_date.strftime("%m.%y")
        return f"[{day_min}-{day_max}({month_year})]"
    # Si min_date et max_date sont dans la même année
    elif (min_date.year == max_date.year):
        # 1er date : 02/03/2023 | 2eme date : 27/05/2023
        # ex: [02.03-27.05(2023)]
        day_min = min_date.day
        day_max = max_date.day
        month_min = min_date.strftime("%m")
        month_max = max_date.strftime("%m")
        year = min_date.year
        return f"[{day_min}.{month_min}-{day_max}.{month_max}({year})]"
    else:
        dmin_str = min_date.strftime(fmt_full)
        dmax_str = max_date.strftime(fmt_full)
        return f"[{dmin_str}-{dmax_str}]"

def build_new_filename(date_export_fr: str, nomCompte: str, period: str):
    # Pour éviter problèmes de / dans le nom de fichier
    safe_period = period.replace("/", "-").replace(":", "-")
    return f"{safe_period}_{nomCompte}_{date_export_fr}.xlsx"

def get_nom_compte(account_part: str) -> str:
    return cptsCBC.get(account_part, account_part)

def get_output_filename(input_file: str, df: pd.DataFrame) -> str:
    """
    Fonction principale pour générer le nom de fichier de sortie.
    1) Parse le nom du CSV (input_file)
    2) Calcule la période min/max dans df["Date"]
    3) Convertit date d'export
    4) Fait le mapping compte
    5) Construit la string finale
    Retourne le nom de fichier final (str).
    """
    # 1. Analyser le nom d’entrée
    account_part, date_part, time_part, extension = parse_filename(input_file)
    # 2. Calculer la période (à partir des dates du DataFrame)
    period = build_period_string(df)
    # 3. Convertir la date d’export (ex: "20250106" → "06/01/25")
    date_export_fr = format_export_date(date_part)
    # 4. Trouver le nom de compte
    nomCompte = get_nom_compte(account_part)
    # 5. Construire le nom final
    out_file_name = build_new_filename(date_export_fr, nomCompte, period)
    return out_file_name

def get_output_filename_and_period(input_file: str, df: pd.DataFrame):
    """
    Renvoie (out_file_name, period)
    out_file_name = le nom final du fichier.
    period = la chaîne [02.03-27.03(23)] pour usage éventuel en nom de feuille.
    """
    account_part, date_part, time_part, extension = parse_filename(input_file)
    period = build_period_string(df)      # ex: [02-27(03/23)]
    date_export_fr = format_export_date(date_part)
    nomCompte = get_nom_compte(account_part)
    out_file_name = build_new_filename(date_export_fr, nomCompte, period)

    return out_file_name, period

# *************  TEST INDEPENDANT   ********************* 
def main():
    # Parse le nom
    account_part, date_part, time_part, ext = parse_filename(input_file)
    # Calculer la période
    period = build_period_string(df)
    # Convertir la date
    date_export_fr = format_export_date(date_part)
    # Trouver le nomCompte dans le dico cptsCBC
    nomCompte = cptsCBC.get(account_part, account_part)
    # Construire le nom de fichier final
    out_file_name = build_new_filename(date_export_fr, nomCompte, period)
    return out_file_name

# -- Optionnel : un bloc de test direct --
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python naming.py <fichier.csv>")
        sys.exit(1)
    test_file = sys.argv[1]
    # On peut charger un faux DataFrame ou un vrai CSV
    df_test = pd.DataFrame({
        "Date": pd.to_datetime(["2024-01-13", "2024-02-22"]) # ex: 13 janv 24 et 22 fév 24
    })
    result_name = get_output_filename_and_period(test_file, df_test)
    print(f"Nom de fichier généré : {result_name}")
