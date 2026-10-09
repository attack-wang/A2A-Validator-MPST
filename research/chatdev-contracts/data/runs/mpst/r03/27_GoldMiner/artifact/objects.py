import math, random
import pygame
from settings import *
class GameObject:
    def __init__(self, kind, x, y):
        spec = OBJECT_TYPES[kind]
        self.kind = kind
        self.x = x; self.y = y
        self.radius = spec["radius"]
        self.value = spec["value"]
        self.weight = spec["weight"]
        self.caught = False
        self.removed = False
        self.wobble = random.uniform(0, math.tau)  # for slight animation
    def update(self, dt): pass  # overridden by moving objects
    def draw(self, surface): raise NotImplementedError -> implement per subclass