"""
level.py
Level generation and management...
"""
import math
import random
import settings as S
from gold import Gold
from objects import Rock, Diamond, Bone, TNT
class Level:
    def __init__(self, number, rng=None):
        self.number = number
        self.rng = rng or random.Random()
        self.time_limit = max(S.MIN_TIME_LIMIT,
                              S.START_TIME_LIMIT + S.TIME_PER_LEVEL * (number - 1))
        self.target = S.BASE_TARGET + S.TARGET_INCREMENT * (number - 1)
        self.swing_speed = min(S.MAX_SWING_SPEED,
                               S.BASE_SWING_SPEED + S.SWING_SPEED_INCREMENT * (number - 1))
        self.objects = []
        self._generate_objects()
        self.time_left = self.time_limit
    def _count(self, base, per_level, min_level=1):
        if self.number < min_level:
            return 0
        return int(round(base + per_level * (self.number - min_level)))
    def _generate_objects(self):
        """Spawn this level's objects; higher levels ⇒ more rocks/TNT/diamonds."""
        plan = [
            (lambda: Gold(0, 0, 'large'), S.LARGE_GOLD_BASE, S.LARGE_GOLD_PER_LEVEL, 1),
            (lambda: Gold(0, 0, 'medium'), S.MEDIUM_GOLD_BASE, S.MEDIUM_GOLD_PER_LEVEL, 1),
            (lambda: Gold(0, 0, 'small'), S.SMALL_GOLD_BASE, S.SMALL_GOLD_PER_LEVEL, 1),
            (lambda: Diamond(0, 0), S.DIAMOND_BASE, S.DIAMOND_PER_LEVEL, S.DIAMOND_MIN_LEVEL),
            (lambda: Rock(0, 0, 'small' if self.rng.random() < 0.6 else 'large'),
             S.ROCK_BASE, S.ROCK_PER_LEVEL, 1),
            (lambda: Bone(0, 0), S.BONE_BASE, S.BONE_PER_LEVEL, S.BONE_MIN_LEVEL),
            (lambda: TNT(0, 0), S.TNT_BASE, S.TNT_PER_LEVEL, S.TNT_MIN_LEVEL),
        ]
        for factory, base, per_level, min_level in plan:
            for _ in range(self._count(base, per_level, min_level)):
                self._place(factory())
    def _place(self, obj):
        """Try to drop the object somewhere free; skip it if the mine is full."""
        for _ in range(200):
            r = obj.radius
            x = self.rng.uniform(S.MINE_MARGIN_X + r, S.SCREEN_WIDTH - S.MINE_MARGIN_X - r)
            y = self.rng.uniform(S.MINE_TOP + r, S.MINE_BOTTOM - r)
            ok = True
            for other in self.objects:
                if math.hypot(x - other.x, y - other.y) < r + other.radius + 14:
                    ok = False
                    break
            if ok:
                obj.x, obj.y = x, y
                self.objects.append(obj)
                return True
        return False
    def alive_objects(self):
        return [o for o in self.objects if o.alive]