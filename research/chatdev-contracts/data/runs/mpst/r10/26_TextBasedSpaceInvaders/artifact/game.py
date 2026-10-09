import pygame
import sys
import random
from settings import Settings
from player import Player
from alien import AlienFleet
from bullet import Bullet
class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption(self.settings.caption)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, self.settings.font_size)
        self.big_font = pygame.font.SysFont(None, self.settings.big_font_size)
        self.reset_game()
    def reset_game(self):
        self.score = 0
        self.lives = self.settings.player_lives
        self.wave = 1
        self.state = 'playing'  # playing, game_over, victory... 
        self.player = Player(self.settings)
        self.player_bullets = []
        self.alien_bombs = []
        self.fleet = AlienFleet(self.settings, self.wave)
        self.last_shot_time = 0
    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)