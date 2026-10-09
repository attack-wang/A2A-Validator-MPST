"""Main game class: loop, states, rendering."""
import sys
import math
import random
import pygame
from config import *
from claw import Claw
from level import Level
from objects import GameObject
from hud import HUD, FloatingText
MENU, PLAYING, LEVEL_COMPLETE, GAME_OVER, PAUSED = "menu", "playing", "level_complete", "game_over", "paused"
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gold Miner")
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.SysFont("arial", 40, bold=True)
        self.font = pygame.font.SysFont("arial", 22)
        self.font_small = pygame.font.SysFont("arial", 14)
        self.hud = HUD(...)
        self.state = MENU
        self.level_number = 1
        self.level = None
        self.claw = Claw()
        self.gold = 0
        self.total_gold = 0
        self.floating_texts = []
        self.shake_time = 0.0
        self.show_labels = True
        self.background = self._make_background()  # pre-render static background
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()