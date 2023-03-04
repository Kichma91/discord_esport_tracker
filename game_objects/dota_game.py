from game_objects.main_game import Match


class DotaMatch(Match):
    def __init__(self, data, expire_time = 5):
        super().__init__(data=data ,expire_time=expire_time)
        self.game_key = f'dota2_{data["league_id"]}_{data["match_id"]}'
        self.game_type = "dota2"

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
        self.league_id = self.raw_data["league_id"]


    def update_data(self, data):
        self.raw_data = data
        self.determine_data_quality()
        self.update_last_scan()
        self.assign_data()
        # create image




