"""
objects.py
Mineable objects for the Gold Miner game...
"""
import math
import random
import pygame
import settings as S
class GameObject:
    """Base class for everything lying in the mine that the claw can grab."""
    def __init__(self, x, y, kind, value, weight, radius):
        self.x = float(x)
        self.y = float(y)
        self.kind = kind
        self.value = value
        self.weight = weight
        self.radius = radius
        self.alive = True
        self.caught = False
    def distance_to(self, px, py):
        return math.hypot(px - self.x, py - self.y)
    def hits_point(self, px, py, point_radius=0.0):
        return self.distance_to(px, py) <= self.radius + point_radius
    def draw(self, surface):
        raise NotImplementedError
class Rock(GameObject):
    """A worthless-but-heavy rock; grabbing one wastes time for a tiny score."""
    def __init__(self, x, y, size):
        if size == 'small':
            cfg = (S.ROCK_SMALL_VALUE, S.ROCK_SMALL_WEIGHT, S.ROCK_SMALL_RADIUS)
        else:
            cfg = (S.ROCK_LARGE_VALUE, S.ROCK_LARGE_WEIGHT, S.ROCK_LARGE_RADIUS)
        super().__init__(x, y, 'rock_' + size, *cfg)
        self.size = size
        # random polygon shape
        self.shape = [(random.uniform(0.8, 1.15), random.uniform(0, math.pi)) for _ in range(8)]
        # hmm, better: angles evenly spaced with jitter, radii jitter