'''
game.py
Core game state machine and main loop for the Gold Miner game.
'''
import math
import random
import sys
import pygame
import settings
from claw import Claw, STATE_SWINGING
from level import generate_objects, level_time_limit, level_target
from objects import TNT, MysteryBag
from ui import UI
STATE_MENU = 'menu'
STATE_PLAYING = 'playing'
STATE_LEVEL_COMPLETE = 'level_complete'
STATE_GAME_OVER = 'game_over'
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UI()
        self.reset()
    def reset(self):
        self.state = STATE_MENU
        self.level = 1
        self.score = 0
        self.objects = []
        self.claw = Claw()
        self.time_left = 0.0
        self.target = 0
        self.explosions = []
        self.floating_texts = []
        self.level_result = None
    def start_level(self, level):
        self.level = level
        self.objects = generate_objects(level)
        self.claw.reset()
        self.time_left = level_time_limit(level)
        self.target = level_target(level)
        self.explosions = []
        self.floating_texts = []
        self.state = STATE_PLAYING
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if self.state == STATE_MENU:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start_level(1)
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        self.claw.launch()
                elif self.state == STATE_LEVEL_COMPLETE:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.start_level(self.level + 1)
                elif self.state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset()
    def update(self, dt):
        if self.state != STATE_PLAYING:
            return
        self.time_left -= dt
        self.claw.update(dt)
        # collision detection while extending
        if self.claw.state == 'extending':
            tx, ty = self.claw.tip_position
            for obj in self.objects:
                if obj.alive and obj.collides_with_point(tx, ty):
                    self.grab(obj)
                    break
        # deposit caught object
        if self.claw.state == 'swinging' and self.claw.caught is not None:
            self.deposit(self.claw.caught)
            self.claw.caught = None
        # update effects
        ...
        # check level end
        if self.score >= self.target:
            self.state = STATE_LEVEL_COMPLETE
            ...
        elif self.time_left <= 0:
            self.time_left = 0
            self.state = STATE_GAME_OVER
    def grab(self, obj):
        if isinstance(obj, TNT):
            self.explode(obj)
            self.claw.state = 'reeling'  # retract empty fast
        else:
            if isinstance(obj, MysteryBag):
                obj.reveal_value()
            obj.alive = False  # hmm, but we want to draw it while reeling
            self.claw.attach(obj)