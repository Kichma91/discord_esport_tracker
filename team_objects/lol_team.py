import urllib.request
import time
import os

class LolTeam():
    def __init__(self, name, code, image_link, image_name, game_wins, dirs):
        self.name = name
        self.code = code
        self.image_link = image_link
        self.image_name = image_name
        self.game_wins = game_wins

        self.players = {}
        self.players_name_dict = {}
        self.id = ""
        self.color = ""
        self.gold = 0
        self.inhibitors = 0
        self.towers = 0
        self.barons = 0
        self.total_kills = 0
        self.dragons = []
        self.dirs = dirs
        self.team_image_dir = self.dirs["lol_teams"]
        self.download_team_image()

    def download_team_image(self):
        team_image_name = self.image_link.split(r"/")[-1]
        team_image_dir_listed = os.listdir(self.team_image_dir)
        if team_image_name in team_image_dir_listed:
            pass
        else:
            urllib.request.urlretrieve(self.image_link, fr"{self.team_image_dir}/{team_image_name}")
            time.sleep(0.5)





