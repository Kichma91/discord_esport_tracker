import json

from game_objects.dota_game import DotaMatch
from game_objects.lol_game import LoLMatch
from image_creators.LoLImage import LoLImg

from constants import Constants


class GameController(Constants):
    def __init__(self):
        super().__init__(type="controller")
        self.active_game_list = {}
        self.lol_image_creator = LoLImg()

    def update_games(self,game_list):

        for game in game_list:
            game_name = game[0]
            game_data = game[1]

            if game_name == "lol":
                game_key = f'lol_{game_data["league"]}_{game_data["match"]["teams"][0]["name"]}_{game_data["match"]["teams"][1]["name"]}'
                if game_key not in self.active_game_list.keys():
                    self.active_game_list[game_key] = LoLMatch(game_data)
                else:
                    self.active_game_list[game_key].update_data()
                print("Created game: ", game_key)
                print(self.active_game_list[game_key].raw_data_level)

            elif game_name == "dota2":
                game_key = f'dota2_{game_data["league_id"]}_{game_data["match_id"]}'
                self.active_game_list[game_key] = DotaMatch(game_data)
            elif game_name == "valorant":
                pass


    def create_images(self):
        for game in self.active_game_list.values():
            if game.game_type == "lol":
                self.lol_image_creator.create_image(game)

    def remove_finished_states(self):
        pass

    def remove_finished_games(self):
        pass





