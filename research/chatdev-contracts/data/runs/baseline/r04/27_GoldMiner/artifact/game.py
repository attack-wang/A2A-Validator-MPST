'''Main game controller: loop, states, events, updates, rendering.'''
import math
import random
import sys
import pygame
from settings import *
from level import Level
from claw import Claw
from ui import UI
from objects import make_object
MENU, PLAYING, PAUSED, LEVEL_COMPLETE, GAME_OVER = range(5)
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Gold Miner')
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.state = MENU
        self.level_number = 1
        self.total_score = 0
        self.reset_level(1)
    def reset_level(self, number):
        self.level = Level(number)
        self.claw = Claw(self.level.swing_speed)
        self.score = 0
        self.time_left = self.level.time_limit
        self.floaters = []
        self.particles = []
        self.shake = 0.0
        self.end_timer = None
    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()