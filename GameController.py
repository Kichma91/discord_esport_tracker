import json

from game_objects.dota_game import DotaMatch
from game_objects.lol_game import LoLMatch



class GameController():
    def __init__(self):
        self.active_game_list = {}
        with open(r"C:\Users\Davor\PycharmProjects\discord_esport_tracker\assets\dirs.json", "r") as fp:  # directories for images and tables
            self.dirs = json.load(fp)

    def create_games(self,game_list):

        for game in game_list:
            game_name = game[0]
            game_data = game[1]

            if game_name == "lol":
                game_key = f'lol_{game_data["league"]}_{game_data["match"]["teams"][0]["name"]}_{game_data["match"]["teams"][1]["name"]}'
                if game_key not in self.active_game_list.keys():
                    self.active_game_list[game_key] = LoLMatch(game_data)
                else:
                    self.active_game_list[game_key].update_data()

            elif game_name == "dota2":
                game_key = f'dota2_{game_data["league_id"]}_{game_data["match_id"]}'
                self.active_game_list[game_key] = DotaMatch(game_data,self.dirs)
            elif game_name == "valorant":
                pass





