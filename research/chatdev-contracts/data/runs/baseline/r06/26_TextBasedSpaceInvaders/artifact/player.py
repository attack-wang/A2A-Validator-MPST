'''
player.py
Player ship: horizontal movement with arrow keys / A-D, space-bar
shooting with a cooldown, invulnerability blinking after being hit,
and a polygon-based ship sprite.
'''
import pygame
import settings
from bullet import Bullet
class Player:
    """The player's ship at the bottom of the playfield."""
    def __init__(self):
        self.rect = pygame.Rect(0, 0, settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
        self.rect.midbottom = (settings.SCREEN_WIDTH // 2,
                               settings.SCREEN_HEIGHT - 30)
        self.cooldown = 0.0
        self.invulnerable = 0.0
    def update(self, dt):
        """Read input, move the ship, and tick down timers."""
        keys = pygame.key.get_pressed()
        move = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move += 1
        self.rect.x += round(move * settings.PLAYER_SPEED * dt)
        self.rect.clamp_ip(pygame.Rect(0, 0, settings.SCREEN_WIDTH,
                                       settings.SCREEN_HEIGHT))
        if self.cooldown > 0.0:
            self.cooldown -= dt
        if self.invulnerable > 0.0:
            self.invulnerable -= dt
    def can_shoot(self):
        """True when the cooldown has elapsed."""
        return self.cooldown <= 0.0
    def shoot(self):
        """Fire a bullet from the nose of the ship and start the cooldown."""
        self.cooldown = settings.PLAYER_COOLDOWN
        return Bullet(self.rect.centerx, self.rect.top)
    def hit(self):
        """Register a bomb hit: start invulnerability and return True."""
        self.invulnerable = settings.PLAYER_INVULNERABLE_TIME
        return True
    def is_invulnerable(self):
        """True while the ship cannot be damaged."""
        return self.invulnerable > 0.0
    def draw(self, screen):
        """Draw the ship; blink while invulnerable."""
        if self.is_invulnerable() and int(self.invulnerable * 10) % 2 == 0:
            return  # blink effect
        r = self.rect
        body = [
            (r.centerx, r.top),                       # nose
            (r.centerx + r.width // 4, r.centery),    # right shoulder
            (r.right, r.bottom),                      # right base
            (r.left, r.bottom),                       # left base
            (r.centerx - r.width // 4, r.centery),    # left shoulder
        ]
        pygame.draw.polygon(screen, settings.GREEN, body)
        # cockpit light
        pygame.draw.circle(screen, settings.WHITE,
                           (r.centerx, r.centery + 4), 3)