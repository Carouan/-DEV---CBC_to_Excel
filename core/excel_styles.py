from openpyxl import load_workbook
from openpyxl.styles import NamedStyle

def apply_styles(file_name: str, date_column: int, montant_column: int):
    """
    Applique les styles aux colonnes spécifiées dans un fichier Excel.
    
    Args:
        file_name (str): Le chemin du fichier Excel à modifier.
        date_column (int): Index (1-based) de la colonne contenant les dates.
        montant_column (int): Index (1-based) de la colonne contenant les montants.
    """
    # Charger le fichier Excel existant
    wb = load_workbook(file_name)
    ws = wb.active

    # Définir les styles
    date_style = NamedStyle(name="date_style", number_format="DD-MM-YY")
    montant_style = NamedStyle(name="montant_style", number_format="#,##0.00 €;[RED]- #,##0.00 €")

    # Appliquer les styles aux colonnes
    for row in ws.iter_rows(min_row=2, min_col=date_column, max_col=date_column):
        for cell in row:
            cell.style = date_style

    for row in ws.iter_rows(min_row=2, min_col=montant_column, max_col=montant_column):
        for cell in row:
            cell.style = montant_style

    # Sauvegarder le fichier avec les styles appliqués
    wb.save(file_name)
    print(f"Styles appliqués et fichier sauvegardé : {file_name}")
