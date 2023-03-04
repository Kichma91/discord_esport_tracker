import json
import asyncio
import os
import datetime
import time
import requests
import urllib.request
from GameController import GameController

from bs4 import BeautifulSoup
import pandas as pd

from utilities import  client_id, secret , steam_auth_key
from scrapers.csgo_scraper import CSGOscraper
from scrapers.Scraper import AsyncScraper
from constants import Constants

class PayloadHandler(Constants):
    def __init__(self, update_dota_league = False):
        super().__init__(type="payload")

        self.main_scraper = AsyncScraper()
        # self.csgo_scraper = CSGOscraper()
        if update_dota_league:
            self.update_dota_league_data()
        self.dota_league_data = pd.read_csv(self.dota_league_data_file)
        self.game_controller = GameController
        self.main_loop()



    def update_dota_league_data(self):
        secondary_site = "https://www.datdota.com/leagues/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

        r = requests.get(secondary_site, headers=headers)
        soup = BeautifulSoup(r.content, "lxml")

        table = soup.find("table")
        image_elements = table.find_all("img")
        for image_element in image_elements[:8]:
            time.sleep(1)
            link = image_element["src"]
            try:
                urllib.request.urlretrieve(link,
                                           fr"{self.dota_league_images_dir}\{image_element.get('title')}.png")
            except:
                pass

        r = requests.get("https://www.datdota.com/leagues")
        soup = BeautifulSoup(r.content, "lxml")
        table = soup.find("table")
        all_rows = table.find_all("tr")
        id_list = []
        for row in all_rows[1:]:
            text_element = row.find("span").text
            id_list.append(text_element)
        df = pd.read_html(r.content)
        df = df[0]
        df["League"] = id_list
        df.to_csv(self.dota_league_data_file)


    def scrape_and_filter_data(self):
        # csgo_data = self.csgo_scraper.run_scrape()

        dota_accepted_games = []
        lol_accepted_games = []
        valorant_accepted_games = []

        asyncio.run(self.main_scraper.scrape_all())
        data = self.main_scraper.data
        # for Lol game payload, dota game payload and valorant games list
        for game in data:
            # check which game is it and then filter it
            game_name = game[0]
            game_data = game[1]
            if game_name == "lol":
                game_list = game_data["data"]["schedule"]["events"]
                lol_accepted_games = [("lol", x) for x in game_list if x["state"] == "inProgress" and "match" in x.keys()]

            elif game_name == "dota2":
                game_list = game_data["result"]["games"]
                dota_accepted_games = [("dota2", x) for x in game_list if len(
                    self.dota_league_data.loc[self.dota_league_data["League"] == x[
                    "league_id"], "League Name"]) >= 1 and (("radiant_team" and "dire_team") in x.keys())]
            elif game_name == "valorant":
                pass

        accepted_games = dota_accepted_games + lol_accepted_games # later add on csgo and valorant
        return accepted_games

    def main_loop(self):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        while True:
            accepted_games = self.scrape_and_filter_data()
            print(accepted_games)
            time.sleep(5)

if __name__ == "__main__":
    handler = PayloadHandler()














