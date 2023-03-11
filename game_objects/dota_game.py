from game_objects.main_game import Match
from constants import Constants
from team_objects.dota_team import DotaTeam



class DotaMatch(Match, Constants):
    def __init__(self, data, expire_time = 5):
        Match.__init__(data=data ,expire_time=expire_time)
        Constants.__init__(self, type="dota")
        self.game_key = f'dota2_{data["league_id"]}_{data["match_id"]}'
        self.game_type = "dota2"
        self.teams = {"radiant": None,
                      "dire": None}

    def __getattr__(self, item):
        if item == "state":
            if self.raw_data_level == "low":
                return "pick"
            elif self.raw_data_level == "high":
                return "inProgress"
        else:
            raise AttributeError(f"Attribute '{item}' does not exist")


    def determine_data_quality(self):
        running_game = True
        if "scoreboard" in self.raw_data.keys():
            if "picks" in self.raw_data["scoreboard"].keys():
                if len(self.raw_data["scoreboard"]["radiant"]["picks"]) == 5 and len(self.raw_data["scoreboard"]["dire"]["picks"]) == 5:
                    for team in ["radiant", "dire"]:
                        for player in self.raw_data["scoreboard"][team]["players"]:
                            if player["hero_id"] == 0:
                                running_game = False
                else:
                    running_game = False
            else:
                running_game = False
        else:
            running_game = False
        if running_game:
            self.raw_data_level = "high" # for running game
        else:
            self.raw_data_level = "low" # for hero selection


    def assign_data(self):
        if self.state == "pick":
            self.assign_pick_data()
        elif self.state == "inProgress":
            self.assign_active_data()

    def assign_pick_data(self):
        self.league_id = self.raw_data["league_id"]
        self.match_id = self.raw_data["match_id"]
        league_name = self.dota_league_data.loc[
            self.dota_league_data["League"] == self.raw_data["league_id"], "League Name"]
        self.leage_name = league_name.iloc[0]
        image_name_func = lambda: f"{self.league_name}.png" if f"{self.league_name}.png" in self.league_image_dir else "not_found"
        self.league_image_file = image_name_func()
        for team in ["radiant","dire"]:
            if f"{team}_team" in self.raw_data.keys() and self.teams[team] == "":
                self.teams[team] = DotaTeam(raw_data=self.raw_data[f"{team}_team"])






    def assign_active_data(self):
        pass


    def update_data(self, data):
        self.raw_data = data
        self.determine_data_quality()
        self.update_last_scan()
        self.assign_data()
        # create image




