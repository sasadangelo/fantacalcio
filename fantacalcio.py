import ast
import sys
from players_scraper import PlayersScraper

skills = {
    "Fuoriclasse": 1,
    "Titolare": 3,
    "Buona Media": 2,
    "Goleador": 4,
    "Assistman": 2,
    "Piazzati": 2,
    "Rigorista": 5,
    "Giovane talento": 2,
    "Panchinaro": -4,
    "Falloso": -2,
    "Outsider": 2,
}

# appeal score =( Fantamedia anno scorso * Partite giocate anno scorso/38 * peso
#              + Fantamedia anno corrente * Partite giocate anno corrente/giornata * 100-peso )/ quotazione
#              + skills + altri parametri
def calculatePlayersAppealScore(players_attributes_df) -> float:
    # Cleaning all the ND with 0 or FALSE
    for col in players_attributes_df.columns:
        players_attributes_df.loc[players_attributes_df[col] == "nd", col] = 0

    res = []

    # This piece of code set playedmax with the max number of presence of all the players.
    max_num_presence = 1
    for index, row in players_attributes_df.iterrows():
        if int(row.iloc[-1]) > int(max_num_presence):
            max_num_presence = int(row.iloc[-1])

    # This loop calculate the Appeal Score for each player
    for index, row in players_attributes_df.iterrows():
        player_appeal_score = 0

        # This is the meaning of the different columns
        #
        # row.iloc[2] = Fanta Average last year
        # row.iloc[5] = Presences last year
        # row.iloc[6] = Fanta Average this year
        # row.iloc[7] = Fanta Average last year weighted by presence
        # row.iloc[-1] = Presences this year

        # This piece of code calculate the last year player's fanta average weighted.
        # If the player has at least one presence then:
        # player_appeal_score += ((Fanta Average last year weighted by presence) * (Presences last year) / 38)*20/100
        if int(row.iloc[5]) > 0:
           player_appeal_score += float(row.iloc[7]) * int(row.iloc[5])/38*20/100

        # This piece of code calculate the current year player's fanta average weighted.
        # Notice as the current here weigth 80% and last year 20%.
        #
        # If the player has at least five presences then:
        # player_appeal_score += ((Fanta Average this year) * (Presences this year)/max_num_presence)*80/100
        # else
        # player_appeal_score += ((Fanta Average this year) * (Presences this year)/38)
        if not (players_attributes_df.columns[2].split(" ")[-1] == players_attributes_df.columns[6].split(" ")[-1] and int(row.iloc[-1]) > 5):  # stesso anno
            player_appeal_score = (
                player_appeal_score * float(row.iloc[6]) * int(row.iloc[-1])/max_num_presence*80/100
            )
        else:
            player_appeal_score = float(row.iloc[7]) * int(row.iloc[5])/38

        # media pesata fantamedia * convenienza rispetto alla quotazione * media scorso anno
        player_appeal_score=player_appeal_score*float(row['Punteggio'])*30/100
        if float(row.iloc[1]) == 0:
            pt=1
        else:
            pt=float(row.iloc[1])

        player_appeal_score = (
            player_appeal_score / pt * 100 / 40
        )

        # skills
        try:
            valori = ast.literal_eval(row.iloc[-9])
            plus = 0
            for skill in valori:
                plus += skills[skill]
            player_appeal_score += plus
        except:
            pass

        if row["Nuovo acquisto"]:
            player_appeal_score -= 2
        if int(row["Buon investimento"]) == 60:
            player_appeal_score += 3
        if row["Consigliato prossima giornata"]:
            player_appeal_score += 1
        if row["Trend"] == "UP":
            player_appeal_score += 2
        if row["Infortunato"]:
            player_appeal_score -= 1
        if int(row["Resistenza infortuni"]) > 60:
            player_appeal_score += 4
        if int(row["Resistenza infortuni"]) == 60:
            player_appeal_score += 2
        res.append(player_appeal_score)
    return res

if __name__ == "__main__":
    roles = ["Portieri", "Difensori", "Centrocampisti", "Trequartisti", "Attaccanti"]
    players_urls_file = "players_urls.txt"
    players_file = "players.csv"
    players_excel_file = "players.xlsx"

    scraper = PlayersScraper(roles, players_urls_file, players_file, players_excel_file)
    scraper.run()

    players_attributes_df = scraper.players_attributes_df
    players_attributes_df["Convenienza"] = calculatePlayersAppealScore(players_attributes_df)

    #riordino le colonne come piace a me
    temp = players_attributes_df.columns
    players_attributes_df = players_attributes_df[
        [
            temp[11],
            temp[0],
            temp[18],
            temp[1],
            temp[21],
            temp[19],
            temp[12],
            temp[20],
            temp[6],
            temp[2],
            temp[5],
            temp[7],
            temp[3],
            temp[4],
            temp[16],
            temp[17],
            temp[8],
            temp[9],
            temp[10],
            temp[13],
            temp[14],
            temp[15],
        ]
    ]

    players_attributes_df=players_attributes_df.sort_values(by="Convenienza", ascending=False)
    players_attributes_df.to_excel(players_excel_file)