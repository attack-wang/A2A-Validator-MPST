"""Level generation and progression for the Gold Miner game."""
import random
import config
from objects import (GoldSmall, GoldMedium, GoldLarge, Diamond,
                     RockSmall, RockLarge, Bone, TNT, MysteryBag)
class Level:
    def __init__(self, number):
        self.number = number
        self.time_limit = self._time_for(number)
        self.target_gold = self._target_for(number)
        self.gold_collected = 0
        self.objects = []
        self._populate()
    @staticmethod
    def _time_for(number):
        return max(config.MIN_TIME, config.START_TIME - (number - 1) * config.TIME_PER_LEVEL_DECREASE)
    @staticmethod
    def _target_for(number):
        return config.BASE_TARGET + (number - 1) * config.TARGET_STEP
    def _populate(self):
        n = self.number
        plan = [
            (GoldSmall, 4 + n),
            (GoldMedium, 2 + (n + 1) // 2),
            (GoldLarge, 1 + n // 3),
            (Diamond, n // 2),
            (RockSmall, 1 + n // 2),
            (RockLarge, n // 3),
            (Bone, 1 + n // 2),
            (TNT, n // 2),
            (MysteryBag, 1 if n >= 2 else 0),
        ]
        for cls, count in plan:
            for _ in range(count):
                obj = cls(0, 0)
                if not self._place(obj):
                    break
    def _place(self, obj):
        for _ in range(200):
            x = random.uniform(config.MINING_LEFT + obj.radius, config.MINING_RIGHT - obj.radius)
            y = random.uniform(config.MINING_TOP + obj.radius, config.MINING_BOTTOM - obj.radius)
            if all(not self._overlaps(obj, x, y, other) for other in self.objects):
                obj.x, obj.y = x, y
                self.objects.append(obj)
                return True
        return False
    @staticmethod
    def _overlaps(obj, x, y, other):
        dx = x - other.x
        dy = y - other.y
        return dx * dx + dy * dy < (obj.radius + other.radius + 6) ** 2
    def remove_destroyed(self):
        self.objects = [o for o in self.objects if not o.destroyed]