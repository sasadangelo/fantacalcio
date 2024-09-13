import requests
from bs4 import BeautifulSoup
import csv

# URL della pagina web da cui scaricare i dati
url = 'https://www.fantacalcio.it/probabili-formazioni-serie-a'
# Nome del file CSV
csv_filename = 'data/csv/probable_lineups_2024_25.csv'

# Funzione per scaricare e analizzare la pagina
def get_probable_lineups(url):
    # Richiedere la pagina web
    response = requests.get(url)
    response.raise_for_status()  # Verifica se la richiesta è andata a buon fine

    # Creare l'oggetto BeautifulSoup per l'analisi della pagina
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trovare la sezione contenente le probabili formazioni
    # Nota: il selettore può variare in base alla struttura HTML della pagina
    formations_section = soup.find_all('li', class_='player-item pill')

    # Eseguire il parsing e raccogliere i dati
    formations = []
    for item in formations_section:
        # Nome del calciatore
        player_name_tag = item.find('a', class_='player-name player-link')
        player_name = player_name_tag.get_text(strip=True) if player_name_tag else 'Unknown'

        # Probabilità
        probability_tag = item.find('div', class_='progress-value')
        probability_str = probability_tag.get_text(strip=True) if probability_tag else 'Unknown'

        # Convertire la probabilità in formato decimale
        try:
            # Rimuovere il simbolo di percentuale e convertire in float
            probability = float(probability_str.replace('%', '').strip()) / 100
        except ValueError:
            # Gestire i casi in cui la conversione fallisce
            probability = 0.0

        formations.append({
            'Player': player_name,
            'Probability': probability
        })

    return formations

# Ottenere le probabili formazioni
lineups = get_probable_lineups(url)

# Salvare i dati su file CSV
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Scrivere l'intestazione del file CSV
    writer.writerow(['Calciatore', 'Probabilità'])

    # Scrivere i dati
    for lineup in lineups:
        writer.writerow([lineup['Player'], lineup['Probability']])