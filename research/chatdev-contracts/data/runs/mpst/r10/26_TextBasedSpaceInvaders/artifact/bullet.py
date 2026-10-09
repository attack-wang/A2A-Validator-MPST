'''
bullet.py
Projectile used for both player shots (moving up) and alien bombs (moving down).
Handles its own movement and off-screen culling.
'''
import pygame
class Bullet:
    """A projectile fired by the player (moves up) or an alien bomb (moves down)."""
    def __init__(self, settings, x, y, going_up=True):
        self.settings = settings
        self.going_up = going_up
        if going_up:
            self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
            self.speed = settings.bullet_speed
            self.color = settings.bullet_color
            self.rect.midbottom = (x, y)  # spawn just above the ship
        else:
            self.rect = pygame.Rect(0, 0, settings.bomb_width, settings.bomb_height)
            self.speed = settings.bomb_speed
            self.color = settings.bomb_color
            self.rect.midtop = (x, y)  # spawn just below the alien
    def update(self):
        """Move the projectile. Return False once it leaves the screen."""
        if self.going_up:
            self.rect.y -= self.speed
            return self.rect.bottom > 0
        self.rect.y += self.speed
        return self.rect.top < self.settings.screen_height
    def draw(self, screen):
        """Render the projectile as a simple colored rectangle."""
        pygame.draw.rect(screen, self.color, self.rect)