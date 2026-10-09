'''
bullet.py: projectiles fired by the ship and dropped by aliens.
'''
import pygame
class Bullet:
    """A simple rectangular projectile moving vertically."""
    def __init__(self, settings, x, y, speed, color, width, height, direction):
        self.settings = settings
        self.speed = speed
        self.color = color
        self.direction = direction  # -1 up, +1 down
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.centerx = x
        if direction < 0:
            self.rect.bottom = y
        else:
            self.rect.top = y
        self.y = float(self.rect.y)
        self.dead = False
    def update(self, dt):
        self.y += self.direction * self.speed * dt
        self.rect.y = int(self.y)
    @property
    def off_screen(self):
        return self.rect.bottom < 0 or self.rect.top > self.settings.screen_height
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)