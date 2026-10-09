'''
player.py
The player's ship: horizontal movement, firing cooldown, invulnerability
after being hit, and a vector-drawn ship sprite.
'''
import pygame
class Player:
    """Player-controlled ship at the bottom of the screen."""
    def __init__(self, settings):
        self.settings = settings
        self.rect = pygame.Rect(0, 0, settings.player_width, settings.player_height)
        self.last_shot = 0            # ms timestamp of the last shot fired
        self.visible = True           # hidden briefly after being hit
        self.invulnerable_until = 0   # ms timestamp until which hits are ignored
        self.reset_position()
    def reset_position(self):
        """Center the ship at the bottom of the screen."""
        self.rect.midbottom = (self.settings.screen_width // 2,
                               self.settings.screen_height - self.settings.player_bottom_margin)
    def update(self, keys):
        """Move the ship horizontally based on held keys, clamped to screen."""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.settings.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.settings.player_speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
    def can_fire(self, now):
        """True if the fire cooldown has elapsed."""
        return now - self.last_shot >= self.settings.player_fire_cooldown
    def is_invulnerable(self, now):
        """True while the ship is blinking and immune after a hit."""
        return now < self.invulnerable_until
    def draw(self, screen):
        """Draw the ship as a polygon; blink while invulnerable."""
        if not self.visible:
            return
        # Blink at ~8 Hz while invulnerable
        if pygame.time.get_ticks() < self.invulnerable_until:
            if (pygame.time.get_ticks() // 125) % 2 == 0:
                return
        r = self.rect
        color = (0, 200, 255)
        points = [
            (r.centerx, r.top),                       # nose
            (r.right, r.bottom),                      # bottom right
            (r.right - r.width // 4, r.bottom - r.height // 3),
            (r.left + r.width // 4, r.bottom - r.height // 3),
            (r.left, r.bottom),                       # bottom left
        ]
        pygame.draw.polygon(screen, color, points)
        # cockpit
        pygame.draw.rect(screen, (255, 255, 255),
                         (r.centerx - 3, r.top + r.height // 3, 6, 6))