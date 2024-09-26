# Fantacalcio

Fantacalcio è una serie di scripts Python che utilizzo per giocare a Fantacalcio.

## Prerequisiti

Per usare questa serie di script Python hai bisogno:
1. git
2. Python 3.x

## Preparazione ambiente esecuzione

Questi sono i passi per preparare l'ambiente di esecuzione:

1. Scarica il repository con il comando `git clone https://github.com/sasadangelo/fantacalcio`.
2. Prepara il Python Virtual Environment con il comando `python3 -m venv venv`.
3. Attiva il Python Virtual environment con il comando `source venv/bin/activate`.
4. Installa le dipendenze con il comando `pip3 install -r requirements.txt`.

## Come aggiornare le statistiche dei giocatori alla fine di ogni Giornata di campionato?

Questi sono i passi da fare alla fine di ogni giornata di campionato:

1. Scarica il file Excel con i voti dal sito [Fantacalcio.it](https://www.fantacalcio.it/voti-fantacalcio-serie-a). Per farlo devi essere loggato al sito. Metti il file scaricato nel folder `data/xlsx`.
2. Converti il file Excel scaricato al passo 1 nel file `data/csv/voti_2024_25_giornata_N.csv` con il comando `python3 fantacalcio_scores_processor.py --input data/xlsx/Voti_Fantacalcio_Stagione_2024_25_Giornata_N.xlsx --output data/csv/voti_2024_25_giornata_N.csv` dove N è il numero della giornata.
3. Aggiorna le statistiche dei giocatori con il comando `python3 fantacalcio_stats_processor.py --season 2024_25 --max_day N` dove N è il numero della giornata. Ovviamente sostituisci l'annata della stagione con quella attuale.

## Come preparare la formazione per la prossima giornata di Campionato?

Questi script Python calcolano la migliore formazione per la prossima giornata incrociando la Fantamedia, le Presenza con le Probabili formazioni. Con questi dati verrà calcolato un valore di Appeal del giocatore. Più è alto questo valore è migliore è il suo ranking ad essere schierato. Ricordo che questa procedura andrebbe fatta il giorno prima dell'inizio della giornata o, meglio ancora, qualche ora prima dell'inizio. Il motivo è che la lista dei probabili giocatori che giocheranno sarà più affidabile.

Questi sono i passi da fare per calcolare la formazione da schierare la prossima giornata di campionato:

1. Assicurati di avere il file `team.csv` con i giocatori della tua rosa.
2. Scarica le probabilità di presenza di ciascun giocatore con il comando `python3 fantacalcio_probable_lineups_processor.py`.
3. Calcola l'appeal di ciascun calciatore con il comando `python3 fantacalcio_team_processor.py`. Il file `data/csv/team_stats_2024_25.csv` verrà aggiornato.
4. Calcola la migliore formazione da schierare in base all'appeal dei calciatori con il comando `python3 fantacalcio_lineup_processor.py `.
