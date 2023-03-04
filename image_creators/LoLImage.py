from PIL import Image, ImageDraw, ImageFont



class LoLImg():
    def __init__(self):
        self.x_positions = {
            "hero_img": 15,
            "player_name": 80,
            "hero_name": 83,
            "single_digit_lvl": 271,
            "double_digit_lvl": 265,
            "role": 310,
            "kills": 435,
            "creeps": 585,
            "gold": 670
                            }
        self.y_positions = {"blue":
                                {
                                    "names": [155, 223, 291, 360, 428],
                                    "heroes": [188, 256, 324, 393, 461],
                                    "role": [173,241,310,378,445],
                                    "kills": [170,238,307,375,442],
                                    "creep": [170,238,307,375,442],
                                    "gold": [170, 238, 307, 375, 442]
                                 },
                            "red":
                                {
                                    "names": [560, 628, 697, 766, 834],
                                    "heroes": [593, 661, 730, 799, 867],
                                    "role": [578, 646, 715, 783, 850],
                                    "kills": [575, 643, 712, 780, 847],
                                    "creep": [575, 643, 712, 780, 847],
                                    "gold": [575, 643, 712, 780, 847]
                                }
                            }
    def create_image(self):
