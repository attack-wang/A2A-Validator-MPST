'''
bullet.py
Projectile classes: a base Bullet moving vertically with a signed
speed, plus PlayerBullet (upward) and EnemyBullet (downward). Both
handle their own movement, lifetime bounds and drawing.
'''
import pygame
class Bullet:
    """Base projectile moving vertically; subclasses set direction."""
    def __init__(self, settings, screen, x, y):
        self.settings = settings
        self.screen = screen
        self.image = pygame.Surface((settings.BULLET_WIDTH, settings.BULLET_HEIGHT))
        self.rect = self.image.get_rect(centerx=x, centery=y)
        self.y = float(self.rect.y)
        self.speed = 0.0
    def update(self, dt):
        """Move the bullet vertically by its signed speed."""
        self.y += self.speed * dt
        self.rect.y = round(self.y)
    def off_screen(self):
        """True when the bullet has left the play area."""
        return self.rect.bottom < 0 or self.rect.top > self.settings.SCREEN_HEIGHT
    def draw(self):
        self.screen.blit(self.image, self.rect)
class PlayerBullet(Bullet):
    """A shot fired by the player's ship, moving upward."""
    def __init__(self, settings, screen, x, y):
        super().__init__(settings, screen, x, y)
        self.speed = -settings.BULLET_SPEED
        self.image.fill(settings.COLOR_BULLET)
class EnemyBullet(Bullet):
    """A shot fired by an alien, moving downward."""
    def __init__(self, settings, screen, x, y):
        super().__init__(settings, screen, x, y)
        self.speed = settings.ENEMY_BULLET_SPEED
        self.image.fill(settings.COLOR_ENEMY_BULLET)