import pygame
from settings import Settings
class Bullet:
    """Player shot that travels upward and is removed once off-screen."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, Settings.BULLET_WIDTH, Settings.BULLET_HEIGHT)
        self.rect.midbottom = (x, y)
        self.speed = Settings.BULLET_SPEED
    def update(self, dt):
        self.rect.y -= round(self.speed * dt)
    @property
    def off_screen(self):
        return self.rect.bottom < 0
    def draw(self, screen):
        pygame.draw.rect(screen, Settings.BULLET_COLOR, self.rect)
class Bomb:
    """Alien bomb that travels downward and is removed once off-screen."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, Settings.BOMB_WIDTH, Settings.BOMB_HEIGHT)
        self.rect.midtop = (x, y)
        self.speed = Settings.BOMB_SPEED
    def update(self, dt):
        self.rect.y += round(self.speed * dt)
    @property
    def off_screen(self):
        return self.rect.top > Settings.SCREEN_HEIGHT
    def draw(self, screen):
        pygame.draw.rect(screen, Settings.BOMB_COLOR, self.rect)