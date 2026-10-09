'''Bullets fired by the ship and by aliens.'''
import pygame
from settings import (BULLET_SPEED, ALIEN_BULLET_SPEED, BULLET_WIDTH,
                      BULLET_HEIGHT, SCREEN_HEIGHT, CYAN, RED)
class Bullet(pygame.sprite.Sprite):
    '''A projectile that travels straight up or down the screen.'''
    def __init__(self, x, y, going_up=True):
        super().__init__()
        color = CYAN if going_up else RED
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y) if going_up else (x, y)
        self.speed = BULLET_SPEED if going_up else ALIEN_BULLET_SPEED
        self.going_up = going_up
    def update(self):
        if self.going_up:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        # Kill bullets that leave the screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()