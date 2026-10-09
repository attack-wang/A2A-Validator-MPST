'''
ui.py
HUD and screen rendering helpers: score/time/level display, claw position
readout, menu, level-complete and game-over screens.
'''
import pygame
import settings
class UI:
    def __init__(self):
        pygame.font.init()
        self.font_big = pygame.font.SysFont('arial', 48, bold=True)
        self.font_medium = pygame.font.SysFont('arial', 28, bold=True)
        self.font_small = pygame.font.SysFont('arial', 20)
        self.font_tiny = pygame.font.SysFont('arial', 16)
    def draw_hud(self, surface, level, score, target, time_left, claw):
        # top bar
        # Level | Score/Target | Time | claw position readout
        ...
    def draw_world_background(self, surface):
        # sky, ground, dirt texture dots
        ...
    def draw_menu(self, surface): ...
    def draw_level_complete(self, surface, level, score, bonus): ...
    def draw_game_over(self, surface, level, score): ...
    def draw_center_text(...)