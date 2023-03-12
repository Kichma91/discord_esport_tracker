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

        self.active_x_positions = {
            "league_img": 380,
            "league_name": 460,
            "team_img": 5,
            "team_name": 80,
            "team_wins": 295,
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
            "dmg": 1100
          }
        self.active_y_positions = {
            "player_difference": 48,
            "team_difference": 380,
            "main": 80,
            "player0_img": 116,
            "player0_name": 120,
            "player0_lvl": 140,
            "player0_hero":140,
            "player0_main":138
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



    def create_pick_image(self):
        pass
