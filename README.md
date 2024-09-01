# Fantacalcio

Fantacalcio è un piccolo python tool ispirato da questo repository per creare una lista di giocatori da scegliere per la Fanta Asta. Questi giocatori sono ordinati per Convenienza che è una metrica calcolata a partire dalle statistiche di ciascun giocatore. Le statistiche sono scaricate da [Fantacalciopedia.com](https://www.fantacalciopedia.com/).

## Le statistiche di FantacalcioPedia.com usate

Per ogni giocatore il tool scarica le seguenti informazioni dal sito [Fantacalciopedia.com](https://www.fantacalciopedia.com/) e li mette nel file [players.csv](https://github.com/sasadangelo/fantacalcio/blob/main/players.csv):
* **Punteggio**: il punteggio incorpora il trend degli ultimi 3 anni del giocatore e quello relativo al rendimento più recente insieme ad altri vari indicatori dello stato di forma. 
* **Fantamedia anno 2023-2024**: è la fantamedia del campionato corrente (è ancora presto per avere i dati del 2024/25).
* **Fantamedia anno 2022-2023**: è la fantamedia del campionato scorso.
* **Fantamedia anno 2021-2022**: è la fantamedia del campionato di 2 anni fa.
* **Presenze 2023-2024**: presenza nel campionato corrente.
* **Fanta Media 2023-2024**: to remove
* **FM su tot gare 2023-2024**: è il valore (Fantamedia anno 2023-2024/Presenze 2023-2024).
* **Presenze previste**: le presenze previste nel campionato corrente.
* **Gol previsti**: gol previsti nel campionato corrente.
* **Assist previsti**: assist previsti nel campionato corrente.
* **Ruolo**: Ruolo del giocatore. Valori possibili sono: Portiere, Difensore, Centrocampista, Trequartista, Attaccante.
* **Skills**: le attitudini del giocatore. Valori possibili sono: Titolare, Buona Media, Falloso, Outsider, Assistman, Piazzati, Goleador, Giovane talento. Questi skills saranno usate nel calcolo dell'appeal del giocatore come bonus o malus.
* **Buon investimento**: un valore che indica se il giocatore può essere un buon investimento.
* **Resistenza infortuni**: un valore che indica se il giocatore è predisposto o meno agli infortuni.
* **Consigliato prossima giornata**: se il giocatore è consigliato nella prossima giornata.
* **Nuovo acquisto**: se il giocatore è un nuovo acquisto della sua squadra.
* **Infortunato**: se il giocatore è infortunato.
* **Squadra**: la squadra dove gioca il calciatore.
* **Trend**: il trend del giocatore.
* **Presenze campionato corrente**: presenze campionato corrente.
