import argparse
from pathlib import Path

import pandas as pd

from .config import DEFAULT_CATEGORY_FILE, DEFAULT_ENCODING, DELIMITER
from .steps import (
    step1_clean_columns,
    step2_create_new_columns,
    step3_rename_columns,
    step4_reorder_columns,
    step5_find_operation_type,
    step6_fill_contrepartie_ET_objFact,
    step7_drop_description,
    step8_fill_categorie,
    step9_export_excel,
    validate_schema,
)


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
    parser.add_argument(
        "--categories",
        default=DEFAULT_CATEGORY_FILE,
        help=(
            "Chemin vers le fichier CSV des catégories "
            f"(défaut: {DEFAULT_CATEGORY_FILE})."
        ),
    )
    parser.add_argument(
        "--no-categories",
        action="store_true",
        help="Désactive l'association automatique des catégories.",
    )
    return parser.parse_args()


# --- MAIN ---
def main():
    args = parse_args()
    df = read_input_csv(args.input, args.encoding, args.delimiter)
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

    if not args.no_categories:
        category_path = Path(args.categories)
        if not category_path.exists():
            raise FileNotFoundError(
                f"Fichier de catégories introuvable: {category_path}"
            )
        df = step8_fill_categorie(df, str(category_path))

    # *****     FINAL STEP     *****
    #
    df = step9_export_excel(df, args.input)

if __name__ == "__main__":
    main()
