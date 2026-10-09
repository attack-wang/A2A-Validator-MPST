'''
entities.py
Game entities: the player's ship, the alien invaders, bullets and the
small explosion effect shown when something is destroyed.
'''
import random
import pygame
import settings
class Player:
    """The ship controlled by the player at the bottom of the screen."""
    def __init__(self):
        self.width = settings.PLAYER_WIDTH
        self.height = settings.PLAYER_HEIGHT
        self.x = (settings.SCREEN_WIDTH - self.width) / 2
        self.y = settings.SCREEN_HEIGHT - self.height - settings.PLAYER_BOTTOM_OFFSET
        self.speed = settings.PLAYER_SPEED
        self.lives = settings.PLAYER_START_LIVES
        self.cooldown_ms = 0
        self.invulnerable_ms = 0
    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
    def update(self, keys, dt_ms):
        """Move horizontally, and tick down cooldown / invulnerability timers."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        self.x = max(0.0, min(self.x, settings.SCREEN_WIDTH - self.width))
        self.cooldown_ms = max(0, self.cooldown_ms - dt_ms)
        self.invulnerable_ms = max(0, self.invulnerable_ms - dt_ms)
    def can_fire(self):
        return self.cooldown_ms <= 0
    def fire(self):
        """Spawn a bullet from the ship's cannon and start the reload timer."""
        self.cooldown_ms = settings.PLAYER_COOLDOWN_MS
        x = self.x + self.width / 2 - settings.BULLET_WIDTH / 2
        return Bullet(x, self.y - settings.BULLET_HEIGHT, -settings.PLAYER_BULLET_SPEED, settings.CYAN)
    def hit(self):
        """Register a hit. Returns True if the player is out of lives."""
        self.lives -= 1
        self.invulnerable_ms = settings.PLAYER_RESPAWN_INVULN_MS
        return self.lives <= 0
    def is_invulnerable(self):
        return self.invulnerable_ms > 0
    def draw(self, surface):
        # Blink while invulnerable so the player can see the protected state.
        if self.is_invulnerable() and (self.invulnerable_ms // 100) % 2 == 0:
            return
        body = self.rect
        pygame.draw.rect(surface, settings.CYAN, body)
        pygame.draw.rect(surface, settings.CYAN,
                         (body.centerx - 3, body.top - 8, 6, 8))
        pygame.draw.rect(surface, settings.WHITE,
                         (body.centerx - 8, body.bottom - 6, 16, 4))