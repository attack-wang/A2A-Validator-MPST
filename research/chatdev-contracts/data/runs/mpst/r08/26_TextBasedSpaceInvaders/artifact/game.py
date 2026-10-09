'''Core game logic: state machine, updates, collisions, and rendering.'''
import random
import sys
import pygame
import settings
from entities import Player, AlienFleet, Bullet, Explosion
import ui
class Game:
    '''Runs the Space Invaders game loop and manages all game state.'''
    STATE_RUNNING = "running"
    STATE_GAME_OVER = "game_over"
    STATE_VICTORY = "victory"
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = ...
        self.score = 0
        self.player_bullets = []
        self.alien_bullets = []
        self.explosions = []
        self.player = Player()
        self.fleet = AlienFleet()
        self.fire_timer = ...
        self.start_new_game()
    def start_new_game(self):
        self.score = 0
        self.player = Player()
        self.fleet = AlienFleet()
        self.player_bullets = []
        self.alien_bullets = []
        self.explosions = []
        self.alien_fire_timer = random.uniform(0.5, settings.ALIEN_FIRE_INTERVAL)
        self.state = Game.STATE_RUNNING
    def run(self):
        '''Main loop: process events, update, draw, and tick the clock.'''
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            self.handle_events()
            if self.state == Game.STATE_RUNNING:
                self.update(dt)
            self.draw()
        pygame.quit()