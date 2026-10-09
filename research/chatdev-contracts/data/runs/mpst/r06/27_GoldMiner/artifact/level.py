'''
Level generation and difficulty progression.
'''
import random
import settings
from objects import GoldNugget, Rock, Diamond, MysteryBag, TNT
# Playfield band where objects spawn (below the sky strip, above the bottom edge)
MINE_TOP = 150
MINE_BOTTOM = settings.SCREEN_HEIGHT - 40
MINE_LEFT = 50
MINE_RIGHT = settings.SCREEN_WIDTH - 50
class Level:
    def __init__(self, number):
        self.number = number
        self.time_limit = max(settings.MIN_TIME,
                              settings.START_TIME - (number - 1) * settings.TIME_DECREASE_PER_LEVEL)
        self.target = settings.TARGET_BASE + (number - 1) * settings.TARGET_GROWTH
        self.objects = self._generate_objects()
    def _generate_objects(self):
        '''Build the object list for this level; counts scale with difficulty.'''
        n = self.number
        objects = []
        # counts scale with level (ascending difficulty)
        gold_counts = {"small": 3 + n // 2, "medium": 2 + n // 2, "large": 1 + (n - 1) // 3}
        rock_counts = {"small": 1 + n // 2, "large": 1 + (n - 1) // 2}
        diamond_count = 1 if n >= 2 else 0
        tnt_count = min(1 + (n - 1) // 2, 5)
        mystery_count = 1 + (n - 1) // 3
        blueprint = []
        blueprint += [("gold", "small")] * gold_counts["small"]
        blueprint += [("gold", "medium")] * gold_counts["medium"]
        blueprint += [("gold", "large")] * gold_counts["large"]
        blueprint += [("rock", "small")] * rock_counts["small"]
        blueprint += [("rock", "large")] * rock_counts["large"]
        blueprint += [("diamond", None)] * diamond_count
        blueprint += [("tnt", None)] * tnt_count
        blueprint += [("mystery", None)] * mystery_count
        random.shuffle(blueprint)
        for kind, size in blueprint:
            obj = self._spawn(kind, size, objects)
            if obj is not None:
                objects.append(obj)
        return objects
    def _spawn(self, kind, size, placed, max_tries=200):
        '''Rejection-sample a free spot for a new object.'''
        for _ in range(max_tries):
            x = random.uniform(MINE_LEFT, MINE_RIGHT)
            y = random.uniform(MINE_TOP, MINE_BOTTOM)
            radius = self._preview_radius(kind, size)
            if all(math.hypot(...) for ...):  # need math import
                ...
        return None