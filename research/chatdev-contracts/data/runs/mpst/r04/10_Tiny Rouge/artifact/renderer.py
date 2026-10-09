"""Pygame renderer: draws the 80x80 grid, entities, and the minimal UI sidebar."""
import pygame
import config
class Renderer:
    def __init__(self, screen):
        self.screen = screen
        pygame.font.init() — actually pygame.init() in main covers font? pygame.init() initializes font module too. I'll call pygame.font.init() defensively.
        self.font_small = pygame.font.SysFont("consolas,monospace", 14) — use Font(None, size) to avoid missing fonts: pygame.font.Font(None, 16).
        self.font_big = pygame.font.Font(None, 32)
    def draw(self, game):
        fill bg
        draw map area: for each tile draw wall/floor; draw door, chests, monsters, player.
        draw sidebar: level, HP bar, adjacent monsters stats, log.
        if dead: overlay.