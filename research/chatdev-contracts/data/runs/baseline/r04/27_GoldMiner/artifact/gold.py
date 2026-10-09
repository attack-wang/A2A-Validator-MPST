'''Concrete item classes: Gold, Rock, Diamond, Bone, TNT, MysteryBag.'''
import math
import random
import pygame
from objects import GameObject
from settings import *
class Gold(GameObject):
    def __init__(self, size, x, y):
        kind = f'gold_{size}'
        spec = OBJECT_TYPES[kind]
        super().__init__(kind, x, y, spec['radius'], spec['value'], spec['reel_time'])
        self.size = size
    def draw(self, surface):
        r = self.radius
        cx, cy = int(self.x), int(self.y)
        pygame.draw.circle(surface, COLOR_GOLD_DARK, (cx, cy), r)
        pygame.draw.circle(surface, COLOR_GOLD, (cx - r//4, cy - r//4), int(r*0.8))
        pygame.draw.circle(surface, (255, 240, 160), (cx - r//3, cy - r//3), max(2, r//4))
        # outline
        pygame.draw.circle(surface, COLOR_GOLD_DARK, (cx, cy), r, 2)