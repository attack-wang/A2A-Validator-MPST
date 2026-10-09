'''ship.py — the player-controlled ship at the bottom of the screen.'''
import pygame
from assets import image_from_pattern, SHIP_PATTERN
class Ship:
    '''Represents the player's ship: horizontal movement and firing position.'''
    def __init__(self, game):
        '''Initialize the ship and set its starting position.'''
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()
        # Build the ship image from a pixel pattern (no external files needed)
        self.image = image_from_pattern(SHIP_PATTERN, (0, 220, 255), scale=3)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        # Small gap above the bottom edge
        self.rect.y -= 10
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
    def update(self):
        '''Update the ship's position based on movement flags.'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
    def blitme(self):
        '''Draw the ship on the screen.'''
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        '''Re-center the ship after losing a life.'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 10
        self.x = float(self.rect.x)