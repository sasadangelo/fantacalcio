import pandas as pd

# Pesi per fantamedia e probabilità
FANTAMEDIA_WEIGHT = 0.3
PROBABILITY_WEIGHT = 0.7

# File paths
team_file = 'data/csv/team.csv'
stats_file = 'data/csv/stats_2024_25.csv'
probability_file = 'data/csv/probable_lineups_2024_25.csv'
output_file = 'data/csv/team_stats_2024_25.csv'

# Leggere il file team.csv
team_df = pd.read_csv(team_file)

# Leggere il file stats_2024_25.csv
stats_df = pd.read_csv(stats_file)

# Leggere il file probable_lineups_2024_25.csv
probability_df = pd.read_csv(probability_file)

# Unire i dati in base al nome del calciatore
# Qui consideriamo solo i giocatori presenti nella rosa
merged_stats_df = pd.merge(team_df, stats_df, on=['Calciatore', 'Ruolo'], how='inner')
merged_df = pd.merge(merged_stats_df, probability_df[['Calciatore', 'Probabilità']], on='Calciatore', how='left')

# Calcolare l'Appeal
merged_df['Appeal'] = (merged_df['Fantamedia'] * FANTAMEDIA_WEIGHT + merged_df['Probabilità'] * PROBABILITY_WEIGHT).round(2)

# Salvare il risultato su un nuovo file CSV
merged_df.to_csv(output_file, index=False)

print(f"File salvato correttamente in {output_file}")
