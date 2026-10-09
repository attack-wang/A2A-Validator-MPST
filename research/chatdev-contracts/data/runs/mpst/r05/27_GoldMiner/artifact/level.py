"""Builds and tracks one level: objects, timer and gold target."""
import math
import random
import pygame
from settings import *
from objects import (Gold, Rock, Diamond, Skull, TNT, MysteryBag, Mole,
                     make_object)
class Level:
    """Builds and tracks one level: objects, timer and gold target."""
    def __init__(self, number):
        self.number = number
        self.time_limit = max(MIN_TIME, BASE_TIME - (number - 1) * TIME_PER_LEVEL)
        self.time_left = self.time_limit
        self.gold_target = BASE_TARGET + (number - 1) * TARGET_PER_LEVEL
        self.swing_speed = CLAW_SWING_SPEED + (number - 1) * CLAW_SWING_SPEED_PER_LEVEL
        self.objects = []
        self._populate()
    def _populate(self):
        counts = {
            'gold': 5 + self.number,
            'rock': 2 + self.number // 2,
            'diamond': max(0, self.number - 1),
            'skull': self.number // 2,
            'tnt': max(0, self.number - 3),
            'mystery': 1 if self.number >= 2 else 0,
            'mole': self.number // 3,
        }
        placed = []
        for kind, count in counts.items():
            for _ in range(count):
                pos = self._find_spot(placed)
                obj = make_object(kind, pos[0], pos[1], self.number)
                placed.append(obj)
                self.objects.append(obj)
    def _find_spot(self, placed, tries=200):
        x = OBJECT_MARGIN_X + 30
        y = OBJECT_MIN_Y
        for _ in range(tries):
            x = random.uniform(OBJECT_MARGIN_X + 30, SCREEN_WIDTH - OBJECT_MARGIN_X - 30)
            y = random.uniform(OBJECT_MIN_Y, OBJECT_MAX_Y)
            ok = True
            for other in placed:
                if math.hypot(x - other.x, y - other.y) < other.radius + 46:
                    ok = False
                    break
            if ok:
                return (x, y)
        return (x, y)  # last attempt anyway
    def update(self, dt):
        """Count down the level timer and animate moving objects (moles)."""
        self.time_left = max(0.0, self.time_left - dt)
        for obj in self.objects:
            if obj.alive and isinstance(obj, Mole):
                obj.update(dt)