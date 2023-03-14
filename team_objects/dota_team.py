import urllib.request
import time
import os
from constants import Constants
from player_objects.dota_player import DotaPlayer
from urllib import error

class DotaTeam(Constants):
    def __init__(self, raw_data,side):
        super().__init__(type="dota")
        self.raw_data = raw_data
        self.player_data_assigned = False
        self.name = raw_data["team_name"]

        self.id = raw_data["team_id"]
        self.team_logo_id = raw_data["team_logo"]
        self.game_wins = 0


        self.side = side
        if side == "radiant":
            self.color = "blue"
        elif side == "dire":
            self.color = "red"

        self.picks = []
        self.bans = []
        self.download_team_image()
        self.players = {}

    def assign_player_data(self, all_player_data, team_number):
        if not self.player_data_assigned:
            for player in all_player_data:
                if player["team"] == team_number:
                    player_id = player["account_id"]
                    self.players[player_id] = DotaPlayer(player_data=player)
            if len(self.players.keys()) == 5:
                self.player_data_assigned = True

    def update_player_data(self, player_data):
        if self.player_data_assigned:
            for player in player_data:
                self.players[player["account_id"]].update_data(player)


    def download_team_image(self):
        team_image_name = f"{self.id}.png"

        image_link = f"https://cdn.cloudflare.steamstatic.com/apps/dota2/teamlogos/{team_image_name}"
        team_image_dir_listed = os.listdir(self.team_image_dir)
        if team_image_name in team_image_dir_listed:
            pass
        else:
            try:
                urllib.request.urlretrieve(image_link, fr"{self.team_image_dir}/{team_image_name}")
                time.sleep(0.5)
            except urllib.error.HTTPError:
                print(f"No team image for {self.name}")

