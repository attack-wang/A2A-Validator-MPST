'''
bullet.py
Defines projectiles fired by the player and bombs dropped by aliens.
'''
import pygame
import settings
class Bullet:
    """A projectile: direction 1 = player shot (up), -1 = alien bomb (down)."""
    def __init__(self, screen, centerx, top, direction):
        self.screen = screen
        self.direction = direction
        if direction == 1:
            self.width = settings.BULLET_WIDTH
            self.height = settings.BULLET_HEIGHT
            self.color = settings.BULLET_COLOR
        else:
            self.width = settings.BOMB_WIDTH
            self.height = settings.BOMB_HEIGHT
            self.color = settings.BOMB_COLOR
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = centerx
        self.rect.top = top
        self.y = float(self.rect.y)
    def update(self):
        """Move the bullet up (player) or down (alien)."""
        speed = settings.BULLET_SPEED if self.direction == 1 else settings.BOMB_SPEED
        self.y += speed * self.direction
        self.rect.y = int(self.y)
    def is_off_screen(self):
        """Return True if the bullet has left the screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.bottom < 0 or self.rect.top > screen_rect.bottom
    def blitme(self):
        pygame.draw.rect(self.screen, self.color, self.rect)