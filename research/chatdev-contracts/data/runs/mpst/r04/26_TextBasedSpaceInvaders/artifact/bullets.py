'''Player and alien bullet sprites for the Space Invaders game.'''
import pygame
from settings import (BULLET_WIDTH, BULLET_HEIGHT, BULLET_SPEED,
                      ALIEN_BULLET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT,
                      YELLOW, RED)
class Bullet(pygame.sprite.Sprite):
    '''A player bullet that travels upward and removes itself off-screen.'''
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT), pygame.SRCALPHA)
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_y = float(self.rect.y)
    def update(self):
        self.pos_y -= BULLET_SPEED
        self.rect.y = round(self.pos_y)
        if self.rect.bottom < 0:
            self.kill()
class AlienBullet(pygame.sprite.Sprite):
    '''An alien bullet that travels downward and removes itself off-screen.'''
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT), pygame.SRCALPHA)
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_y = float(self.rect.y)
    def update(self):
        self.pos_y += ALIEN_BULLET_SPEED
        self.rect.y = round(self.pos_y)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()