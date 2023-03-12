from PIL import Image, ImageDraw, ImageFont

from constants import Constants


class DotaImg(Constants):
    def __init__(self):
        super().__init__(type="dota")
        self.im_show = False
        self.active_game_template = Image.open(self.active_game_template_file).convert("RGBA")
        self.partial_game_template = Image.open(self.partial_game_template_file).convert("RGBA")
        self.player_name_font = ImageFont.truetype("LSANS.TTF", 11)
        self.league_font = ImageFont.truetype("LSANS.TTF", 14)

        self.font_colors = {"main":(255,255,255)}

        self.active_x_positions = {
            "league_img": 380,
            "league_name": 460,
            "team_img": 5,
            "team_name": 80,
            "team_wins": 295,
            "player_name": 67,
            "player_lvl": 87,
            "player_hero": 130,
            "kills": 355,
            "deaths": 400,
            "assists": 435,
            "gold": 470,
            "item0":506,
            "item1": 569,
            "item2": 632,
            "item3": 695,
            "item4": 758,
            "item5": 821,
            "lhdn": 900,
            "gpm": 975,
            "xpm": 1030,
            "net_worth": 1100
          }
        self.active_y_positions = {
            "player_difference": 48,
            "team_difference": 380,
            "main": 80,
            "hero_img": 116,
            "player_name": 120,
            "player_lvl": 140,
            "player_hero": 140,
            "player_main": 138
        }



    def create_image(self,game_object):
        self.game_object = game_object
        if game_object.state == "inProgress":
            self.create_active_image()
        elif game_object.state == "pick":
            self.create_pick_image()

    def create_active_image(self):
        im1 = self.active_game_template.copy()
        im1_redrawer = ImageDraw.Draw(im1)
        league_img_file = fr"{self.league_image_dir}/{self.game_object.league_image_file}"
        try:
            league_img = Image.open(league_img_file)
            league_img = league_img.resize((80, 80))
            im1.paste(league_img, (self.active_x_positions["league_img"], self.active_y_positions["league_img"]),
                      league_img)
        except FileNotFoundError:
            pass
        im1_redrawer.text((self.active_x_positions["league_name"], self.active_y_positions["league_name"]),
                          text=self.game_object.league_name,
                          font=self.league_font,
                          fill=self.font_colors["main"])
        for i, team in enumerate([self.game_object.radiant_team,self.game_object.dire_team]):
            team_main_pixel_addition = i * self.active_y_positions["team_difference"]
            im1_redrawer.text((self.active_x_positions["team_name"],
                               self.active_y_positions["team_name"] + team_main_pixel_addition),
                              text=team.name,
                              font=self.league_font,
                              fill=self.font_colors["main"])
            team_image_file = fr"{self.team_image_dir}/{team.id}.png"
            team_image = Image.open(team_image_file)
            team_image = team_image.resize((80, 80))
            im1.paste(team_image,
                      (self.active_x_positions["team_img"],
                       self.active_y_positions["team_img"]+team_main_pixel_addition),
                      team_image)

            for i2, player in enumerate(team.players.values()):
                y_pixel_addition =  team_main_pixel_addition + (i2 * self.active_y_positions["player_difference"])

                hero_img_file = fr"{self.hero_image_dir}/{player.hero_name}.png"
                hero_img = Image.open(hero_img_file)
                im1.paste(hero_img,
                          (self.active_x_positions["hero_img"] ,self.active_y_positions["hero_img"]+ y_pixel_addition),
                          hero_img)
                im1_redrawer.text((self.active_x_positions["player_name"],
                                   self.active_y_positions["player_name"] + y_pixel_addition),
                                  text=player.name,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["player_lvl"],
                                   self.active_y_positions["player_lvl"] + y_pixel_addition),
                                  text=player.level,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["player_hero"],
                                   self.active_y_positions["player_hero"] + y_pixel_addition),
                                  text=player.hero_name,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["kills"],
                                   self.active_y_positions["main"] + y_pixel_addition),
                                  text=player.kills,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["deaths"],
                                   self.active_y_positions["main"] + y_pixel_addition),
                                  text=player.deaths,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["assists"],
                                   self.active_y_positions["main"] + y_pixel_addition),
                                  text=player.assists,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["gold"],
                                   self.active_y_positions["main"] + y_pixel_addition),
                                  text=player.gold,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                lhdn_string = fr"{player.last_hits}/{player.denies}"
                im1_redrawer.text((self.active_x_positions["lhdn"],
                                   self.active_y_positions["main"] + y_pixel_addition),
                                  text=lhdn_string,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["gpm"],
                                   self.active_y_positions["main"] + y_pixel_addition),
                                  text=player.gpm,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["xpm"],
                                   self.active_y_positions["main"] + y_pixel_addition),
                                  text=player.xpm,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])
                im1_redrawer.text((self.active_x_positions["net_worth"],
                                   self.active_y_positions["main"] + y_pixel_addition),
                                  text=player.net_worth,
                                  font=self.player_name_font,
                                  fill=self.font_colors["main"])



    def create_pick_image(self):
        pass
