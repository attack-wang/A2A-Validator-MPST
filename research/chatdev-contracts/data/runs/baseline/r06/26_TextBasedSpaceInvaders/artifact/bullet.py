'''
bullet.py
Projectile classes: Bullet (fired by the player ship, travels upward)
and Bomb (dropped by aliens, travels downward). Both are lightweight
rectangle-based objects with simple vertical motion and self-culling.
'''
import pygame
import settings
class Bullet:
    """A shot fired by the player that travels up the screen."""
    def __init__(self, x, y):
        """Create a bullet whose top-center starts at (x, y)."""
        self.rect = pygame.Rect(0, 0, settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
        self.rect.midbottom = (x, y)
        self.alive = True
    def update(self, dt):
        """Move the bullet upward; deactivate when it leaves the screen."""
        self.rect.y -= round(settings.BULLET_SPEED * dt)
        if self.rect.bottom < 0:
            self.alive = False
    def draw(self, screen):
        """Render the bullet as a glowing yellow bolt."""
        pygame.draw.rect(screen, settings.YELLOW, self.rect, border_radius=2)
class Bomb:
    """A bomb dropped by an alien that travels down the screen."""
    def __init__(self, x, y):
        """Create a bomb whose top-center starts at (x, y)."""
        self.rect = pygame.Rect(0, 0, settings.BOMB_WIDTH, settings.BOMB_HEIGHT)
        self.rect.midtop = (x, y)
        self.alive = True
    def update(self, dt):
        """Move the bomb downward; deactivate when it leaves the screen."""
        self.rect.y += round(settings.BOMB_SPEED * dt)
        if self.rect.top > settings.SCREEN_HEIGHT:
            self.alive = False
    def draw(self, screen):
        """Render the bomb as a red zig-zag bolt."""
        pygame.draw.rect(screen, settings.RED, self.rect, border_radius=2)