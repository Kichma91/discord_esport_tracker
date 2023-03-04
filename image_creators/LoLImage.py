from PIL import Image, ImageDraw, ImageFont
from constants import Constants


class LoLImg(Constants):
    def __init__(self):
        super().__init__(type="lol")
        self.active_game_template = Image.open(self.active_game_template_file).convert("RGBA")
        self.player_name_font = ImageFont.truetype("segoeuib.ttf", 20)
        self.player_hero_font = ImageFont.truetype("segoeuib.ttf", 18)
        self.player_role_font = ImageFont.truetype("segoeuib.ttf", 16)
        self.font_colors = {"main": (244, 217, 102),
                            "blue":(2, 166, 226),
                            "red": (181, 3, 4)}
        self.game_object = None
        self.x_positions = {
            "league_img": 0,
            "league_name": 0,
            "league_block": 0,
            "league_games_played":0,

            "blue_team_name": 0,
            "blue_team_image": 0,
            "blue_team_wins": 0,
            "blue_team_gold": 0,
            "blue_team_inhibitors": 0,
            "blue_team_towers": 0,
            "blue_team_barons": 0,
            "blue_team_dragons": 0,


            "red_team_name": 0,


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
        self.y_positions = {"blue":
                                {
                                    "names": [155, 223, 291, 360, 428],
                                    "level": [160, 228, 296, 365, 433],
                                    "hero_images": [155, 223, 291, 360, 428],
                                    "hero_names": [188, 256, 324, 393, 461],
                                    "role": [173,241,310,378,445],
                                    "kills": [170,238,307,375,442],
                                    "creep": [170,238,307,375,442],
                                    "gold": [170, 238, 307, 375, 442]
                                 },
                            "red":
                                {
                                    "names": [560, 628, 697, 766, 834],
                                    "level": [565, 633, 702, 771, 839],
                                    "hero_images": [560, 628, 697, 766, 834],
                                    "hero_names": [593, 661, 730, 799, 867],
                                    "role": [578, 646, 715, 783, 850],
                                    "kills": [575, 643, 712, 780, 847],
                                    "creep": [575, 643, 712, 780, 847],
                                    "gold": [575, 643, 712, 780, 847]
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

        im1_redrawer.text((self.x_positions["kills"] + additional_kill_pixels, y_positions["kills"][i]),
                          text=kill_string, font=self.player_role_font, fill=self.font_colors[team.color])





        for team in self.game_object.teams.values():
            y_positions = self.y_positions[team.color]
            for i, player in enumerate(team.players.values()):
                kill_string = f"{player.kills} / {player.deaths} / {player.assists}"
                additional_kill_pixels = (12-len(kill_string)) * 5

                additional_role_pixels = (7-len(player.role))**1.5 * 2

                hero_img_file = f"{self.hero_image_dir}/{player.champion}.png"
                hero_img = Image.open(hero_img_file)
                hero_img = hero_img.resize((60,60))

                im1.paste(hero_img, (self.x_positions["hero_img"],y_positions["hero_images"][i]))
                im1_redrawer.text((self.x_positions["player_name"], y_positions["names"][i]),
                                  text= player.name, font=self.player_name_font, fill=self.font_colors["main"])
                im1_redrawer.text((self.x_positions["hero_name"], y_positions["hero_names"][i]),
                                  text=player.champion, font=self.player_hero_font, fill=self.font_colors["main"])
                im1_redrawer.text((self.x_positions["role"] + additional_role_pixels, y_positions["role"][i]),
                                  text=player.role.upper(), font=self.player_role_font, fill=self.font_colors[team.color])
                im1_redrawer.text((self.x_positions["kills"]+additional_kill_pixels, y_positions["kills"][i]),
                                  text=kill_string, font=self.player_role_font, fill=self.font_colors[team.color])
                im1_redrawer.text((self.x_positions["creep"], y_positions["creep"][i]),
                                  text=str(player.creep_score), font=self.player_role_font, fill=self.font_colors[team.color])
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





