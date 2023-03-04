import asyncio
import json
import copy
import os
from multiprocessing import Pipe, Process, active_children, Lock
import time

import discord

from scrapers.Scraper import AsyncScraper
from utilities import discord_bot_token



"""
ako je prošao jedan dan, nek se updateaju podaci o ligi
riješiti logiku bota gdje objavljuje slike
umetnuti vrijeme u dota partiju
umetnuti skidanje match info-a

solve when bot joins new server
solve when admin deletes channel bot broadcasts into
solve when bot leaves server / server not in bots active list
"""

# pre code za koji se ne sjecam kako i zasto radi
intents = discord.Intents.default()
intents.message_content = True


class DiscordClient(discord.Client):
    def __init__(self, conn_send):
        super(DiscordClient, self).__init__(intents=intents)
        # scraper je importan iz scraper file-a
        self.scraper = AsyncScraper()
        # conn za slati podatke u drugi proces , koje scraper scrapea
        self.conn_send = conn_send
        self.discord_ready_state = False
        # server data contains all the data for each connected server, with setting set up for them

        with open(r"server_data.json", "r") as fp:
            self.server_data = json.load(fp)

        with open(r"assets/dirs.json", "r") as fp:
            self.directory_data = json.load(fp)
        # this is used when bot joins a new channel , then its added to server data
        self.new_guild_template = {
            "default_channel": None,
            "default_broadcast_channel": None,
            "active_game_list": ["valorant", "counter-strike", "lol", "dota2"],
            "spoiler": True,
            "broadcasts": True
        }
        self.active_game_data = {}

    # function to open server data
    def save_server_data(self):
        with open(r"server_data.json", "w") as fp:
            json.dump(self.server_data, fp, indent=4)

    # checks for guilds stored in data and adds new guilds
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        for guild in self.guilds:
            if str(guild.id) in self.server_data["guild_data"].keys():
                print(f"FOUND {guild.id} IN CONSTANTS ACTIVE GAME LIST")
            else:
                print(f"GUILD {guild.id} NOT FOUND STORED DATA, CREATING IT NOW")
                self.server_data["guild_data"][str(guild.id)] = copy.deepcopy(self.new_guild_template)
                self.save_server_data()
        self.discord_ready_state = True

    # async def setup_hook(self) -> None:
    #     self.bg_task = self.loop.create_task(self.get_scraped_data())

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        print("Message received")
        # this was option if we just want the messages to go in to broadcast channel
        # channel = self.server_data["guild_data"][str(message.guild.id)]["default_broadcast_channel"]

        channel = message.channel.id
        channel = self.get_channel(channel)  # function from discordbot library

        if message.content.startswith('!esport addgame'):
            message_split = message.content.split(" ")
            game_name = message_split[2].lower()
            if game_name in self.server_data["default_game_list"] and game_name not in \
                    self.server_data["guild_data"][str(message.guild.id)]["active_game_list"]:
                self.server_data["guild_data"][str(message.guild.id)]["active_game_list"].append(game_name)
                self.save_server_data()
                await channel.send(f'Game {game_name} has been added {message.author.mention}')
            else:
                if game_name not in self.server_data["default_game_list"]:
                    await channel.send(f"Please write correct name of the game {message.author.mention}, games are {self.server_data['default_game_list']}")
                if game_name in self.server_data["guild_data"][str(message.guild.id)]["active_game_list"]:
                    await channel.send(f"Game is already in the list {message.author.mention}")

        elif message.content.startswith('!esport removegame'):
            message_split = message.content.split(" ")
            game_name = message_split[2].lower()
            if game_name in self.server_data["default_game_list"] and game_name in self.server_data["guild_data"][str(message.guild.id)]["active_game_list"]:
                self.server_data["guild_data"][str(message.guild.id)]["active_game_list"].remove(game_name)
                self.save_server_data()
                await channel.send(f'Game {game_name} has been removed {message.author.mention}')
            else:
                if game_name not in self.server_data["default_game_list"]:
                    await channel.send(f"Please write correct name of the game {message.author.mention}, games are {self.server_data['default_game_list']}")
                if game_name in self.server_data["default_game_list"] and game_name not in self.server_data["guild_data"][str(message.guild.id)]["active_game_list"]:
                    await channel.send(f"Game is not in the list {message.author.mention}")

        elif message.content.startswith("!esport setup_table_channel"):
            message_split = message.content.split(" ")
            channel_name = message_split[2]
            channel_found = discord.utils.get(message.guild.channels,name = channel_name)
            if channel_found: # if we found the channel in server
                channel_id = channel_found.id
                self.server_data["guild_data"][str(message.guild.id)]["default_table_channel"] = channel_id
                self.save_server_data()
            else:
                await message.reply("Please input correct channel name", mention_author=True)

        elif message.content.startswith("!esport setup_broadcast_channel"):
            message_split = message.content.split(" ")
            channel_name = message_split[2]
            channel_found = discord.utils.get(message.guild.channels, name=channel_name)
            if channel_found:  # if we found the channel in server
                channel_id = channel_found.id
                self.server_data["guild_data"][str(message.guild.id)]["default_broadcast_channel"] = channel_id
                self.save_server_data()
            else:
                await message.reply("Please input correct channel name", mention_author=True)

        elif message.content.startswith("!esport broadcasts-on"):
            self.server_data["guild_data"][str(message.guild.id)]["broadcasts"] = True
            await message.reply("Broadcasts have been turned on", mention_author=True)

        elif message.content.startswith("!esport broadcasts-off"):
            self.server_data["guild_data"][str(message.guild.id)]["broadcasts"] = False
            await message.reply("Broadcasts have been turned off", mention_author=True)

        elif message.content.startswith("!esport spoiler-on"):
            self.server_data["guild_data"][str(message.guild.id)]["spoiler"] = True
            await message.reply("Spoilers have been turned on", mention_author=True)

        elif message.content.startswith("!esport spoiler-off"):
            self.server_data["guild_data"][str(message.guild.id)]["spoiler"] = False
            await message.reply("Spoilers have been turned off", mention_author=True)

        elif message.content.startswith("!esport"):
            help_string=f"""
            Write a help message here - TO DO###########################################################################################################
            """
            await channel.send(f'{help_string}')

    # function that cleanses the channel and reuploads all the images
    async def upload_images(self):
        csgo_images_folder = self.directory_data["cs_go_images"]
        dota_images_folder = self.directory_data["dota2_images"]
        lol_images_folder = self.directory_data["lol_images"]
        # we add up all the folders for the loop
        all_folders = [csgo_images_folder, dota_images_folder, lol_images_folder]
        # we then check which guilds have setup the channel for bot
        for guild in self.guilds:
            channel_id =  self.server_data["guild_data"][guild.id]["default_channel"]
            if not channel_id:
                #if not set up go to next guild
                continue
            else:
                # maybe redo this part so its not a for loop? !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                for channel in guild.channels:
                    if channel.id == channel_id:
                        #clean the channel
                        await channel.purge()
                        for folder in all_folders:
                            all_images = os.listdir(folder)
                            for image in all_images:
                                picture = discord.File(fr"{folder}\{image}")
                                await channel.send(file = picture)




    async def main_loop(self):
        """
        Main process of discord bot. It scrapes the data using functions in Scraper.py.
        When data is returned, it sends it to the second process for parsing and sleeps xy seconds,
        allowing the bot to respond to user messages
        """
        # this is also inherited discord.client function - waits till internal cache is
        await self.wait_until_ready()

        while True:
            pass

    async def setup_hook(self) -> None:
        # needed function to create a task for bot that will be looped
        self.bg_task = self.loop.create_task(self.main_loop())
        # self.bg_task_two = self.loop.create_task(self.broadcast_changes())



if __name__ == "__main__":
    try:
        #Locks used when bot reads images and second process creates images
        dota_lock = Lock()
        csgo_lock = Lock()
        valorant_lock = Lock()
        lol_lock = Lock()
        locks_dict = {"dota2:":dota_lock,
                      "csgo":csgo_lock,
                      "valorant":valorant_lock,
                      "lol":lol_lock}
        #pipe used for sending data between discord bot and parser
        conn_receive, conn_transmit = Pipe(duplex=True)
        #2nd process used for analyzing data, starting Reader that is imported from other file
        p1 = Process(target=Reader, kwargs={"conn_receive": conn_receive, "dota_lock":dota_lock,"csgo_lock":csgo_lock,
                                            "valorant_lock":valorant_lock,"lol_lock":lol_lock})
        p1.start()

        print("started parser process")
        time.sleep(25)
        print("starting discord bot")
        client = DiscordClient(conn_send=conn_transmit)
        client.run(discord_bot_token)




    finally:
        for child in active_children():
            child.terminate()