import pandas as pd
import sys

# File delle statistiche dei giocatori
stats_file = 'data/csv/team_stats_2024_25.csv'

# Moduli ordinati per preferenza
formations = [
    {'D': 3, 'C': 4, 'A': 3},  # 3-4-3
    {'D': 4, 'C': 3, 'A': 3},  # 4-3-3
    {'D': 3, 'C': 5, 'A': 2},  # 3-5-2
    {'D': 4, 'C': 4, 'A': 2},  # 4-4-2
    {'D': 5, 'C': 3, 'A': 2},  # 5-3-2
    {'D': 4, 'C': 5, 'A': 1},  # 4-5-1
    {'D': 5, 'C': 4, 'A': 1},  # 5-4-1
]

# Leggere il file delle statistiche
df = pd.read_csv(stats_file)

# Ordinare per fantamedia e poi per presenze in ordine decrescente
df = df.sort_values(by=['Fantamedia', 'Presenze'], ascending=[False, False])

# Selezionare i giocatori per ruolo, ora ordinati anche per presenze
portieri = df[df['Ruolo'] == 'P']
difensori = df[df['Ruolo'] == 'D']
centrocampisti = df[df['Ruolo'] == 'C']
attaccanti = df[df['Ruolo'] == 'A']

def get_best_lineup():
    # Provare a formare una squadra in base ai moduli definiti
    for formation in formations:
        n_difensori = formation['D']
        n_centrocampisti = formation['C']
        n_attaccanti = formation['A']

        # Verifica che ci siano abbastanza giocatori per formare la squadra
        if (len(difensori) >= n_difensori and
            len(centrocampisti) >= n_centrocampisti and
            len(attaccanti) >= n_attaccanti and
            len(portieri) >= 1):

            # Selezionare i migliori giocatori per ogni ruolo
            selected_portiere = portieri.iloc[:1]  # Un solo portiere
            selected_difensori = difensori.iloc[:n_difensori]
            selected_centrocampisti = centrocampisti.iloc[:n_centrocampisti]
            selected_attaccanti = attaccanti.iloc[:n_attaccanti]

            # Formare la formazione titolare
            titolari = pd.concat([selected_portiere, selected_difensori, selected_centrocampisti, selected_attaccanti])

            # Restanti giocatori come panchinari
            #remaining_players = pd.concat([
            #    attaccanti.iloc[n_attaccanti:],  # Attaccanti rimanenti
            #    centrocampisti.iloc[n_centrocampisti:],  # Centrocampisti rimanenti
            #    difensori.iloc[n_difensori:],  # Difensori rimanenti
            #    portieri.iloc[1:],  # Portieri rimanenti (il primo è titolare)
            #]).sort_values(by='Fantamedia', ascending=False)
            # Restanti giocatori come panchinari
            remaining_players = pd.concat([
                attaccanti.iloc[n_attaccanti:],  # Attaccanti rimanenti
                centrocampisti.iloc[n_centrocampisti:],  # Centrocampisti rimanenti
                difensori.iloc[n_difensori:],  # Difensori rimanenti
                portieri.iloc[1:],  # Portieri rimanenti (il primo è titolare)
            ])

            # Restituire titolari e panchinari
            return titolari, remaining_players

    # Nessuna formazione trovata
    return None, None

# Ottenere la miglior formazione e i panchinari
titolari, panchinari = get_best_lineup()

# Se la formazione è stata trovata, stamparla
if titolari is not None:
    print("Formazione titolare:")
    print(titolari[['Calciatore', 'Squadra', 'Ruolo', 'Fantamedia', 'Presenze']])

    print("\nPanchinari:")
    print(panchinari[['Calciatore', 'Squadra', 'Ruolo', 'Fantamedia', 'Presenze']])
else:
    print("Non è stato possibile formare una squadra valida con i giocatori disponibili.")