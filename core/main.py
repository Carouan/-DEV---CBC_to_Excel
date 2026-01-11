import argparse
import pandas as pd
from steps import (
    validate_schema,
    step1_clean_columns,
    step2_create_new_columns,
    step3_rename_columns,
    step4_reorder_columns,
    step5_find_operation_type,
    step6_fill_contrepartie_ET_objFact,
    step7_drop_description,
    step8_fill_categorie,
    step9_export_excel
)
from config import DEFAULT_ENCODING, DELIMITER


def read_input_csv(input_file: str, encoding: str, delimiter: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(input_file, sep=delimiter, encoding=encoding)
    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier '{input_file}' est introuvable.")
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            exc.encoding,
            exc.object,
            exc.start,
            exc.end,
            f"Impossible de lire '{input_file}' avec l'encodage '{encoding}'.",
        ) from exc

    required_columns = {"Description", "Montant", "Valeur"}
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colonnes manquantes dans le CSV : {missing_list}.")

    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convertit un relevé CBC en fichier Excel."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Chemin vers le fichier CSV d'entrée.",
    )
    parser.add_argument(
        "--encoding",
        default=DEFAULT_ENCODING,
        help=f"Encodage du CSV (défaut: {DEFAULT_ENCODING}).",
    )
    parser.add_argument(
        "--delimiter",
        default=DELIMITER,
        help=f"Délimiteur du CSV (défaut: {DELIMITER}).",
    )
    return parser.parse_args()
# --- MAIN ---
def main():
    if len(sys.argv) < 2:
        print("Usage: main.py <fichier.csv>")
        sys.exit(1)
    input_file = sys.argv[1]
    # Charger le CSV
    df = pd.read_csv(input_file, sep=";", encoding="latin-1")
    df = validate_schema(df)
    # *****     VISUAL STEPS     *****
    df = step1_clean_columns(df)
    df = step2_create_new_columns(df)
    df = step3_rename_columns(df)
    df = step4_reorder_columns(df)
    # *****     FONCTIONNAL STEPS     *****
    # Find and exctract operation type from "Description" colomn
    df = step5_find_operation_type(df)
    # Find "Contrepartie" and "Objet de lopération" from "Description" colomn
    df = step6_fill_contrepartie_ET_objFact(df)
    # --- Delete Description column ---
    df = step7_drop_description(df)
  
    # ************
    # df = step8_fill_categorie(df)
    
    # *****     FINAL STEP     *****
    #
    df = step9_export_excel(df, args.input)
    
if __name__ == "__main__":
    main()
