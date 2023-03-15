from datetime import datetime, timedelta
import json

import numpy as np


class Match():
    def __init__(self, data, expire_time):
        self.last_scan_time = datetime.now()
        self.first_scan_time = datetime.now()
        self.expire_time = timedelta(minutes= expire_time)
        self.expired_status = False
        self.raw_data = data
        self.league_name = ""
        self.team_1_name = ""
        self.team_2_name = ""
        self.raw_data_level = ""
        self.game_type = ""




    def update_last_scan(self):
        self.last_scan_time = datetime.now()

    def check_if_expired(self):
        time_now = datetime.now()
        if time_now - self.last_scan_time > self.expire_time:
            # do function to remove the game and send info to controller
            self.expired_status = True
