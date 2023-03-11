import datetime
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
        self.lol_finished_games_list = {}
        self.reset_time = datetime.timedelta(minutes=2)
        self.delete_time = datetime.timedelta(minutes=5)


    def update_games(self,game_list):

        found_games = []
        games_to_delete = []
        for game in game_list:
            game_name = game[0]
            game_data = game[1]

            if game_name == "lol":
                game_key = f'lol_{game_data["league"]}_{game_data["match"]["teams"][0]["name"]}_{game_data["match"]["teams"][1]["name"]}'
                found_games.append(game_key)
                if game_key not in self.active_game_list.keys():
                    self.active_game_list[game_key] = LoLMatch(game_data)
                else:
                    game2 = self.active_game_list[game_key]
                    if game2.match_finished:
                        if game_key in self.lol_finished_games_list:
                            if datetime.datetime.now() - self.lol_finished_games_list[game_key] > self.delete_time:
                                del(self.lol_finished_games_list[game_key])
                                del(self.active_game_list[game_key])
                                # DELETE THE IMAGE
                                print(f"Deleting lol game {game_key}")
                            else:
                                pass
                        else:
                            self.lol_finished_games_list[game_key] = game2.finished_time


                    elif game2.finished_state2:
                        if game_key in self.lol_finished_games_list:
                            if datetime.datetime.now() - self.lol_finished_games_list[game_key] > self.reset_time:
                                game2.reset_data()
                                print(f"reseting lol game {game_key}")
                                del (self.lol_finished_games_list[game_key])

                        else:
                            print("adding finished game")
                            self.lol_finished_games_list[game_key] = game2.finished_time
                    else:
                        game2.update_data()


            elif game_name == "dota2":
                game_key = f'dota2_{game_data["league_id"]}_{game_data["match_id"]}'
                found_games.append(game_key)
                if game_key not in self.active_game_list.keys():
                    self.active_game_list[game_key] = DotaMatch(game_data)
                else:
                    self.active_game_list[game_key].update_data(game_data)


            elif game_name == "valorant":
                pass
        # for game in self.active_game_list.keys():
        #     if game not in found_games:
        #         games_to_delete.append(game)
        # for game2 in games_to_delete:
        #     del (self.active_game_list[game2])


    def create_images(self):
        for game in self.active_game_list.values():

            if game.game_type == "lol" and game.game_key not in self.lol_finished_games_list.keys():
                print("Type: ",game.game_type, "|Key: ",  game.game_key,"|Active game id: ", game.active_game_id,
                      "|Finished: ", game.finished_state,game.match_finished,game.finished_state2, "|Data level: ",game.raw_data_level)
                self.lol_image_creator.create_image(game)







