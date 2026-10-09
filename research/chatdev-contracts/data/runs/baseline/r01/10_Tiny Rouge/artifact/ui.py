'''
Rendering: map view, side panel (HP, level, monster stats), and overlays.
'''
import pygame
from constants import (...)
class UIRenderer:
    """Draws the whole game frame each tick."""
    def __init__(self, screen):
        self.screen = screen
        self.font_small = pygame.font.SysFont("consolas", 14)
        self.font_med = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_big = pygame.font.SysFont("consolas", 32, bold=True)