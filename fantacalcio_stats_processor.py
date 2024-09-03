import pandas as pd
import argparse
import os

# Process all the match days from 1 to the specified match day for a given season and generate a summary report.
#
# Parameters:
# - stagione: str, the season in the format 'YYYY_YY'
# - max_giornata: int, the last match day to process
def process_fantacalcio_stats(stagione, max_giornata):
    # Initialize an empty DataFrame to store all match day data
    all_data = pd.DataFrame()

    # Process each match day from 1 to max_giornata
    for giornata in range(1, max_giornata + 1):
        file_name = f'data/csv/voti_{stagione}_giornata_{giornata}.csv'
        if os.path.exists(file_name):
            # Read the CSV file
            df = pd.read_csv(file_name)
            # Append to the combined DataFrame
            all_data = pd.concat([all_data, df], ignore_index=True)
        else:
            print(f"Warning: File {file_name} does not exist. Skipping...")

    # Ensure necessary columns are present
    required_columns = ['Calciatore', 'Ruolo', 'Voto', 'Gf', 'Gs', 'Rp', 'Rs', 'Rf', 'Au', 'Amm', 'Esp', 'Ass', 'FantaVoto']
    if not all(col in all_data.columns for col in required_columns):
        raise ValueError(f"DataFrame is missing one of the required columns: {required_columns}")

    # Group by 'Calciatore' and aggregate statistics
    stats = all_data.groupby('Calciatore').agg(
        Ruolo=('Ruolo', 'first'),
        Fantamedia=('FantaVoto', 'mean'),
        Presenze=('Calciatore', 'count'),
        Gf=('Gf', 'sum'),
        Gs=('Gs', 'sum'),
        Rp=('Rp', 'sum'),
        Rs=('Rs', 'sum'),
        Au=('Au', 'sum'),
        Amm=('Amm', 'sum'),
        Esp=('Esp', 'sum')
    ).reset_index()

    # Round 'Fantamedia' to 2 decimal places
    stats['Fantamedia'] = stats['Fantamedia'].round(2)

    # Calculate FM su Totale Gare
    #total_gare = len(all_data['Gf'].notnull())
    stats['FM_su_Totale_Gare'] = (stats['Fantamedia']  * stats['Presenze'] / max_giornata).round(2)

    # Save the summary report to a new CSV file
    output_file = f'data/csv/stats_{stagione}.csv'
    stats.to_csv(output_file, index=False)
    print(f"Statistics successfully saved to {output_file}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process match day data and generate player statistics.')
    parser.add_argument('--season', required=True, help='Season in the format YYYY_YY')
    parser.add_argument('--max_day', type=int, required=True, help='Last match day to process')

    # Parse arguments
    args = parser.parse_args()

    # Process the data
    process_fantacalcio_stats(args.season, args.max_day)

if __name__ == '__main__':
    main()
