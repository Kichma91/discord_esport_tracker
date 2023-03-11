import urllib.request
import time
import os
from constants import Constants

class DotaTeam(Constants):
    def __init__(self, raw_data):
        super().__init__(type="dota")
