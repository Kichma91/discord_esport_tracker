import json
from datetime import datetime, timedelta
import requests
import math
import os
import urllib.request
import time
import math

from game_objects.main_game import Match
from team_objects.lol_team import LolTeam
from player_objects.lol_player import LolPlayer
from constants import Constants


class LoLMatch(Match, Constants):
    """
    Main object for a game in LoL that stores all the info and functions connected to that single MATCH
    Lol has a MATCH between 2 teams and it lasts for x number of GAMES(like best of 5).
    Api calls:
    1. api call - get a list of MATCHES and find active MATCHES at the moment. This call is made outside, from
    the discord bot and this object is created for each active MATCH. This returns very little info about the match
    2. api call - get data about the MATCH, like teams, league data, block name, results and just broad info about the
    GAMES played inside that MATCH, like team sides, results and game status. You can get current and future games
    played. This api call is made when the object is initiated, because it will surely yield info, but that info may be
    without the games data, so we do not want it
    3. api call - get very detailed data about the GAME that is currently played. This wont work during the pick and ban
    phase, nor while the commercials are on or broadcasters talking in between games. It is requested with a time
    stamp which defines which moment of the game are you searching for( or better say a dict of 6 seconds of states).

    """
    def __init__(self, data, expire_time=5):
        # info like self.raw data is stored in main game object with super
        Match.__init__(self, data=data, expire_time=expire_time)
        Constants.__init__(self, type="lol")
        self.game_key = f'lol_{data["league"]["name"]}_{data["match"]["teams"][0]["name"]}_{data["match"]["teams"][1]["name"]}'
        self.game_type = "lol"

        self.block_name = self.raw_data["blockName"]
        self.league_name = self.raw_data["league"]["name"]
        self.league_slug = self.raw_data["league"]["slug"]
        self.league_event_id = self.raw_data["match"]["id"]
        self.games_count = self.raw_data["match"]["strategy"]["count"]
        self.raw_data_two = {}
        self.raw_data_three = {}
        self.teams = {}
        self.players = {}
        self.blue_team = ""
        self.red_team = ""
        self.next_game = ""
        self.teams_id_dict = {}
        self.active_game_id = None
        self.match_finished = False
        self.finished_time = None
        self.finished_state = False
        self.secondary_data_assigned = False
        self.third_data_assigned = False
        self.main_time_difference = timedelta()
        self.additional_time_difference = timedelta(seconds=5)
        for team in self.raw_data["match"]["teams"]:
            team_name = team["name"]
            if team_name not in self.teams.keys():
                team_code = team["code"]
                team_image_link = team["image"]
                team_image_name = team["image"].split("/")[-1]
                team_game_wins = team["result"]["gameWins"]
                self.teams[team_name] = LolTeam(name=team_name, code=team_code, image_link=team_image_link,
                                                image_name=team_image_name, game_wins=team_game_wins)
        # first assign immediately makes full data creation from first and secondary data
        self.first_assign()


    def first_assign(self):
        self.get_additional_data()
        self.assign_second_data()
        self.download_league_image()
        self.get_detailed_match_data()
        self.assign_third_data()
        self.update_player_data()
        self.get_next_game_data()

    def update_data(self):
        if self.match_finished or self.finished_state:
            return

        else:
            self.get_additional_data()
            if self.active_game_id:
                self.detect_end_game()
            else:
                self.assign_second_data()
                if not self.active_game_id:
                    self.get_next_game_data()

            self.get_detailed_match_data()
            if not self.third_data_assigned:
                self.assign_third_data()
            self.update_player_data()

    def detect_end_game(self):
        self.get_additional_data()
        matches_to_win = math.ceil(self.games_count / 2)
        for team in self.raw_data_two["data"]["event"]["match"]["teams"]:
            if team["result"]["gameWins"] >= matches_to_win:
                self.match_finished = True
                self.match_finished_time = datetime.now()
                return
        for game in self.raw_data_two["data"]["event"]["match"]["games"]:
            if game["id"] == self.active_game_id:
                if game["state"] != "inProgress":

                    print("FINISHED GAME")
                    self.get_next_game_data()

                    # create finished image
                    self.finished_time = datetime.now()
                    self.finished_state = True
                    return
            #DELETE PLAYER DATA/OBJECTS IN TEAMSž


                #create match finished image

    def reset_data(self):
        self.main_time_difference = timedelta()
        self.additional_time_difference = timedelta(seconds=5)
        self.raw_data_three = {}
        self.raw_data_level = "low"
        self.third_data_assigned = False
        self.secondary_data_assigned = False
        self.active_game_id = None
        self.finished_state = False

    def get_next_game_data(self):
        active_game_detected = False
        if self.active_game_id:
            for game in self.raw_data_two["data"]["event"]["match"]["games"]:
                if game["id"] == self.active_game_id:
                    active_game_detected = True
                if active_game_detected:
                    self.next_game = game
                    break
        else:
            for game in self.raw_data_two["data"]["event"]["match"]["games"]:
                if game["state"] == "unstarted":
                    self.next_game = game








    def get_additional_data(self):
        """
        2nd api call.
        """
        url = fr"https://esports-api.lolesports.com/persisted/gw/getEventDetails?hl=en-GB&id={self.raw_data['match']['id']}"
        # url = fr"https://feed.lolesports.com/livestats/v1/details/{int(data['match']['id'])}?startingTime={data['startTime']}"
        headers = {"authority": "esports-api.lolesports.com",
                   "method": "GET",
                   "scheme": "https",
                   "origin": "https://lolesports.com",
                   "referer": "https://lolesports.com",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                   "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"}
        r = requests.get(url, headers=headers)
        data2 = json.loads(r.content)
        # match shows if active game is going on
        self.raw_data_two = data2



    def assign_second_data(self):
        if "match" in self.raw_data_two["data"]["event"].keys():
            self.raw_data_level = "medium"
        else:
            self.raw_data_level = "low"
        if self.raw_data_level in ["medium", "high"]:
            self.league_id = self.raw_data_two["data"]["event"]["league"]["id"]
            self.league_image = self.raw_data_two["data"]["event"]["league"]["image"]
            self.league_image_name = self.raw_data_two["data"]["event"]["league"]["image"].split("/")[-1]
            self.games_list = {game["id"]: game for game in self.raw_data_two["data"]["event"]["match"]["games"]}
            for team in self.raw_data_two["data"]["event"]["match"]["teams"]:
                self.teams[team["name"]].id = team["id"]
                self.teams_id_dict[team["id"]] = self.teams[team["name"]]
            self.secondary_data_assigned = True
            self.streams = self.raw_data_two["data"]["event"]["streams"]
            for game in self.raw_data_two["data"]["event"]["match"]["games"]:
                if game["state"] == "inProgress":
                    self.active_game_id = game["id"]
                    for team in game["teams"]:
                        for team_object in self.teams.values():
                            if team_object.id == team["id"]:
                                if team["side"] == "blue":
                                    self.blue_team = team_object
                                elif team["side"] == "red":
                                    self.red_team = team_object
                                team_object.color = team["side"]
                    return


    def download_league_image(self):
        league_image_dir_listed = os.listdir(self.league_image_dir)
        if self.league_image_name in league_image_dir_listed:
            pass
        else:
            urllib.request.urlretrieve(self.league_image, fr"{self.league_image_dir}/{self.league_image_name}")
            time.sleep(0.5)

    def get_detailed_match_data(self):
        """
        get the third api call
        Time differences are needed to get the best time string to gather data , and store that string in object
        It doesnt include the request itself, which is in get_last_data function
        """

        if self.active_game_id:
            if self.main_time_difference > timedelta(seconds=5):
                time_string = self.get_time(self.main_time_difference + self.additional_time_difference)
                r = self.get_last_data(self.active_game_id, time_string)
            else:
                time_string = self.get_time()
                r = self.get_last_data(self.active_game_id, time_string)
                data_false = json.loads(r.content)
                message = data_false["message"]
                current_time = message.split("current time:")[1]
                current_time = current_time.split(".")[0]
                current_time_dt = datetime.strptime(current_time, r" %Y-%m-%dT%H:%M:%S")
                time_diff = datetime.now() - current_time_dt
                self.main_time_difference = time_diff
                while r.status_code == 400:
                    time_string = self.get_time(self.main_time_difference + self.additional_time_difference)
                    r = self.get_last_data(self.active_game_id, time_string)
                    self.additional_time_difference = self.additional_time_difference + timedelta(seconds=10)

            try:
                data3 = json.loads(r.content)
                if data3["esportsGameId"] == self.active_game_id:
                    if "frames" in data3.keys():
                        self.raw_data_level = "high"
                        self.raw_data_three = data3
            except (json.decoder.JSONDecodeError, KeyError):
                pass


    def get_last_data(self, game_id, time_stamp):
        headers = {"authority": "esports-api.lolesports.com",
                   "method": "GET",
                   "scheme": "https",
                   "origin": "https://lolesports.com",
                   "referer": "https://lolesports.com",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                                 " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                   "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"}
        url2 = fr"https://feed.lolesports.com/livestats/v1/window/{game_id}?startingTime={time_stamp}"
        r = requests.get(url2, headers=headers)
        return r

    def get_time(self, time_difference=timedelta()):
        time_now = datetime.now() - time_difference
        seconds = time_now.second

        seconds = seconds + (10 - (seconds % 10))  # round to 10-20-30-40-50 seconds
        if seconds == 60:
            seconds = 50

        time_string = time_now.strftime(f"%Y-%m-%dT%H:%M:{seconds}.000Z")
        return time_string

    def assign_third_data(self):
        if self.raw_data_level == "high":
            for player in self.raw_data_three["gameMetadata"]["blueTeamMetadata"]["participantMetadata"]:
                self.blue_team.players[player["participantId"]] = LolPlayer(player["summonerName"],
                                                                            player["participantId"],
                                                                            player["esportsPlayerId"],
                                                                            player["role"],
                                                                            player["championId"],
                                                                            "blue",
                                                                            self.blue_team.name,
                                                                            self.blue_team.id
                                                                            )
                self.blue_team.players_name_dict[player["summonerName"]] = self.blue_team.players[player["participantId"]]
            for player in self.raw_data_three["gameMetadata"]["redTeamMetadata"]["participantMetadata"]:
                self.red_team.players[player["participantId"]] = LolPlayer(player["summonerName"],
                                                                           player["participantId"],
                                                                           player["esportsPlayerId"],
                                                                           player["role"],
                                                                           player["championId"],
                                                                           "red",
                                                                           self.blue_team.name,
                                                                           self.blue_team.id
                                                                           )
                self.red_team.players_name_dict[player["summonerName"]] = self.red_team.players[player["participantId"]]
            self.third_data_assigned = True

    def update_player_data(self):
        if self.raw_data_level == "high" and self.third_data_assigned:
            self.last_frame = self.raw_data_three["frames"][-1]
            self.game_status = self.last_frame["gameState"]
            self.blue_team.gold = self.last_frame["blueTeam"]["totalGold"]
            self.blue_team.inhibitors = self.last_frame["blueTeam"]["inhibitors"]
            self.blue_team.towers = self.last_frame["blueTeam"]["towers"]
            self.blue_team.barons = self.last_frame["blueTeam"]["barons"]
            self.blue_team.total_kills = self.last_frame["blueTeam"]["totalKills"]
            self.blue_team.dragons = self.last_frame["blueTeam"]["dragons"]

            self.red_team.gold = self.last_frame["redTeam"]["totalGold"]
            self.red_team.inhibitors = self.last_frame["redTeam"]["inhibitors"]
            self.red_team.towers = self.last_frame["redTeam"]["towers"]
            self.red_team.barons = self.last_frame["redTeam"]["barons"]
            self.red_team.total_kills = self.last_frame["redTeam"]["totalKills"]
            self.red_team.dragons = self.last_frame["redTeam"]["dragons"]

            for blue_player in self.last_frame["blueTeam"]["participants"]:
                self.blue_team.players[blue_player["participantId"]].gold = blue_player["totalGold"]
                self.blue_team.players[blue_player["participantId"]].level = blue_player["level"]
                self.blue_team.players[blue_player["participantId"]].kills = blue_player["kills"]
                self.blue_team.players[blue_player["participantId"]].deaths = blue_player["deaths"]
                self.blue_team.players[blue_player["participantId"]].assists = blue_player["assists"]
                self.blue_team.players[blue_player["participantId"]].creep_score = blue_player["creepScore"]
                self.blue_team.players[blue_player["participantId"]].current_health = blue_player["currentHealth"]
                self.blue_team.players[blue_player["participantId"]].max_health = blue_player["maxHealth"]
            for red_player in self.last_frame["redTeam"]["participants"]:
                self.red_team.players[red_player["participantId"]].gold = red_player["totalGold"]
                self.red_team.players[red_player["participantId"]].level = red_player["level"]
                self.red_team.players[red_player["participantId"]].kills = red_player["kills"]
                self.red_team.players[red_player["participantId"]].deaths = red_player["deaths"]
                self.red_team.players[red_player["participantId"]].assists = red_player["assists"]
                self.red_team.players[red_player["participantId"]].creep_score = red_player["creepScore"]
                self.red_team.players[red_player["participantId"]].current_health = red_player["currentHealth"]
                self.red_team.players[red_player["participantId"]].max_health = red_player["maxHealth"]


















if __name__ == "__main__":
    # with open(r"C:\Users\Davor\PycharmProjects\discord_esport_tracker\assets\dirs.json", "r") as fp:
    #     dirs = json.load(fp)
    url = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-GB&leagueId=98767991302996019%2C100695891328981122%2C105266098308571975%2C107407335299756365%2C105266111679554379%2C98767991332355509%2C98767991310872058%2C98767991355908944%2C105709090213554609%2C98767991299243165%2C98767991349978712%2C101382741235120470%2C98767991314006698%2C104366947889790212%2C98767991343597634%2C98767975604431411%2C98767991295297326%2C105266101075764040%2C105266103462388553%2C105266108767593290%2C105266106309666619%2C105266094998946936%2C105266088231437431%2C105266074488398661%2C105266091639104326%2C99332500638116286%2C107921249454961575%2C107898214974993351%2C98767991335774713%2C108203770023880322%2C105549980953490846%2C101097443346691685%2C107582580502415838%2C107581050201097472%2C107603541524308819%2C107581669166925444%2C107598636564896416%2C107598951349015984%2C107582133359724496%2C107577980054389784%2C98767991325878492%2C108001239847565215"
    headers = {"authority": "esports-api.lolesports.com",
               "method": "GET",
               "scheme": "https",
               "origin": "https://lolesports.com",
               "referer": "https://lolesports.com",
               "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
               "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"}

    r = requests.get(url, headers=headers)
    data = json.loads(r.content)

    game_list = data["data"]["schedule"]["events"]
    lol_accepted_games = [x for x in game_list if x["state"] == "inProgress" and "match" in x.keys()]
    counter = 0
    game_objs = {}
    for y in lol_accepted_games:
        game_objs[counter] = LoLMatch(data=y)
        print(game_objs[counter].raw_data_level)
        counter +=1

    # game = game_objs.values()
    for game in game_objs.values():
        if game.raw_data_level == "high":
            with open("../raw_data_jsons/lol/lol_raw_1.json", "w") as fp:
                json.dump(game.raw_data, fp, indent=4)
            with open("../raw_data_jsons/lol/lol_raw_2.json", "w") as fp:
                json.dump(game.raw_data_two, fp, indent=4)
            with open("../raw_data_jsons/lol/lol_raw_3.json", "w") as fp:
                json.dump(game.raw_data_three, fp, indent=4)
            print("dumped info")



