import json
import time
import re

from selenium import webdriver
from selenium.webdriver.common.by import By



class CSGOscraper():
    def __init__(self):
        self.browser = webdriver.Firefox()
        self.main_url = "https://www.1337pro.com"
        self.csgo_url = "https://www.1337pro.com/en/csgo/match-scores/live"
        self.browser.get(self.csgo_url)
        time.sleep(5)

        self.matches_windows = {}


    def get_main_page_data(self):
        self.csgo_main_window = self.browser.window_handles[0]
        self.browser.switch_to.window(self.csgo_main_window)
        time.sleep(1)
        match_blocks = self.browser.find_elements(By.CLASS_NAME,"match-block")
        link_list = []
        for match in match_blocks:
            match2 = match.find_element(By.TAG_NAME,"a")
            link = match2.get_attribute("href")
            link_list.append(link)
        return link_list


    def open_new_links(self, link_list):
        links_to_remove = []
        for active_link in self.matches_windows.keys():
            if active_link not in link_list:
                self.browser.switch_to.window(self.matches_windows[active_link])
                self.browser.close()
                links_to_remove.append(active_link)
        for removed_link in links_to_remove:
            del self.matches_windows[removed_link]

        self.browser.switch_to.window(self.browser.window_handles[-1])
        number_of_tabs = len(self.browser.window_handles)

        tabs_created = 0
        for link in link_list:

            if link not in self.matches_windows.keys():
                self.browser.execute_script("window.open('');")
                self.browser.switch_to.window(self.browser.window_handles[number_of_tabs + tabs_created])
                self.browser.get(link)
                tab_id = self.browser.current_window_handle

                self.matches_windows[link] = tab_id
                tabs_created += 1



    def get_data(self):
        all_data = {"matches": []}

        for link, tab in self.matches_windows.items():
            match_data = {}
            match_data["link"] = link
            self.browser.switch_to.window(tab)
            time.sleep(0.5)
            match_block = self.browser.find_element(By.CLASS_NAME,"live-match-block")
            header_data = match_block.text.split("\n")

            match_data["team1"] = {}
            match_data["team2"] = {}
            for word in header_data[2:]:
                if re.match(r"\d - \d",word):
                    match_data["game_score"] = word
            match_data["time"] = header_data[3]
            match_data["team1"]["name"] = header_data[1]
            match_data["team1"]["players"] = []
            match_data["team2"]["name"] = header_data[4]
            match_data["team2"]["players"] = []


            navigation_panel = self.browser.find_element(By.CLASS_NAME,"match-detail__nav")
            navigation_panel_buttons = navigation_panel.find_elements(By.TAG_NAME,"li")
            for button in navigation_panel_buttons:
                if button.text == "INFO":
                    button.click()
                    time.sleep(0.5)
                    match_details_panel = self.browser.find_element(By.CLASS_NAME,"match-detail__container ")
                    stat_blocks = match_details_panel.find_elements(By.CLASS_NAME,"stats-block__content")
                    for statblock in stat_blocks[1:-2]:
                        for key, value in zip(statblock.text.split("\n")[::2], statblock.text.split("\n")[1::2]):
                            match_data[key] = value
                    for i, value in enumerate(stat_blocks[-2].text.split("\n")):
                        match_data[f"team{i + 1}"]["name"] = value

                if button.text == "SUMMARY":
                    button.click()
                    time.sleep(1)
                    match_details_panel = self.browser.find_element(By.CLASS_NAME,"match-detail__container ")
                    match_result = match_details_panel.find_element(By.CLASS_NAME,"match-intro__info")
                    match_data["match_score"] = match_result.text.split("\n")[1]
                    for team_data, team_dict in zip(self.browser.find_elements(By.CLASS_NAME,"match-summary__col"),
                                                    [match_data["team1"], match_data["team2"]]):
                        player_data = team_data.find_element(By.TAG_NAME,"tbody")
                        for player in player_data.find_elements(By.TAG_NAME,"tr"):
                            player_dict = {}
                            text = player.text.split(" ")
                            player_dict["name"] = text[0]
                            player_dict["K"] = text[1]
                            player_dict["D"] = text[2]
                            player_dict["A"] = text[3]
                            team_dict["players"].append(player_dict)
            all_data["matches"].append(match_data)
        # with open("test_data_csgo.json", "w") as fp:
        #     json.dump(all_data, fp, indent=4)

        return all_data

    def run_scrape(self):
        link_list= self.get_main_page_data()
        self.open_new_links(link_list)
        data = self.get_data()
        return data


if __name__ == "__main__":
    driver = CSGOscraper()
    data = driver.run_scrape()








