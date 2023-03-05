from PIL import Image, ImageDraw, ImageFont
from constants import Constants


class LoLImg(Constants):
    def __init__(self):
        super().__init__(type="lol")
        self.active_game_template = Image.open(self.active_game_template_file).convert("RGBA")
        self.player_name_font = ImageFont.truetype("segoeuib.ttf", 19)
        self.player_hero_font = ImageFont.truetype("segoeuib.ttf", 17)
        self.player_role_font = ImageFont.truetype("segoeuib.ttf", 16)
        self.league_name_font = ImageFont.truetype("segoeuib.ttf", 27)
        self.team_name_font = ImageFont.truetype("segoeuib.ttf", 23)
        self.team_name_font_smaller = ImageFont.truetype("segoeuib.ttf", 19)
        self.team_info_small = ImageFont.truetype("segoeuib.ttf", 18)

        self.font_colors = {"main": (255,255,255),#(244, 217, 102),
                            "blue":(2, 166, 226),
                            "red": (181, 45, 45),
                            "league": (255, 255, 255)}
        self.game_object = None
        self.x_positions = {
            "league_img": 235,
            "league_name": 320,
            "league_block": 320,
            "league_games_played": 550,

            "team_name": 90,
            "team_image": 15,
            "team_wins": 400,
            "team_gold": 675,
            "team_inhibitors": 540,
            "team_towers": 540,
            "team_barons": 630,
            "team_dragons": 630,


            "hero_img": 15,
            "player_name": 80,
            "hero_name": 83,
            "single_digit_lvl": 270,
            "double_digit_lvl": 264,
            "role": 310,
            "kills": 440,
            "creep": 585,
            "gold": 670
                            }
        increment = 5
        self.y_positions = {
            "league_name": 10,
            "league_block": 40,
            "league_img": 0,
            "league_games_played": 20,
            "blue":
                {
                    "names": [155, 223, 291, 360, 428],
                    "level": [160, 228, 296, 365, 433],
                    "hero_images": [155, 222, 290, 358, 426],
                    "hero_names": [183, 251, 319, 388, 456],
                    "role": [173,241,310,378,445],
                    "kills": [170,238,307,375,442],
                    "creep": [170,238,307,375,442],
                    "gold": [170, 238, 307, 375, 442],
                    "team_image": 78,
                    "team_name": 95,
                    "team_wins": 95,
                    "team_gold": 115,
                    "team_inhibitors": 110+increment,
                    "team_towers": 80+increment,
                    "team_barons": 80+increment,
                    "team_dragons": 110+increment,
                 },
            "red":
                {
                    'names': [567, 635, 704, 773, 841],
                    'level': [572, 640, 709, 778, 846],
                    'hero_images': [567, 634, 702, 769, 837],
                    'hero_names': [595, 663, 732, 801, 869],
                    'role': [585, 653, 722, 790, 857],
                    'kills': [582, 650, 719, 787, 854],
                    'creep': [582, 650, 719, 787, 854],
                    'gold': [582, 650, 719, 787, 854],
                    'team_image': 494,
                    'team_name': 512,
                    'team_wins': 512,
                    'team_gold': 530,
                    'team_inhibitors': 525+increment,
                    'team_towers': 495+increment,
                    'team_barons': 495+increment,
                    'team_dragons': 525+increment
                }
            }
    def create_image(self, game_object):
        self.game_object = game_object
        if game_object.third_data_assigned:
            self.create_active_image()
        else:
            self.create_partial_image()

    def create_active_image(self):
        im1 = self.active_game_template.copy()
        im1_redrawer = ImageDraw.Draw(im1)

        league_img_file = fr"{self.league_image_dir}/{self.game_object.league_image_name}"
        league_img = Image.open(league_img_file)
        league_img = league_img.resize((80, 80))
        try:
            im1.paste(league_img,(self.x_positions["league_img"],self.y_positions["league_img"]),league_img)
        except ValueError:
            print(fr"BAD LEAGUE IMAGE FOR {self.game_object.league_image_name}")

        im1_redrawer.text((self.x_positions["league_block"], self.y_positions["league_block"]),
                          text=self.game_object.block_name,
                          font=self.player_hero_font,
                          fill=self.font_colors["league"])
        im1_redrawer.text((self.x_positions["league_name"], self.y_positions["league_name"]),
                          text=self.game_object.league_name,
                          font=self.league_name_font,
                          fill=self.font_colors["league"])

        total_games_played = self.game_object.red_team.game_wins + self.game_object.blue_team.game_wins
        games_played_string = f"GAME {total_games_played+1} / {self.game_object.games_count}"

        im1_redrawer.text((self.x_positions["league_games_played"], self.y_positions["league_games_played"]),
                          text=games_played_string,
                          font=self.league_name_font,
                          fill=self.font_colors["league"])





        for team in self.game_object.teams.values():
            y_positions = self.y_positions[team.color]
            team_img_file = fr"{self.team_image_dir}/{team.image_name}"
            team_img = Image.open(team_img_file)
            team_img = team_img.resize((70,70))
            im1.paste(team_img,(self.x_positions["team_image"], y_positions["team_image"]),team_img)
            if len(team.name) > 20:
                team_font = self.team_name_font_smaller
            else:
                team_font = self.team_name_font
            im1_redrawer.text((self.x_positions["team_name"], y_positions["team_name"]),
                              text=team.name,
                              font=team_font,
                              fill=self.font_colors["league"])
            im1_redrawer.text((self.x_positions["team_wins"], y_positions["team_wins"]),
                              text=fr"WINS: {str(team.game_wins)}",
                              font=self.player_name_font,
                              fill=self.font_colors["league"])

            im1_redrawer.text((self.x_positions["team_towers"], y_positions["team_towers"]),
                              text=str(team.towers),
                              font=self.team_info_small,
                              fill=self.font_colors[team.color])
            im1_redrawer.text((self.x_positions["team_inhibitors"], y_positions["team_inhibitors"]),
                              text=str(team.inhibitors),
                              font=self.team_info_small,
                              fill=self.font_colors[team.color])
            im1_redrawer.text((self.x_positions["team_barons"], y_positions["team_barons"]),
                              text=str(team.barons),
                              font=self.team_info_small,
                              fill=self.font_colors[team.color])
            im1_redrawer.text((self.x_positions["team_dragons"], y_positions["team_dragons"]),
                              text=str(len(team.dragons)),
                              font=self.team_info_small,
                              fill=self.font_colors[team.color])
            # team_gold = 0
            # for player in team.players.values():
            #     team_gold += int(player.gold)
            # if team_gold > 10000:
            team_gold = f"{round(int(team.gold)/1000,1)} K"
            im1_redrawer.text((self.x_positions["team_gold"], y_positions["team_gold"]),
                              text=str(team_gold),
                              font=self.team_info_small,
                              fill=self.font_colors[team.color])





            for i, player in enumerate(team.players.values()):
                kill_string = f"{player.kills} / {player.deaths} / {player.assists}"
                additional_kill_pixels = (12-len(kill_string)) * 5

                additional_role_pixels = (7-len(player.role))**1.5 * 2

                hero_img_file = f"{self.hero_image_dir}/{player.champion}.png"
                hero_img = Image.open(hero_img_file)
                hero_img = hero_img.resize((60, 60))

                im1.paste(hero_img, (self.x_positions["hero_img"],y_positions["hero_images"][i]))
                im1_redrawer.text((self.x_positions["player_name"], y_positions["names"][i]),
                                  text=player.name, font=self.player_name_font, fill=self.font_colors["main"])
                im1_redrawer.text((self.x_positions["hero_name"], y_positions["hero_names"][i]),
                                  text=player.champion, font=self.player_hero_font, fill=self.font_colors["main"])
                im1_redrawer.text((self.x_positions["role"] + additional_role_pixels, y_positions["role"][i]),
                                  text=player.role.upper(), font=self.player_role_font,
                                  fill=self.font_colors[team.color])
                im1_redrawer.text((self.x_positions["kills"]+additional_kill_pixels, y_positions["kills"][i]),
                                  text=kill_string, font=self.player_role_font, fill=self.font_colors[team.color])
                im1_redrawer.text((self.x_positions["creep"], y_positions["creep"][i]),
                                  text=str(player.creep_score), font=self.player_role_font,
                                  fill=self.font_colors[team.color])
                im1_redrawer.text((self.x_positions["gold"], y_positions["gold"][i]),
                                  text=str(player.gold), font=self.player_role_font,
                                  fill=self.font_colors[team.color])

                if player.level >= 10:
                    x_temp = self.x_positions["double_digit_lvl"]
                else:
                    x_temp = self.x_positions["single_digit_lvl"]
                im1_redrawer.text((x_temp, y_positions["names"][i]+17),
                                  text= str(player.level), font=self.player_hero_font,
                                  fill=self.font_colors["main"])

        im1.show()
        im1.save(f"{self.created_images_dir}/{self.game_object.game_key}.png")

    def create_partial_image(self):
        pass





