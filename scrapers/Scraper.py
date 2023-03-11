import json
import asyncio
from asyncio import AbstractEventLoop
import requests
from requests.structures import CaseInsensitiveDict
import time
import aiohttp

from utilities import  client_id, secret , steam_auth_key




class AsyncScraper():
    def __init__(self):
        self.auth_twitch = self.get_twitch_auth()
        self.client_id_twitch = client_id
        self.active_game_list = []
        self.game_changes = []
        self.active_game_list_clean = []
        self.game_changes_clean = []
        self.data = []
        print(self.client_id_twitch)
        print(self.auth_twitch)

###############################
    @staticmethod
    def get_twitch_auth():
        url = "https://id.twitch.tv/oauth2/token"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"

        data = f"client_id={client_id}&client_secret={secret}&grant_type=client_credentials"
        resp = requests.post(url, headers=headers, data=data)
        resp_dict = json.loads(resp.content)
        return resp_dict["access_token"]

    async def get_lol_data(self):
        # url = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-GB&leagueId=98767991302996019%2C100695891328981122%2C105266098308571975%2C107407335299756365%2C105266111679554379%2C98767991332355509%2C98767991310872058%2C98767991355908944%2C105709090213554609%2C98767991299243165%2C98767991349978712%2C101382741235120470%2C98767991314006698%2C104366947889790212%2C98767991343597634%2C98767975604431411%2C98767991295297326%2C105266101075764040%2C105266103462388553%2C105266108767593290%2C105266106309666619%2C105266094998946936%2C105266088231437431%2C105266074488398661%2C105266091639104326%2C99332500638116286%2C107921249454961575%2C107898214974993351%2C98767991335774713%2C108203770023880322%2C105549980953490846%2C101097443346691685%2C107582580502415838%2C107581050201097472%2C107603541524308819%2C107581669166925444%2C107598636564896416%2C107598951349015984%2C107582133359724496%2C107577980054389784%2C98767991325878492%2C108001239847565215"
        url = "https://esports-api.lolesports.com/persisted/gw/getLive?hl=en-GB"
        headers = {"authority": "esports-api.lolesports.com",
                   "method": "GET",
                   "scheme": "https",
                   "origin": "https://lolesports.com",
                   "referer": "https://lolesports.com",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                   "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                html = await resp.text()
                data = json.loads(html)
                return data

    async def get_valorant_data(self):
        url = "https://esports-api.service.valorantesports.com/persisted/val/getSchedule?hl=en-GB&sport=val&eventState=inProgress"
        headers = {"authority": "esports-api.service.valorantesports.com",
                   "method": "GET",
                   "scheme": "https",
                   "origin": "https://valorantesports.com",
                   "referer": "https://valorantesports.com",
                   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                   "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                resp.raise_for_status()
                html = await resp.text()
                data = json.loads(html)
                return data

    async def get_dota_data(self):
        url = f"https://api.steampowered.com/IDOTA2Match_570/GetLiveLeagueGames/v1/?key={steam_auth_key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                html = await resp.text()
                data = json.loads(html)
                return data

    async def get_dota_endgame_data(self, match_id):
        url = f"https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/v1/?key=B8B1FD1109C9590694B5AE9C53C7998D&match_id={match_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                html = await resp.text()
                data = json.loads(html)
                return data

    async def scrape_all(self):
        print("Scraping")
        tasks = []
        self.data = []
        self.loop = asyncio.get_event_loop()
        # tasks.append((self.loop.create_task(self.get_valorant_data()),"valorant"))
        # tasks.append((self.loop.create_task(self.get_dota_data()),"dota"))
        tasks.append((self.loop.create_task(self.get_lol_data()),"lol"))

        for task,game_name in tasks:
            data = await task
            self.data.append((game_name,data))




if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    scraper = AsyncScraper()
    while True:
        asyncio.run(scraper.scrape_all())
        print(scraper.data["lol"], scraper.data["valorant"], scraper.data["dota"])
        time.sleep(5)



