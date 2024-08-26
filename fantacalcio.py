from players_scraper import PlayersScraper

if __name__ == "__main__":
    roles = ["Portieri", "Difensori", "Centrocampisti", "Trequartisti", "Attaccanti"]
    players_urls_file = "players_urls.txt"
    players_file = "players.csv"
    players_excel_file = "players.xlsx"

    scraper = PlayersScraper(roles, players_urls_file, players_file, players_excel_file)
    scraper.run()