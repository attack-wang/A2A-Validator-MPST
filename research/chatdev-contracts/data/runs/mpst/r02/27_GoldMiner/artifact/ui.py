'''
ui.py
'''
import math
import pygame
import settings
class FloatingText:
    def __init__(self, text, x, y, color=settings.WHITE, life=60):
        ...
    def update(self): ...
    def draw(self, surface, font): ...
def draw_world_background(surface):
    # sky band, ground line, dirt texture dots (precomputed?) 