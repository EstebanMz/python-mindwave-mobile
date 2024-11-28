import pandas as pd
import os


# ==================================================
#   Merge DataFrame and save "MindwaveDB.csv" file
# ==================================================

# Merges all CSV files in a folder into a single CSV file, skipping specified files.
# Args:
# - folder_path: The path to the folder containing the CSV files.
# - output_filename: The name of the output CSV file.

folder_path = "output_files/"
output_filename = "output_files/MindwaveDB.csv"

def merge_csv_files(folder_path, output_filename):

    all_dataframes = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and filename not in ("history.csv", "MindwaveDB.csv"):
            filepath = os.path.join(folder_path, filename)
            try:
                df = pd.read_csv(filepath)
                all_dataframes.append(df)
                print(f"Archivo '{filename}' cargado correctamente.")
            except pd.errors.EmptyDataError:
                print(f"Advertencia: El archivo '{filename}' está vacío y se omitirá.")
            except pd.errors.ParserError:
                print(f"Error: No se pudo analizar el archivo '{filename}'. Se omitirá.")

    if all_dataframes:
        merged_df = pd.concat(all_dataframes, ignore_index=True)
        merged_df.to_csv(output_filename, index=False)
        print(f"\nArchivos CSV combinados y guardados en '{output_filename}'.\n")
    else:
        print("\nNo se encontraron archivos CSV válidos para combinar.\n")


# ===============================
#   Run merge and export script
# ===============================

merge_csv_files(folder_path, output_filename)


# =========================
#   Data Cleaning actions
# =========================

# Load the merged CSV file into a pandas DataFrame
df = pd.read_csv('output_files/MindwaveDB.csv')

# Remove rows where 'amount_of_noise' is greater than 0, 
# and where 'meditation' and 'attention' have a value of 0. Resets the df index.
df = df[(df['amount_of_noise'] == 0) & 
        (df['meditation'] > 0) & 
        (df['attention'] > 0)].reset_index(drop=True)

# Drop 'blink', 'date_time' and 'amount_of_noise' columns
df = df.drop(['date_time', 'blink', 'amount_of_noise'], axis=1, errors='ignore')


# ==================================
#   Export dataframe to a CSV file
# ==================================

# df.to_csv(output_filename, index=False)

# Now 'df' contains the processed data
print(df.shape)
# print(df.dtypes)
print(df.head().T)