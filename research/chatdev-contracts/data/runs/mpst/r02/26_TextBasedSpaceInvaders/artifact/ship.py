'''Player ship: horizontal movement and firing.'''
import pygame
from settings import (BLACK, GREEN, SHIP_SPEED, SHIP_WIDTH, SHIP_HEIGHT,
                      SCREEN_HEIGHT, PLAYER_BULLET_LIMIT)
class Ship(pygame.sprite.Sprite):
    '''The player-controlled ship at the bottom of the screen.'''
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SHIP_WIDTH, SHIP_HEIGHT), pygame.SRCALPHA)
        self._draw_ship()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)
        self.speed = SHIP_SPEED
        self.moving_left = False
        self.moving_right = False
        self.bullet_limit = PLAYER_BULLET_LIMIT
    def _draw_ship(self):
        '''Draw a simple cannon-shaped ship onto its surface.'''
        # body
        pygame.draw.rect(self.image, GREEN, (0, SHIP_HEIGHT - 12, SHIP_WIDTH, 12))
        # turret
        pygame.draw.rect(self.image, GREEN, (SHIP_WIDTH // 2 - 5, 0, 10, SHIP_HEIGHT - 12))
        # little side wings
        pygame.draw.polygon(self.image, GREEN, [(0, SHIP_HEIGHT - 12), (10, SHIP_HEIGHT - 22), (14, SHIP_HEIGHT - 12)])
        pygame.draw.polygon(self.image, GREEN, [(SHIP_WIDTH, SHIP_HEIGHT - 12), (SHIP_WIDTH - 10, SHIP_HEIGHT - 22), (SHIP_WIDTH - 14, SHIP_HEIGHT - 12)])
    def update(self):
        '''Move the ship horizontally, keeping it on screen.'''
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.speed
        if self.moving_right and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
    def center_ship(self):
        '''Reposition the ship at the center bottom (after losing a life).'''
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10)