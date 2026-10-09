'''
objects.py
Definitions of collectible items that appear in the mine.
Every item is drawn procedurally (no external image assets needed).
'''
import math
import random
import pygame
from settings import (OBJECT_SPECS, GOLD_COLOR, GOLD_DARK, ROCK_COLOR,
                      ROCK_DARK, DIAMOND_COLOR, DIAMOND_DARK, BONE_COLOR,
                      TNT_COLOR, TNT_DARK, BAG_COLOR, WHITE, BLACK, GREY)
_font_cache = {}
def _get_font(size):
    if size not in _font_cache:
        _font_cache[size] = pygame.font.Font(None, size)
    return _font_cache[size]
class GameObject:
    '''Base class for every collectible in the mine.'''
    def __init__(self, kind, x=None, y=None):
        spec = OBJECT_SPECS[kind]
        self.kind = kind
        self.x = x
        self.y = y
        self.radius = spec['radius']
        self.value = spec['value']
        self.weight = spec['weight']
        self.alive = True
        self.carried = False
        self.wobble = random.uniform(0, math.tau)
    @property
    def position(self):
        return (self.x, self.y)
    def draw(self, surface):
        '''Default drawing: a simple labelled circle (subclasses override).'''
        pygame.draw.circle(surface, GREY, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 2)
class Gold(GameObject):
    '''A shiny gold nugget; size variant is carried in `kind`.'''
    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        r = self.radius
        # lumpy nugget: main blob plus two smaller bumps
        pygame.draw.circle(surface, GOLD_COLOR, (x, y), r)
        pygame.draw.circle(surface, GOLD_COLOR, (x - r // 2, y + r // 3), int(r * 0.55))
        pygame.draw.circle(surface, GOLD_COLOR, (x + r // 2, y + r // 4), int(r * 0.5))
        pygame.draw.circle(surface, GOLD_DARK, (x, y), r, 2)
        # sparkle highlight
        pygame.draw.circle(surface, WHITE, (x - r // 3, y - r // 3), max(2, r // 5))