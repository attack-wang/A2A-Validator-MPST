"""Rendering: board panel, candy sprites, HUD, popups, and overlays."""
import math
import pygame
import constants as c
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.Font(None, 44)
        self.font_med = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 24)
        self.sprites = [self._build_sprite(i) for i in range(c.NUM_CANDY_TYPES)]
        self.selected_surf = ... (border rect drawn directly)
    def _lighten(color, f): tuple(min(255, int(v + (255-v)*f)) for v in color)
    def _darken...
    def _build_sprite(self, type_id):
        surf = pygame.Surface((CELL_SIZE, CELL_SIZE), SRCALPHA)
        draw shape centered with radius ~ CELL_SIZE*0.38, color, plus gloss highlight
        return surf