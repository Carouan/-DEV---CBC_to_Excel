# main.py
import sys
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
    df = step9_export_excel(df, input_file)
    
if __name__ == "__main__":
    main()
