'''Level generation and mining-field logic.'''
import random
import pygame
from settings import *
from objects import GameObject
FIELD_MARGIN_X = 40
FIELD_TOP_PAD = 45
FIELD_BOTTOM_PAD = 35
MIN_GAP = 12
class Level:
    '''One mining field: object layout, cash goal and time limit.'''
    def __init__(self, number):
        self.number = number
        self.objects = []
        self.goal = BASE_GOAL + (number - 1) * GOAL_STEP
        self.time_limit = max(MIN_TIME, BASE_TIME - (number - 1) * TIME_PER_LEVEL)
        self.generate()
    def swing_speed(self):
        return min(SWING_SPEED * (1 + 0.06 * (self.number - 1)), SWING_SPEED * 1.8)
    def generate(self):
        lvl = self.number
        plan = []
        plan += ["gold_large"] * (1 + lvl // 3)
        plan += ["gold_medium"] * (2 + lvl // 2)
        plan += ["gold_small"] * (3 + lvl)
        plan += ["rock_small"] * (2 + lvl)
        plan += ["rock_large"] * (1 + lvl // 2)
        plan += ["tnt"] * min(1 + lvl // 2, 6)
        if lvl >= 2:
            plan += ["diamond"] * (1 + (lvl - 1) // 3)
        plan += ["skull"] * (1 + lvl // 2)
        if lvl >= 3:
            plan += ["mystery"] * (1 + (lvl - 3) // 2)
        rng = random.Random()
        left = FIELD_MARGIN_X
        right = WIDTH - FIELD_MARGIN_X
        top = GROUND_Y + FIELD_TOP_PAD
        bottom = HEIGHT - FIELD_BOTTOM_PAD
        placed = []
        for kind in plan:
            obj = self._place(kind, rng, left, right, top, bottom, placed)
            if obj is not None:
                placed.append(obj)
                self.objects.append(obj)
    def _place(self, kind, rng, left, right, top, bottom, placed):
        obj = GameObject(kind, 0, 0)
        r = obj.radius
        for attempt in range(600):
            x = rng.uniform(left + r, right - r)
            y = rng.uniform(top + r, bottom - r)
            gap = MIN_GAP if attempt < 400 else 2
            if all(math.hypot(x - o.x, y - o.y) > r + o.radius + gap for o in placed):
                obj.x, obj.y = x, y
                return obj
        return None  # field too crowded; skip this one
    def object_at(self, x, y, radius):
        '''Return the first alive object whose body overlaps the claw tip area.'''
        for obj in self.objects:
            if obj.alive and math.hypot(x - obj.x, y - obj.y) <= radius + obj.radius:
                return obj
        return None
    def explode(self, tnt):
        '''Destroy everything (TNT included) inside the blast radius.'''
        destroyed = 0
        for obj in self.objects:
            if obj.alive and math.hypot(obj.x - tnt.x, obj.y - tnt.y) <= BLAST_RADIUS:
                obj.alive = False
                destroyed += 1
        return destroyed
    def draw(self, surface):
        for obj in self.objects:
            if obj.alive:
                obj.draw(surface)