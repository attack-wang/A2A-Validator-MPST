'''
ship.py
Defines the player's ship: horizontal movement and rendering.
'''
import pygame
import settings
class Ship:
    """The player's ship at the bottom of the screen."""
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # Build the ship rect (drawn as a polygon, rect used for positioning/collisions)
        self.width, self.height = 48, 32
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom -= 10
        # Store position as float for smooth movement
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False
    def update(self):
        """Update the ship's position based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += settings.SHIP_SPEED
        if self.moving_left and self.rect.left > 0:
            self.x -= settings.SHIP_SPEED
        self.rect.x = int(self.x)
    def center_ship(self):
        """Center the ship horizontally after losing a life."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom -= 10
        self.x = float(self.rect.x)
    def blitme(self):
        """Draw the ship as a simple polygon shape."""
        left = self.rect.left
        right = self.rect.right
        top = self.rect.top
        bottom = self.rect.bottom
        midx = self.rect.centerx
        body_color = (60, 200, 255)
        cockpit_color = (240, 240, 240)
        # Main hull
        pygame.draw.polygon(self.screen, body_color, [
            (midx, top),                    # nose
            (right, bottom),
            (right - 8, bottom),
            (midx, top + 14),
            (left + 8, bottom),
            (left, bottom),
        ])
        # Cockpit
        pygame.draw.circle(self.screen, cockpit_color, (midx, top + 12), 4)