'''
Level generation and difficulty scaling: goals rise, time shrinks and
more obstacles (rocks, TNT) appear as levels progress.
'''
import math
import random
import settings
from objects import Gold, Rock, Diamond, TNT, MysteryBag
class Level:
    def __init__(self, number):
        self.number = number
        self.goal = self._compute_goal()
        self.time_limit = self._compute_time()
        self.objects = []
        self._generate_objects()
    def _compute_goal(self):
        """Minimum gold value required to clear the level."""
        return settings.BASE_TARGET + (self.number - 1) * settings.TARGET_STEP
    def _compute_time(self):
        """Time limit shrinks every level, down to MIN_TIME."""
        return max(settings.MIN_TIME,
                   settings.START_TIME - (self.number - 1) * settings.TIME_PER_LEVEL_DECREASE)
    def _generate_objects(self):
        """Populate the field; counts scale with the level number."""
        lvl = self.number
        gold_count = min(4 + lvl, 10)
        rock_count = min(1 + (lvl + 1) // 2, 7)
        tnt_count = min(max(0, (lvl - 1) // 2), 4)
        diamond_count = min(1 + (lvl - 1) // 3, 3)
        mystery_count = 1 if lvl >= 2 else 0
        # bigger nuggets become more common on later levels
        sizes = ['small', 'medium', 'large']
        size_weights = [max(60 - 5 * lvl, 20), 35, min(5 + 3 * lvl, 45)]
        for _ in range(gold_count):
            size = random.choices(sizes, weights=size_weights)[0]
            self._place(Gold(0, 0, size))
        for _ in range(rock_count):
            self._place(Rock(0, 0))
        for _ in range(diamond_count):
            self._place(Diamond(0, 0))
        for _ in range(tnt_count):
            self._place(TNT(0, 0))
        for _ in range(mystery_count):
            self._place(MysteryBag(0, 0))
    def _place(self, obj):
        """Try to drop obj at a random non-overlapping spot; True on success."""
        for _ in range(200):
            margin = obj.radius + 6
            x = random.uniform(settings.PLAY_AREA_LEFT + margin,
                               settings.PLAY_AREA_RIGHT - margin)
            y = random.uniform(settings.PLAY_AREA_TOP + margin,
                               settings.PLAY_AREA_BOTTOM - margin)
            # test the CANDIDATE position (x, y), not the object's current one
            if all(math.hypot(x - o.x, y - o.y) > obj.radius + o.radius + 8
                   for o in self.objects):
                obj.x, obj.y = x, y
                self.objects.append(obj)
                return True
        return False
    def alive_objects(self):
        """Objects still sitting in the field."""
        return [o for o in self.objects if o.alive]