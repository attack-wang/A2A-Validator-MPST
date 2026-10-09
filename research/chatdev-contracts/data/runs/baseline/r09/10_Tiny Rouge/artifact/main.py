class Game:
    def __init__(self):
        self.level = 1
        self.rng = random.Random()
        self.generator = MapGenerator(self.rng)
        self.messages = []
        self.game_over = False
        self.victory_level = None
        self.player = None
        self.floor_version = 0
        self._load_floor(keep_hp=False)