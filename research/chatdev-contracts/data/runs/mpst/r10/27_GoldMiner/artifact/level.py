"""Level generation and difficulty scaling for Gold Miner."""
import math
import random
import settings
from objects import Gold, Rock, Diamond, TNT, MysteryBag
GOLD_KINDS = ("gold_small", "gold_medium", "gold_large")
ROCK_KINDS = ("rock_small", "rock_large")
class Level:
    """Holds the object field and difficulty parameters for one level."""
    def __init__(self, number):
        self.number = number
        config = settings.level_config(number)
        self.time_limit = config["time_limit"]
        self.target_gold = config["target_gold"]
        self.swing_speed = config["swing_speed"]
        self.objects = self.generate_objects(config)
    def generate_objects(self, config):
        """Place objects with rejection sampling so they never overlap.
        Difficulty scaling: higher levels add more TNT/rocks and push the
        most valuable gold deeper into the mine.
        """
        placed = []  # (obj, x, y, radius)
        objects = []
        def try_place(kind):
            for _ in range(200):
                x, y = self._random_position()
                radius = settings.OBJECT_STATS[kind]["radius"]
                if self._fits(x, y, radius, placed):
                    cls = KIND_TO_CLASS[kind]
                    obj = cls(kind, x, y)
                    objects.append(obj)
                    placed.append((obj, x, y, radius))
                    return True
            return False
        # Gold — deeper placement for bigger nuggets on higher levels
        for i in range(config["gold_count"]):
            kind = random.choice(GOLD_KINDS)
            try_place(kind)
        for _ in range(config["rock_count"]):
            try_place(random.choice(ROCK_KINDS))
        for _ in range(config["tnt_count"]):
            try_place("tnt")
        for _ in range(config["diamond_count"]):
            try_place("diamond")
        for _ in range(config["mystery_count"]):
            try_place("mystery_bag")
        return objects
    @staticmethod
    def _random_position():
        x = random.randint(settings.MINE_MARGIN, settings.SCREEN_WIDTH - settings.MINE_MARGIN)
        y = random.randint(settings.MINE_TOP, settings.MINE_BOTTOM)
        return x, y
    @staticmethod
    def _fits(x, y, radius, placed):
        gap = 10
        for _, ox, oy, orad in placed:
            if math.hypot(x - ox, y - oy) < radius + orad + gap:
                return False
        return True