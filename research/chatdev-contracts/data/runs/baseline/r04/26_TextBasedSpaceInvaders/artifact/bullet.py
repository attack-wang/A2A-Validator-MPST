'''Projectile class for both player bullets and alien bombs.'''
import pygame
import settings
class Bullet:
    def __init__(self, x, y, speed, color, width, height):
        self.x = float(x)
        self.y = float(y)
        self.speed = float(speed)
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self._sync()
    def _sync(self):
        self.rect.centerx = int(round(self.x))
        self.rect.centery = int(round(self.y))
    def update(self, dt):
        self.y += self.speed * dt
        self._sync()
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    def is_offscreen(self):
        return self.rect.bottom < 0 or self.rect.top > settings.SCREEN_HEIGHT