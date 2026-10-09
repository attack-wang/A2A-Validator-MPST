'''Main game loop: states, events, scoring, TNT blasts and level progression.'''
import pygame
import sys
from settings import *
from claw import Claw
from level import Level
from ui import UI, FloatingText
MENU = 'menu'
PLAYING = 'playing'
LEVEL_CLEAR = 'level_clear'
GAME_OVER = 'game_over'
WIN = 'win'
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.state = MENU
        self.level_number = STARTING_LEVEL
        self.score = 0
        self.total_score = 0
        self.time_left = BASE_TIME
        self.level = None
        self.claw = None
        self.float_texts = []
        self.explosions = []   # (x, y, age) blast animations
        self._build_level(self.level_number)
    # --- setup ---------------------------------------------------------
    def _build_level(self, number):
        self.level = Level(number)
        self.claw = Claw()
        # ascending difficulty: the claw swings faster on deeper levels
        self.claw.swing_speed = min(SWING_SPEED + (number - 1) * SWING_SPEED_INCREMENT, MAX_SWING_SPEED)
        self.score = 0
        self.time_left = self.level.time_limit
        self.float_texts = []
        self.explosions = []
    # --- events ---------------------------------------------------------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif self.state == MENU:
                    self.state = PLAYING
                elif self.state == PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.claw.launch()
                elif self.state == LEVEL_CLEAR:
                    self.level_number += 1
                    self._build_level(self.level_number)
                    self.state = PLAYING
                elif self.state in (GAME_OVER, WIN):
                    self.level_number = STARTING_LEVEL
                    self.total_score = 0
                    self._build_level(self.level_number)
                    self.state = MENU
            elif event.type == pygame.MOUSEBUTTONDOWN and self.state == PLAYING:
                self.claw.launch()