import math
import random
import sys
import pygame
from settings import *
from claw import Claw
from level import Level
from ui import (Floater, Explosion, draw_hud, draw_menu, draw_level_clear,
                draw_game_over, build_background)
MENU, PLAYING, LEVEL_CLEAR, GAME_OVER = "menu", "playing", "level_clear", "game_over"
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.fonts = {
            "small": pygame.font.Font(None, 26),
            "medium": pygame.font.Font(None, 34),
            "large": pygame.font.Font(None, 48),
            "huge": pygame.font.Font(None, 72),
        }
        self.state = MENU
        self.level_number = 1
        self.total_score = 0
        self.floaters = []
        self.explosions = []
        self.background = build_background()
        self.clouds = [...]  # drifting clouds
        self.level = None
        self.claw = None
        self.level_score = 0
        self.time_left = 0.0
        self.message = ""
        self.end_reason = ""
        self.last_bonus = 0
    def reset_level(self):
        self.level = Level(self.level_number)
        self.claw = Claw()
        self.level_score = 0
        self.time_left = self.level.time_limit
        self.floaters = []
        self.explosions = []
    def start_game(self):
        self.level_number = 1
        self.total_score = 0
        self.reset_level()
        self.state = PLAYING
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()