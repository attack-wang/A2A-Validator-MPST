'''
entities.py
Game entities: the player's ship, the player's bullets, alien bombs and
the individual aliens. Every entity knows how to update itself, draw
itself and report its collision rectangle.
'''
import pygame
import settings
from bitmaps import ALIEN_FRAMES, PLAYER_PATTERN, render_bitmap
class Player:
    """The player's ship. Moves horizontally along the bottom of the screen."""
    def __init__(self):
        self.image = render_bitmap(PLAYER_PATTERN, settings.COLOR_PLAYER, settings.PLAYER_PIXEL)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 30)
        self.speed = settings.PLAYER_SPEED
        self.cooldown_ms = settings.PLAYER_FIRE_COOLDOWN
        self.last_shot_ms = 0
        self.invincible_until_ms = 0
        self.alive = True
    def handle_input(self, keys, now_ms):
        """Move the ship according to the currently pressed keys."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, settings.SCREEN_WIDTH)
    def can_fire(self, now_ms):
        return now_ms - self.last_shot_ms >= self.cooldown_ms
    def fire(self, now_ms):
        """Create a bullet above the ship (if the cooldown allows it)."""
        if not self.can_fire(now_ms):
            return None
        self.last_shot_ms = now_ms
        return Bullet(self.rect.centerx, self.rect.top - 2)
    def hit(self, now_ms):
        """Register a bomb hit; grants temporary invincibility."""
        self.invincible_until_ms = now_ms + settings.PLAYER_RESPAWN_INVINCIBILITY
    def is_invincible(self, now_ms):
        return now_ms < self.invincible_until_ms
    def draw(self, surface, now_ms):
        # Blink while invincible so the player can see the shield timer.
        if self.is_invincible(now_ms) and (now_ms // 100) % 2 == 0:
            return
        surface.blit(self.image, self.rect)
class Bullet:
    """A shot fired by the player. Travels upwards."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, settings.BULLET_WIDTH, settings.BULLET_HEIGHT)
        self.rect.midbottom = (x, y)
        self.speed = settings.BULLET_SPEED
    def update(self):
        self.rect.y -= self.speed
    def is_off_screen(self):
        return self.rect.bottom < 0
    def draw(self, surface):
        pygame.draw.rect(surface, settings.COLOR_BULLET, self.rect)
class Bomb:
    """A projectile dropped by the aliens. Travels downwards, slightly wiggles."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, settings.BOMB_WIDTH, settings.BOMB_HEIGHT)
        self.rect.midtop = (x, y)
        self.speed = settings.BOMB_SPEED
        self.wobble = 0
    def update(self):
        self.rect.y += self.speed
        self.wobble = (self.wobble + 1) % 20
    def is_off_screen(self):
        return self.rect.top > settings.SCREEN_HEIGHT
    def draw(self, surface):
        offset = 1 if self.wobble < 10 else -1
        pygame.draw.rect(surface, settings.COLOR_BOMB, self.rect)
        # little zig-zag tail
        pygame.draw.rect(surface, settings.COLOR_BOMB,
                         (self.rect.centerx + offset - 1, self.rect.top - 4, 2, 4))
class Alien:
    """A single alien. Belongs to a fleet which controls its movement."""
    def __init__(self, alien_type, points, x, y):
        self.type = alien_type
        self.points = points
        self.frames = ALIEN_FRAMES[alien_type]
        self.frame_index = 0
        self.images = [render_bitmap(frame, ..., settings.ALIEN_PIXEL) for frame in self.frames]
        ...