'''
Main game class: state machine, event handling, update loop, rendering.
'''
import pygame
import sys
import settings
from claw import Claw
from level import Level
from hud import HUD
class Game:
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_LEVEL_COMPLETE = "level_complete"
    STATE_GAME_OVER = "game_over"
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.hud = HUD()
        self.claw = Claw()
        self.level_number = 1
        self.level = Level(self.level_number)
        self.gold = 0
        self.time_left = self.level.time_limit
        self.state = Game.STATE_MENU
        self.explosion_timer = 0.0
        self.explosion_pos = None
    def run(self):
        while True:
            dt = min(self.clock.tick(settings.FPS) / 1000.0, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == Game.STATE_MENU:
                        self.start_level(1)
                    elif self.state == Game.STATE_PLAYING:
                        self.claw.launch()
                    elif self.state == Game.STATE_LEVEL_COMPLETE:
                        self.start_level(self.level_number + 1)
                    elif self.state == Game.STATE_GAME_OVER:
                        self.start_level(1)
                elif event.key == pygame.K_ESCAPE and self.state == Game.STATE_PLAYING:
                    self.state = Game.STATE_MENU  # or quit? Let's go to menu
    def start_level(self, number):
        self.level_number = number
        self.level = Level(number)
        self.claw = Claw()
        self.time_left = self.level.time_limit
        if number == 1:
            self.gold = 0
        self.state = Game.STATE_PLAYING