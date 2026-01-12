from __future__ import annotations

from core import main


def test_cli_creates_output(tmp_path):
    input_file = tmp_path / "export_BE50732047041718_20250106_1105.csv"
    input_file.write_text(
        "Description;Montant;Valeur\nTEST;1,00;01/01/2024\n",
        encoding="latin-1",
    )

    output_dir = tmp_path / "out"
    args = [
        "--input",
        str(input_file),
        "--output-dir",
        str(output_dir),
        "--no-update-check",
    ]

    exit_code = main.main(args)

    assert exit_code == 0
    assert list(output_dir.glob("*.xlsx"))
