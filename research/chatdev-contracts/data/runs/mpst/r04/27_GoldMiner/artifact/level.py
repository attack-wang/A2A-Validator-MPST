"""Level generation and difficulty scaling for Gold Miner."""
import math
import random
import settings
from objects import create_object
class Level:
    """Holds the layout, time limit and goal for one level."""
    def __init__(self, number):
        self.number = number
        self.time_limit = self._time_limit()
        self.target = self._target()
        self.objects = self._generate_objects()
    def _time_limit(self):
        return max(settings.LEVEL_TIME_BASE - (self.number - 1) * settings.LEVEL_TIME_DECREASE,
                   settings.LEVEL_TIME_MIN)
    def _target(self):
        return 350 + (self.number - 1) * 300
    def _generate_objects(self):
        rng = random.Random(self.number * 1337 + 7)
        n_large_gold = 1 + (self.number // 3)
        n_medium_gold = 2 + self.number // 2
        n_small_gold = 3 + self.number // 2
        n_diamond = 1 if self.number >= 2 else 0
        if self.number >= 6:
            n_diamond += (self.number - 2) // 4
        n_large_rock = 1 + self.number // 2
        n_small_rock = 2 + self.number
        n_bone = 1 + self.number // 3
        n_tnt = self.number // 2
        n_mystery = 1 if self.number >= 3 else 0
        counts = [
            ("gold_large", n_large_gold),
            ("gold_medium", n_medium_gold),
            ("gold_small", n_small_gold),
            ("diamond", n_diamond),
            ("rock_large", n_large_rock),
            ("rock_small", n_small_rock),
            ("bone", n_bone),
            ("tnt", n_tnt),
            ("mystery", n_mystery),
        ]
        placed = []
        for kind, count in counts:
            self._place(kind, count, placed, rng)
        return placed
    def _place(self, kind, count, placed, rng):
        """Randomly place `count` objects of `kind`, avoiding overlaps and TNT blasts."""
        base_radius = settings.GOLD_SPECS[kind][0]
        for _ in range(count):
            for attempt in range(200):
                radius = base_radius
                x = rng.uniform(settings.MINE_LEFT + radius, settings.MINE_RIGHT - radius)
                y = rng.uniform(settings.MINE_TOP + radius, settings.MINE_BOTTOM - radius)
                ok = True
                for other in placed:
                    min_dist = other.radius + radius + 12
                    if kind == "tnt" and other.kind in settings.GOLD_KINDS:
                        min_dist = max(min_dist, settings.TNT_BLAST_RADIUS + other.radius + 6)
                    if math.hypot(other.x - x, other.y - y) < min_dist:
                        ok = False
                        break
                if ok:
                    placed.append(create_object(kind, x, y))
                    break