import pandas as pd
import json

class Constants():
    def __init__(self,type):
        if type == "lol":
            self.team_image_dir = "assets/lol/team_images"
            self.hero_image_dir = "assets/lol/hero_images"
            self.league_image_dir ="assets/lol/league_images"
            self.created_images_dir = "game_stats/lol"
            self.active_game_template_file = "assets/lol/template_full.png"
            self.partial_game_template_file = "assets/lol/template_partial.png"
        elif type == "dota":
            self.hero_image_dir = "assets/dota/dota_hero_icons"
            self.item_mage_dir = "assets/dota/dota_item_icons"
            self.team_image_dir = "assets/dota/dota_team_logos"
            self.league_image_dir = "assets/dota/dota_tournament_logos"
            self.league_data = "assets/dota/dota_leagues_data.csv"
            self.active_game_template_file = "assets/dota/active_template.png"
            self.partial_game_template_file = "assets/dota/pick_template.png"
            self.created_images_dir = "game_stats/dota"
        elif type == "valorant":
            pass
        elif type == "csgo":
            pass
        elif type == "controller":
            self.lol_created_images = "game_stats/lol"
            self.dota_created_images = "game_stats/dota"
            self.valorant_created_images = "game_stats/valorant"
            self.csgo_created_images = "game_stats/csgo"

        elif type == "payload":
            self.dota_league_data_file = r"assets/dota/dota_leagues_data.csv"
            self.dota_league_images_dir = r"assets/dota/dota_tournament_logos"