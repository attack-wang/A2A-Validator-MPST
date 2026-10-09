'''
Main game class: state machine, game loop, collision and scoring logic.
'''
import math
import pygame
import settings
from claw import Claw
from level import Level
from hud import FloatingText, Explosion, draw_hud, draw_center_message
from sounds import SoundManager
MENU, PLAYING, LEVEL_COMPLETE, GAME_OVER = ...
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20, bold=True)  # or Font(None, ...)
        ...
        self.sounds = SoundManager()
        self.reset()
    def reset(self):
        self.level_number = 1
        self.total_money = 0
        self.start_level()
    def start_level(self):
        self.level = Level(self.level_number)
        self.claw = Claw()
        self.earned = 0
        self.time_left = self.level.time_limit
        self.state = PLAYING (or transition)
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            for event in pygame.event.get():
                ...
            self.update(dt)
            self.draw()
        pygame.quit()