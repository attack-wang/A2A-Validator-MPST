'''
game.py
Core Game class: main loop, state management, collisions, HUD rendering.
'''
import random
import sys
import pygame
import settings
from sprites import Player, Alien, Bullet
class Game:
    '''Manages the Space Invaders game loop, state, and rendering.'''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, settings.FONT_SIZE)
        self.big_font = pygame.font.SysFont(None, settings.BIG_FONT_SIZE)
        self.running = True
        self.reset()
    def reset(self):
        '''(Re)initialize all game objects and state for a fresh round.'''
        self.player = Player()
        self.aliens = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.direction = 1
        self.score = 0
        self.state = "playing"  # playing / game_over / victory
        self.last_alien_fire = 0
        self.create_aliens()
    def create_aliens(self):
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLS):
                self.aliens.add(Alien(row, col))
    def run(self):
        while self.running:
            self.delta = self.clock.tick(settings.FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()  # hmm, maybe just pygame.quit()