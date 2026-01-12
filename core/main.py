"""CLI entrypoint for converting CBC CSV exports to Excel."""

from __future__ import annotations

import argparse
import sys
import tempfile
from importlib import metadata
from pathlib import Path

import pandas as pd

from .config import DEFAULT_CATEGORY_FILE, DEFAULT_ENCODING, DEFAULT_OUTPUT_DIR, DELIMITER
from .naming import get_output_filename_and_period
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
from .updater import check_for_updates, maybe_notify_update, perform_portable_update


def get_version() -> str:
    """Return the installed package version or a fallback."""
    try:
        return metadata.version("cbc-to-excel")
    except metadata.PackageNotFoundError:
        return "0.0.0"


def read_input_csv(input_file: str, encoding: str, delimiter: str) -> pd.DataFrame:
    """Read a CSV export into a DataFrame.

    Args:
        input_file: Path to the CSV file.
        encoding: Text encoding of the CSV file.
        delimiter: Column separator used in the CSV file.

    Returns:
        DataFrame containing the parsed CSV rows.

    Raises:
        FileNotFoundError: When the input file does not exist.
        UnicodeDecodeError: When decoding fails with the provided encoding.
    """
    try:
        return pd.read_csv(input_file, sep=delimiter, encoding=encoding)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Le fichier '{input_file}' est introuvable.") from exc
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            exc.encoding,
            exc.object,
            exc.start,
            exc.end,
            f"Impossible de lire '{input_file}' avec l'encodage '{encoding}'.",
        ) from exc


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments.

    Args:
        argv: Optional argument list for testing.

    Returns:
        Parsed argparse namespace.
    """
    parser = argparse.ArgumentParser(
        description="Convertit un relevé CBC en fichier Excel.",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Chemin vers le fichier CSV d'entrée.",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help=(
            "Répertoire de sortie pour le fichier Excel "
            f"(défaut: {DEFAULT_OUTPUT_DIR})."
        ),
    )
    parser.add_argument(
        "--output",
        help=(
            "Chemin complet de sortie pour le fichier Excel. "
            "Si défini, --output-dir est ignoré."
        ),
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
    parser.add_argument(
        "--check-updates",
        action="store_true",
        help="Force la vérification de mise à jour et affiche le résultat.",
    )
    parser.add_argument(
        "--no-update-check",
        action="store_true",
        help="Désactive la vérification automatique des mises à jour.",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="Télécharge la dernière version disponible (portable Windows).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )
    return parser.parse_args(argv)


def _resolve_output_path(args: argparse.Namespace, df: pd.DataFrame) -> str:
    """Resolve the output Excel file path based on arguments.

    Args:
        args: Parsed CLI arguments.
        df: DataFrame used to compute the output name.

    Returns:
        String path to the output Excel file.
    """
    if args.output:
        return str(Path(args.output))

    output_dir = Path(args.output_dir)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        output_dir = Path(tempfile.mkdtemp(prefix="cbc-to-excel-"))
        print(
            "Impossible de créer le répertoire demandé. "
            f"Utilisation du dossier temporaire: {output_dir}"
        )

    output_name, _ = get_output_filename_and_period(args.input, df)
    return str(output_dir / output_name)


# --- MAIN ---
def main(argv: list[str] | None = None) -> int:
    """Run the CBC to Excel conversion pipeline.

    Args:
        argv: Optional argument list for testing.

    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    args = parse_args(argv)
    current_version = get_version()

    if args.check_updates:
        result = check_for_updates(current_version)
        print(result.message)
        return 0

    if args.update:
        perform_portable_update(current_version)
        return 0

    if not args.no_update_check:
        try:
            maybe_notify_update(current_version)
        except Exception as exc:  # pragma: no cover - fails silently for UX
            print(f"Mise à jour ignorée: {exc}")

    try:
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
        output_path = _resolve_output_path(args, df)
        step9_export_excel(df, args.input, output_path)
    except Exception as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
