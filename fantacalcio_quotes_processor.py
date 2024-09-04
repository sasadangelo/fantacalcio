import pandas as pd
import argparse
import os

# Process an Excel file and save the cleaned DataFrame to a CSV file.
#
# Parameters:
# - input_file: str, path to the input Excel file
# - output_file: str, path to the output CSV file
def process_excel_to_csv(input_file, output_file):
    # Ensure the input file is an Excel file
    if not input_file.lower().endswith(('.xlsx', '.xls')):
        raise ValueError("Input file must be an Excel file with extension .xlsx or .xls")

    # Load the data from the Excel file
    df = pd.read_excel(input_file, sheet_name='Tutti')

    # List of column indices to drop
    columns_to_drop = [0, 2, 5, 6, 7, 8, 9, 10, 12]

    # Drop the specified columns
    df = df.drop(df.columns[columns_to_drop], axis=1)

    # Remove the first useless4 rows
    df = df.iloc[1:]

    # Define the new header
    new_header = ['Ruolo', 'Calciatore', 'Squadra', 'FVM']

    # Set the new header
    df.columns = new_header

    # Remove rows where all columns are NaN
    df = df.dropna(how='all')
    # Extract the relevant columns
    df_corrected = df[['Ruolo', 'Calciatore', 'Squadra', 'FVM']]

    # Reorder the columns
    df_corrected = df_corrected[['Calciatore', 'Squadra', 'Ruolo', 'FVM']]

    # Save the DataFrame to a CSV file
    df_corrected.to_csv(output_file, index=False)
    print(f"{input_file} successfully converted in a CSV file and saved to {output_file}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert the Excel Quote file to CSV format.')
    parser.add_argument('--input', required=True, help='Path to the input Excel file')
    parser.add_argument('--output', required=True, help='Path to the output CSV file')

    # Parse arguments
    args = parser.parse_args()

    # Process the Excel file and save as CSV
    process_excel_to_csv(args.input, args.output)

if __name__ == '__main__':
    main()
