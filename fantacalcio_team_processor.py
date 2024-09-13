import pandas as pd

# File paths
team_file = 'data/csv/team.csv'
stats_file = 'data/csv/stats_2024_25.csv'
output_file = 'data/csv/team_stats_2024_25.csv'

# Leggere il file team.csv
team_df = pd.read_csv(team_file)

# Leggere il file stats_2024_25.csv
stats_df = pd.read_csv(stats_file)

# Unire i dati in base al nome del calciatore
# Qui consideriamo solo i giocatori presenti nella rosa
merged_df = pd.merge(team_df, stats_df, on=['Calciatore', 'Ruolo'], how='inner')

# Salvare il risultato su un nuovo file CSV
merged_df.to_csv(output_file, index=False)

print(f"File salvato correttamente in {output_file}")
