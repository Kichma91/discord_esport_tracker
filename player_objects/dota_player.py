from constants import Constants


class DotaPlayer(Constants):
    def __init__(self, player_data):
        super().__init__(type="dota")
        self.raw_player_data = player_data
        self.id = player_data["account_id"]
        self.name = player_data["name"]
        self.hero_id = player_data["hero_id"]
        self.hero_name = self.dota_hero_ids[str(self.hero_id)]["localized_name"]

    def update_data(self, data):
        self.raw_update_data = data
        if self.hero_id != data["hero_id"]:
            print("WARNING WRONG HERO ID \n" * 100)

        self.player_slot = data["player_slot"]
        self.kills = data["kills"]
        self.deaths = data["death"]
        self.assists = data["assistss"]
        self.last_hits = data["last_hits"]
        self.denies = data["denies"]
        self.gold = data["gold"]
        self.level = data["level"]
        self.gpm = data["gold_per_min"]
        self.xpm = data["xp_per_min"]
        self.ultimate_state = data["ultimate_state"]
        self.ultimate_cooldown = data["ultimate_cooldown"]
        self.item_list = [data[f"item{i}"] for i in range(6)]
        self.respawn_timer = data["respawn_timer"]
        self.position_x = data["position_x"]
        self.position_y = data["position_y"]
        self.net_worth = data["net_worth"]

