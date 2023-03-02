import os
import urllib.request
import time

class LolPlayer():
    def __init__(self, name, game_id, esports_id, role, champion_id, color, team_name, team_id,dirs):
        self.name = name
        self.game_id = game_id
        self.esports_id = esports_id
        self.role = role
        self.champion = champion_id
        self.color = color
        self.team_name = team_name
        self.team_id = team_id

        self.gold = 0
        self.level = 0
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.creep_score = 0
        self.current_health = 0
        self.max_health = 0
        self.dirs = dirs
        self.hero_image_dir = self.dirs["lol_heroes"]
        self.download_hero_image()

    def download_hero_image(self):
        hero_image_name = f"{self.champion}.png"
        hero_link = fr"https://ddragon.leagueoflegends.com/cdn/12.14.1/img/champion/{hero_image_name}"

        hero_image_dir_listed = os.listdir(self.hero_image_dir)
        if hero_image_name in hero_image_dir_listed:
            pass
        else:
            try:
                urllib.request.urlretrieve(hero_link, fr"{self.hero_image_dir}/{hero_image_name}")
                time.sleep(0.5)
            except:
                hero_link = fr"https://ddragon.leagueoflegends.com/cdn/13.3.1/img/champion/{hero_image_name}"
                urllib.request.urlretrieve(hero_link, fr"{self.hero_image_dir}/{hero_image_name}")
                time.sleep(0.5)
