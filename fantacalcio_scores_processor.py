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
    df = pd.read_excel(input_file, sheet_name='Fantacalcio')

    # Drop the first column
    df = df.drop(df.columns[0], axis=1)

    # Remove the first useless4 rows
    df = df.iloc[4:]

    # Define the new header
    new_header = ['Ruolo', 'Calciatore', 'Voto', 'Gf', 'Gs', 'Rp', 'Rs', 'Rf', 'Au', 'Amm', 'Esp', 'Ass']

    # Set the new header
    df.columns = new_header

    # Remove rows where all columns are NaN
    df = df.dropna(how='all')

    # Replace '6*' with '6' in the 'Voto' column
    if 'Voto' in df.columns:
        df['Voto'] = df['Voto'].replace('6*', '6')

    # Convert columns to numeric types
    numeric_columns = ['Voto', 'Gf', 'Gs', 'Rp', 'Rs', 'Au', 'Amm', 'Esp', 'Ass']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Calculate FantaVoto
    df['FantaVoto'] = (df['Voto'] +
                       3 * df['Gf'] -
                       1 * df['Gs'] +
                       3 * df['Rp'] +
                       3 * df['Rs'] -
                       1 * df['Au'] -
                       0.5 * df['Amm'] -
                       1 * df['Esp'] +
                       1 * df['Ass'])

    # Remove rows where 'Ruolo' appears in any column
    df = df[~df.apply(lambda row: row.astype(str).str.contains('Ruolo').any(), axis=1)]

    # Remove rows where 'ALL' appears in any column
    #df = df[~df.applymap(lambda x: 'ALL' in str(x)).any(axis=1)]
    # Remove rows where 'ALL' appears in any column
    df = df[~df.apply(lambda row: row.astype(str).str.contains('ALL').any(), axis=1)]

    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)
    print(f"{input_file} successfully converted in a CSV file and saved to {output_file}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert an Excel file to a CSV file with data processing.')
    parser.add_argument('--input', required=True, help='Path to the input Excel file')
    parser.add_argument('--output', required=True, help='Path to the output CSV file')

    # Parse arguments
    args = parser.parse_args()

    # Process the Excel file and save as CSV
    process_excel_to_csv(args.input, args.output)

if __name__ == '__main__':
    main()
