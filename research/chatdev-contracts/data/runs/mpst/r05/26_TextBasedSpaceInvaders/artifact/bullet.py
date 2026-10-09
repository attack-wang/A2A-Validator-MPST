'''bullet.py: projectiles fired by the player and bombs dropped by aliens.'''
import pygame
class Bullet(pygame.sprite.Sprite):
    """Base projectile: a small rectangle moving straight up or down."""
    def __init__(self, x, y, direction, color, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction  # -1 = up (player shot), +1 = down (bomb)
        self.speed = speed
    def update(self):
        """Move the projectile one step each frame."""
        self.rect.y += int(self.direction * self.speed)
    def is_offscreen(self, screen_height):
        """Return True once the projectile has left the play area."""
        return self.rect.bottom < 0 or self.rect.top > screen_height
class PlayerBullet(Bullet):
    """Shot fired by the player ship (travels upward)."""
    def __init__(self, settings, x, y):
        super().__init__(x, y, -1, settings.bullet_color,
                         settings.bullet_width, settings.bullet_height,
                         settings.bullet_speed)
class Bomb(Bullet):
    """Bomb dropped by an alien (travels downward)."""
    def __init__(self, settings, x, y):
        super().__init__(x, y, 1, settings.bomb_color,
                         settings.bomb_width, settings.bomb_height,
                         settings.bomb_speed)