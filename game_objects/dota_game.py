from game_objects.main_game import Match
from constants import Constants
from team_objects.dota_team import DotaTeam



class DotaMatch(Constants):
    def __init__(self, data):
        Constants.__init__(self, type="dota")
        self.game_key = f'dota_{data["league_id"]}_{data["match_id"]}'
        self.game_type = "dota"
        self.teams = {}
        self.update_data(data)

    def __setattr__(self, name, value):
        if name in ["raw_data", "raw_data_level", "state", "teams"]:
            super().__setattr__(name, value)
        else:
            if hasattr(self,name):
                pass
            else:
                super().__setattr__(name, value)




    def update_data(self, data):
        self.raw_data = data
        self.determine_data_quality()
        self.assign_data()
        # create image


    def determine_data_quality(self):
        running_game = True
        if "scoreboard" in self.raw_data.keys():

            if "picks" in self.raw_data["scoreboard"]["radiant"].keys() and "picks" in self.raw_data["scoreboard"]["dire"].keys():
                if len(self.raw_data["scoreboard"]["radiant"]["picks"]) == 5 and len(self.raw_data["scoreboard"]["dire"]["picks"]) == 5:
                    for team in ["radiant", "dire"]:
                        for player in self.raw_data["scoreboard"][team]["players"]:
                            if player["hero_id"] == 0:
                                print("failed on player_id")
                                running_game = False
                else:
                    running_game = False
                    print("failed on picks len")
            else:
                running_game = False
                print("failed on picks")
        else:
            running_game = False
            print("failed on scoreboard")
        print(running_game)
        if running_game:
            self.state = "inProgress" # for running game
        else:
            self.state = "pick" # for hero selection

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
        self.league_name = league_name.iloc[0]
        # print(league_name)
        image_name_func = lambda: f"{self.league_name}.png" if f"{self.league_name}.png" in self.league_image_dir else "not_found"
        self.league_image_file = image_name_func()
        for team in ["radiant","dire"]:
            if f"{team}_team" in self.raw_data.keys():
                if team == "radiant":
                    self.radiant_team = DotaTeam(raw_data=self.raw_data[f"{team}_team"], side=team)
                    self.teams[team] = self.radiant_team
                    self.radiant_team.game_wins = self.raw_data["radiant_series_wins"]
                elif team == "dire":
                    self.dire_team = DotaTeam(raw_data=self.raw_data[f"{team}_team"], side=team)
                    self.teams[team] = self.dire_team
                    self.dire_team.game_wins = self.raw_data["dire_series_wins"]

            if "scoreboard" in self.raw_data.keys():
                if "picks" in self.raw_data["scoreboard"][team].keys():
                    self.teams[team].picks = self.raw_data["scoreboard"][team]["picks"]
                if "bans" in self.raw_data["scoreboard"][team].keys():
                    self.teams[team].bans = self.raw_data["scoreboard"][team]["bans"]


    def assign_active_data(self):
        self.league_id = self.raw_data["league_id"]
        self.match_id = self.raw_data["match_id"]
        league_name = self.dota_league_data.loc[
            self.dota_league_data["League"] == self.raw_data["league_id"], "League Name"]
        self.league_name = league_name.iloc[0]
        image_name_func = lambda: f"{self.league_name}.png" if f"{self.league_name}.png" in self.league_image_dir else "not_found"
        self.league_image_file = image_name_func()
        self.duration = self.raw_data["scoreboard"]["duration"]

        # first team assign
        self.radiant_team = DotaTeam(raw_data=self.raw_data["radiant_team"], side="radiant")
        self.teams["radiant"] = self.radiant_team
        self.dire_team = DotaTeam(raw_data=self.raw_data["dire_team"], side="dire")
        self.teams["dire"] = self.dire_team

        self.radiant_team.assign_player_data(all_player_data=self.raw_data["players"], team_number=0)
        self.dire_team.assign_player_data(all_player_data=self.raw_data["players"], team_number=1)
        self.radiant_team.update_player_data(self.raw_data["scoreboard"]["radiant"]["players"])
        self.dire_team.update_player_data(self.raw_data["scoreboard"]["dire"]["players"])





