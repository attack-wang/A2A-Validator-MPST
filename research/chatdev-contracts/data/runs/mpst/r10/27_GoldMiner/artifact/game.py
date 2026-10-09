"""Main game application: game states, HUD, rendering, and the main loop."""
import math
import sys
import pygame
import settings
from claw import Claw
from level import Level
class Game:
    """Top-level application: menu -> playing -> level_complete/game_over -> victory."""
    MENU, PLAYING, LEVEL_COMPLETE, GAME_OVER, VICTORY = (
        "menu", "playing", "level_complete", "game_over", "victory")
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.state = self.MENU
        self.level_number = 1
        self.score = 0
        self.time_left = 0.0
        self.level = None
        self.claw = None
        self.explosion_timer = 0
        self.explosion_pos = None
        self._start_level(self.level_number)
    def _start_level(self, number):
        self.level = Level(number)
        self.claw = Claw(self.level.swing_speed)
        self.time_left = float(self.level.time_limit)
        self.explosion_timer = 0
        self.explosion_pos = None
    def run(self):
        """Main loop: handle events, update, draw."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self._primary_action()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._primary_action()
    def _primary_action(self):
        """Space/Enter/click: launch the claw, or advance menu/screens."""
        if self.state == self.PLAYING:
            self.claw.launch()
        elif self.state == self.MENU:
            self.state = self.PLAYING
        elif self.state == self.LEVEL_COMPLETE:
            self.level_number += 1
            if self.level_number > settings.MAX_LEVEL:
                self.state = self.VICTORY
            else:
                self._start_level(self.level_number)
                self.state = self.PLAYING
        elif self.state in (self.GAME_OVER, self.VICTORY):
            self.level_number = 1
            self.score = 0
            self._start_level(1)
            self.state = self.PLAYING