"""Helpers to derive output file names from CBC exports."""

from __future__ import annotations

import os

import pandas as pd

from .config import cptsCBC


def parse_filename(file_name: str) -> tuple[str, str, str, str]:
    """Parse the CBC export filename into components.

    Args:
        file_name: Input CSV file name.

    Returns:
        Tuple containing account part, date part, time part, and extension.

    Raises:
        ValueError: If the file name does not match the expected pattern.
    """
    base_name = os.path.basename(file_name)
    root, extension = os.path.splitext(base_name)
    parts = root.split("_", maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"Nom de fichier non conforme : {file_name}")
    _ = parts[0]  # "export"
    account_part = parts[1]  # "BE50732047041718" ou "Mastercard Business Blue CBC"
    date_part = parts[2]  # "20250106"
    time_part = parts[3]  # "1105"
    return account_part, date_part, time_part, extension


def format_export_date(date_yyyymmdd: str) -> str:
    """Format an export date from YYYYMMDD to YYYY.MM.DD."""
    year = date_yyyymmdd[0:4]
    month = date_yyyymmdd[4:6]
    day = date_yyyymmdd[6:8]
    return f"{year}.{month}.{day}"


def build_period_string(df: pd.DataFrame) -> str:
    """Build a human-readable period string from the Date column.

    Args:
        df: DataFrame containing a "Date" column.

    Returns:
        Period string suitable for sheet names and file names.
    """
    if "Date" not in df.columns:
        return "[no date]"
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    if pd.isnull(min_date) or pd.isnull(max_date):
        return "[date non définie]"
    fmt_full = "%d.%m.%Y"

    if (min_date.month == max_date.month) and (min_date.year == max_date.year):
        day_min = min_date.day
        day_max = max_date.day
        month_year = min_date.strftime("%m.%y")
        return f"[{day_min}-{day_max}({month_year})]"
    if min_date.year == max_date.year:
        day_min = min_date.day
        day_max = max_date.day
        month_min = min_date.strftime("%m")
        month_max = max_date.strftime("%m")
        year = min_date.year
        return f"[{day_min}.{month_min}-{day_max}.{month_max}({year})]"

    dmin_str = min_date.strftime(fmt_full)
    dmax_str = max_date.strftime(fmt_full)
    return f"[{dmin_str}-{dmax_str}]"


def build_new_filename(date_export_fr: str, nomCompte: str, period: str) -> str:
    """Build the output Excel file name from parts."""
    safe_period = period.replace("/", "-").replace(":", "-")
    return f"{safe_period}_{nomCompte}_{date_export_fr}.xlsx"


def get_nom_compte(account_part: str) -> str:
    """Map an account identifier to a friendly name."""
    return cptsCBC.get(account_part, account_part)


def get_output_filename(input_file: str, df: pd.DataFrame) -> str:
    """Generate the output file name based on the input CSV.

    Args:
        input_file: Input CSV file path.
        df: DataFrame containing the parsed rows.

    Returns:
        Output Excel file name.
    """
    account_part, date_part, _time_part, _extension = parse_filename(input_file)
    period = build_period_string(df)
    date_export_fr = format_export_date(date_part)
    nomCompte = get_nom_compte(account_part)
    return build_new_filename(date_export_fr, nomCompte, period)


def get_output_filename_and_period(
    input_file: str, df: pd.DataFrame
) -> tuple[str, str]:
    """Return the output file name and period string.

    Args:
        input_file: Input CSV file path.
        df: DataFrame containing the parsed rows.

    Returns:
        Tuple of output file name and period string.
    """
    account_part, date_part, _time_part, _extension = parse_filename(input_file)
    period = build_period_string(df)
    date_export_fr = format_export_date(date_part)
    nomCompte = get_nom_compte(account_part)
    out_file_name = build_new_filename(date_export_fr, nomCompte, period)

    return out_file_name, period


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python naming.py <fichier.csv>")
        sys.exit(1)
    test_file = sys.argv[1]
    df_test = pd.DataFrame({"Date": pd.to_datetime(["2024-01-13", "2024-02-22"])})
    result_name = get_output_filename_and_period(test_file, df_test)
    print(f"Nom de fichier généré : {result_name}")
