'''
ship.py
Defines the player's ship: horizontal movement, firing with a
cooldown, and drawing itself as a simple polygon on the screen.
'''
import pygame
class Ship:
    """Player-controlled ship at the bottom of the screen."""
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        # Build a surface with the ship drawn on it once, then blit it.
        self.image = pygame.Surface((settings.SHIP_WIDTH, settings.SHIP_HEIGHT), pygame.SRCALPHA)
        self._draw_ship_image()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 10)
        self.x = float(self.rect.x)
        self.moving_left = False
        self.moving_right = False
        self.cooldown_timer = 0.0
    def _draw_ship_image(self):
        """Render the ship sprite (triangle + body) onto its surface."""
        w, h = self.image.get_size()
        body = pygame.Rect(4, h // 2, w - 8, h // 2)
        pygame.draw.rect(self.image, self.settings.COLOR_SHIP, body, border_radius=4)
        pygame.draw.polygon(
            self.image,
            self.settings.COLOR_SHIP,
            [(w // 2, 0), (w - 6, h // 2 + 2), (6, h // 2 + 2)],
        )
        # cockpit
        pygame.draw.circle(self.image, (200, 255, 200), (w // 2, h // 2 + 6), 4)
    def update(self, dt):
        """Move the ship horizontally and tick the fire cooldown."""
        if self.moving_left and not self.moving_right:
            self.x -= self.settings.SHIP_SPEED * dt
        elif self.moving_right and not self.moving_left:
            self.x += self.settings.SHIP_SPEED * dt
        self.x = max(0.0, min(self.x, self.settings.SCREEN_WIDTH - self.settings.SHIP_WIDTH))
        self.rect.x = round(self.x)
        if self.cooldown_timer > 0:
            self.cooldown_timer = max(0.0, self.cooldown_timer - dt)
    def can_fire(self):
        """True when the cooldown has elapsed."""
        return self.cooldown_timer <= 0.0
    def start_cooldown(self):
        """Begin the firing cooldown."""
        self.cooldown_timer = self.settings.SHIP_COOLDOWN
    def reset_position(self):
        """Center the ship at the bottom of the screen."""
        self.rect.midbottom = (self.settings.SCREEN_WIDTH // 2, self.settings.SCREEN_HEIGHT - 10)
        self.x = float(self.rect.x)
        self.moving_left = False
        self.moving_right = False
        self.cooldown_timer = 0.0
    def draw(self):
        self.screen.blit(self.image, self.rect)