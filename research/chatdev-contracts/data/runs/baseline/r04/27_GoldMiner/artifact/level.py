'''Level generation and rules.'''
import math
import random
from settings import *
from objects import make_object
class Level:
    def __init__(self, number):
        self.number = number
        self.target = LEVEL_BASE_TARGET + (number - 1) * LEVEL_TARGET_STEP
        self.time_limit = max(LEVEL_MIN_TIME, LEVEL_BASE_TIME - (number - 1) * LEVEL_TIME_STEP)
        self.swing_speed = min(CLAW_MAX_SWING_SPEED,
                               CLAW_BASE_SWING_SPEED + (number - 1) * CLAW_SWING_SPEED_PER_LEVEL)
        self.objects = []
        self._populate()
    def _composition(self):
        n = self.number
        counts = {
            'gold_small': 4 + n,
            'gold_medium': 2 + n // 2,
            'gold_large': 1 + n // 2,
            'rock_small': 1 + n // 2,
            'rock_large': 1 + n // 2,
            'bone': 1 + n // 2,
        }
        if n >= 2:
            counts['diamond'] = n // 2
            counts['tnt'] = 1 + n // 2
        if n >= 3:
            counts['mystery'] = 1
        return counts
    def _populate(self):
        counts = self._composition()
        for kind, count in counts.items():
            for _ in range(count):
                self._place_object(kind)
    def _place_object(self, kind):
        r = OBJECT_TYPES[kind]['radius']
        for attempt in range(200):
            x = random.uniform(PLAY_AREA_LEFT + r, PLAY_AREA_RIGHT - r)
            y = random.uniform(PLAY_AREA_TOP + r, PLAY_AREA_BOTTOM - r)
            if all(math.hypot(x - o.x, y - o.y) >= r + o.radius + 14 for o in self.objects):
                self.objects.append(make_object(kind, x, y))
                return
        # fallback: place anyway (should rarely happen)
        self.objects.append(make_object(kind, x, y))
    def remaining_value(self):
        total = 0
        for o in self.objects:
            if o.alive:
                total += MYSTERY_NOMINAL_VALUE if o.kind == 'mystery' else o.value
        return total
    def counts_by_kind(self):
        counts = {}
        for o in self.objects:
            if o.alive:
                counts[o.kind] = counts.get(o.kind, 0) + 1
        return counts
    def remove(self, obj):
        obj.alive = False
        if obj in self.objects:
            self.objects.remove(obj)
    def alive_objects(self):
        return [o for o in self.objects if o.alive]