'''ship.py: the player-controlled ship at the bottom of the screen.'''
import pygame
class Ship(pygame.sprite.Sprite):
    """Player ship: horizontal movement and firing."""
    def __init__(self, settings, screen):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # Pre-render the ship image
        self.image = pygame.Surface((settings.ship_width, settings.ship_height), pygame.SRCALPHA)
        self._draw_ship_image()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.screen_rect.centerx, self.screen_rect.bottom - 10)
        self.x = float(self.rect.centerx)
        self.moving_left = False
        self.moving_right = False
    def _draw_ship_image(self):
        """Pre-render the ship sprite (triangle body, cockpit, thruster base)."""
        w, h = self.settings.ship_width, self.settings.ship_height
        color = self.settings.ship_color
        # body
        pygame.draw.polygon(self.image, color, [
            (w // 2, 0), (w, h), (0, h)
        ])
        # cockpit
        pygame.draw.circle(self.image, (255, 255, 255), (w // 2, h - 12), 4)
        # thrusters/base
        pygame.draw.rect(self.image, (200, 200, 220), (w // 2 - 10, h - 6, 20, 6))
    def update(self):
        """Apply horizontal movement, clamped to the screen edges."""
        if self.moving_left and not self.moving_right:
            self.x -= self.settings.ship_speed
        elif self.moving_right and not self.moving_left:
            self.x += self.settings.ship_speed
        half = self.rect.width / 2
        self.x = min(max(self.x, half), self.screen_rect.width - half)
        self.rect.centerx = int(self.x)
    def blit(self):
        """Draw the ship onto the screen."""
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        """Re-center the ship (after losing a life or on restart)."""
        self.rect.midbottom = (self.screen_rect.centerx, self.screen_rect.bottom - 10)
        self.x = float(self.rect.centerx)