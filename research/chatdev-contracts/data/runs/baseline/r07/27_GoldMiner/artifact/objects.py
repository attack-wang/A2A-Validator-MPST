'''Game object definitions: gold nuggets, rocks, diamonds, skulls and TNT.'''
import math
import random
import pygame
from settings import *
class GameObject:
    """Base class for all grabbable objects in the mine."""
    def __init__(self, x, y, value, weight, radius, obj_type):
        self.x = x
        self.y = y
        self.value = value
        self.weight = weight
        self.radius = radius
        self.type = obj_type
        self.alive = True
        self.being_reeled = False
        self.seed = random.uniform(0, math.tau)
    @property
    def collision_radius(self):
        return self.radius
    def draw(self, surface):
        raise NotImplementedError
class Gold(GameObject):
    ... (full implementation from objects.py)
class Diamond(GameObject):
    ... (from diamond.py)
class Rock(GameObject):
    ... (from rock.py)
class Skull(GameObject):
    ... (from skull.py)
class TNT(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, -TNT_PENALTY, 1.0, 16, 'tnt')
        self.exploded = False  # fix: initialize flag
    def draw(self, surface):
        ... (from tnt.py)