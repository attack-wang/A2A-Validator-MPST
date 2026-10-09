"""Grabbable objects buried in the dirt, plus the factory that builds them."""
import math
import random
import pygame
from settings import *
class GameObject:
    """Base class for every grabbable item buried in the dirt."""
    def __init__(self, x, y, value, weight, radius, name):
        self.x = x
        self.y = y
        self.value = value
        self.weight = weight
        self.radius = radius
        self.name = name
        self.alive = True
        self.wobble = random.uniform(0, math.tau)
    def contains_point(self, px, py, extra=0.0):
        return math.hypot(px - self.x, py - self.y) <= self.radius + extra
    def update(self, dt):
        """Base classes are static; subclasses may override (e.g. Mole)."""
    def draw(self, surface):
        raise NotImplementedError
    # helpers
    def _polygon_points(self, n, irregularity, seed_offset=0.0):
        """Generate n points around the object centre with jittered radii."""
        pts = []
        for i in range(n):
            ang = (math.tau * i / n) + seed_offset
            r = self.radius * (1.0 + random.uniform(-irregularity, irregularity))
            pts.append((self.x + math.cos(ang) * r,
                        self.y + math.sin(ang) * r))
        return pts