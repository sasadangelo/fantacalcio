from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import os
from time import sleep
from random import randint
import pandas as pd
from player import Player

class PlayersScraper:
    def __init__(self, roles, players_urls_file, players_file, players_excel_file):
        self.roles = roles
        self.players_urls_file = players_urls_file
        self.players_file = players_file
        self.players_excel_file = players_excel_file
        self.players_urls = []
        self.players = []
        self.players_attributes_df = None

    def __collect_player_attributes(self, url: str) -> Player:
        # Fetch the player's page
        response = requests.get(url.strip())

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            attributes = dict()

            attributes['Nome']=soup.select_one("h1").get_text().strip()

            selector = "div.col_one_fourth:nth-of-type(1) span.stickdan"
            attributes['Punteggio']= soup.select_one(selector).text.strip().replace("/100", "")

            selector = "	div.col_one_fourth:nth-of-type(n+2) div"
            avgs = [el.find("span").text.strip() for el in soup.select(selector)]
            years = [el.find("strong").text.split(" ")[-1].strip() for el in soup.select(selector)]
            i = 0
            for year in years:
                attributes[f"Fantamedia anno {year}"] = avgs[i]
                i += 1

            selector = "div.col_one_third:nth-of-type(2) div"
            stats_last_year = soup.select_one(selector)
            parameters = [el.text.strip().replace(":", "") for el in stats_last_year.find_all("strong")]
            stats_last_year_values = [el.text.strip() for el in stats_last_year.find_all("span")]
            attributes.update(dict(zip(parameters, stats_last_year_values)))

            selector = ".col_one_third.col_last div"
            stats_previste = soup.select_one(selector)
            parameters = [el.text.strip().replace(":", "") for el in stats_previste.find_all("strong")]
            valori = [el.text.strip() for el in stats_previste.find_all("span")]
            attributes.update(dict(zip(parameters, valori)))

            selector = ".label12 span.label"
            role = soup.select_one(selector)
            attributes["Ruolo"] = role.get_text().strip()

            selector = "span.stickdanpic"
            skills = [el.text for el in soup.select(selector)]
            attributes["Skills"] = skills

            selector = "div.progress-percent"
            investiment = soup.select(selector)[2]
            attributes["Buon investimento"] = investiment.text.replace("%", "")

            selector = "div.progress-percent"
            investimento = soup.select(selector)[3]
            attributes["Resistenza infortuni"] = investimento.text.replace("%", "")

            selector = "img.inf_calc"
            try:
                consigliato = soup.select_one(selector).get("title")
                if "Consigliato per la giornata" in consigliato:
                    attributes["Consigliato prossima giornata"] = True
                else:
                    attributes["Consigliato prossima giornata"] = False
            except:
                attributes["Consigliato prossima giornata"] = False

            selector = "span.new_calc"
            nuovo = soup.select_one(selector)
            if not nuovo == None:
                attributes["Nuovo acquisto"] = True
            else:
                attributes["Nuovo acquisto"] = False

            selector = "img.inf_calc"
            try:
                infortunato = soup.select_one(selector).get("title")
                if "Infortunato" in infortunato:
                    attributes["Infortunato"] = True
                else:
                    attributes["Infortunato"] = False
            except:
                attributes["Infortunato"] = False

            selector = "#content > div > div.section.nobg.nomargin > div > div > div:nth-child(2) > div.col_three_fifth > div.promo.promo-border.promo-light.row > div:nth-child(3) > div:nth-child(1) > div > img"
            squadra = soup.select_one(selector).get("title").split(":")[1].strip()
            attributes["Squadra"] = squadra

            selector = "	div.col_one_fourth:nth-of-type(n+2) div"
            try:
                trend = soup.select(selector)[0].find("i").get("class")[1]
                if trend == "icon-arrow-up":
                    attributes["Trend"] = "UP"
                else:
                    attributes["Trend"] = "DOWN"
            except:
                attributes["Trend"] = "STABLE"

            selector = "div.col_one_fourth:nth-of-type(2) span.rouge"
            presenze_attuali = soup.select_one(selector).text
            attributes["Presenze campionato corrente"] = presenze_attuali
            return Player(attributes=attributes)
        else:
            print(f"Failed to retrieve player data from {url}")
            return None

    def __collect_all_player_attributes(self):
        # Load the player URLs from the file
        with open(self.players_urls_file, "r") as file:
            player_urls = file.readlines()

        # Collect attributes for each player
        for player_url in player_urls:
            print(f"Download player attributes from URL {player_url}")
            player = self.__collect_player_attributes(player_url)
            # Random sleep to avoid being blocked by the website
            sleep_time = randint(0, 2000) / 1000
            sleep(sleep_time)
            if player:
                self.players.append(player)

    def __scrape_players_urls(self, role: str) -> list:
        url = f"https://www.fantacalciopedia.com/lista-calciatori-serie-a/{role.lower()}/"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            players_urls = []
            players_list = soup.find_all("article")

            for player_element in players_list:
                player_url = player_element.find("a").get("href")
                players_urls.append(player_url)

            return players_urls
        else:
            print(f"Failed to retrieve data for role: {role}")
            return []

    def __download_all_player_urls(self):
        for role in tqdm(self.roles):
            role_players_urls = self.__scrape_players_urls(role)
            self.players_urls.extend(role_players_urls)
            print(f"Collected {len(role_players_urls)} URLs for role: {role}")

    def __save_players_urls_to_file(self):
        with open(self.players_urls_file, "w") as file:
            for url in self.players_urls:
                file.write(f"{url}\n")

    def __save_players_to_file(self):
        players_attributes = []
        with open(self.players_file, "w") as file:
            for player in self.players:
                players_attributes.append(player.attributes)
        self.players_attributes_df = pd.DataFrame.from_dict(players_attributes)
        self.players_attributes_df.to_csv(self.players_file, index=False)

    def __load_existing_players_urls(self):
        if os.path.exists(self.players_urls_file):
            with open(self.players_urls_file, "r") as file:
                existing_urls = set(line.strip() for line in file)
            return existing_urls
        return set()

    def run(self):
        # This piece of code check if the players_urls.txt file exists.
        # If so, the URLs are loaded in memory otherwise they are downloaded from Fantacalciopedia.com
        # then they will be ket in memory and sved in the players_urls.txt file.
        self.players_urls = self.__load_existing_players_urls()
        if self.players_urls:
            print(f"Found {len(self.players_urls)} existing URLs.")
        else:
            self.__download_all_player_urls()

            if self.players_urls:
                self.__save_players_urls_to_file()
                print(f"New player URLs have been saved to {self.players_urls_file}")
            else:
                print("No new player URLs to save.")

        if os.path.exists(self.players_file):
            self.players_attributes_df = pd.read_csv(self.players_file)
            if not self.players_attributes_df.empty:
                print(f"Found {len(self.players_attributes_df)} players in the {self.players_file} file.")
        else:
            self.__collect_all_player_attributes()
            if self.players:
                self.__save_players_to_file()
                print(f"New players have been saved to {self.players_file}")
            else:
                print("No new player to save.")
