'''
alien.py
Defines a single alien and its rendering.
'''
import pygame
import settings
class Alien:
    """A single alien in the fleet."""
    def __init__(self, screen, row, col):
        self.screen = screen
        self.row = row
        self.col = col
        self.width, self.height = 40, 28
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Different colors per row for visual variety
        colors = [(255, 90, 90), (255, 170, 60), (120, 220, 120), (120, 170, 255)]
        self.color = colors[row % len(colors)]
    def set_position(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    def update(self, direction):
        """Move the alien horizontally in the given direction."""
        self.x += settings.ALIEN_SPEED_X * direction
        self.rect.x = int(self.x)
    def drop(self):
        """Move the alien down by the fleet drop speed."""
        self.y += settings.FLEET_DROP_SPEED
        self.rect.y = int(self.y)
    def check_edges(self, screen_rect):
        """Return True if the alien is at the left or right edge."""
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
    def blitme(self):
        """Draw the alien as a simple pixel-style shape."""
        r = self.rect
        body = self.color
        dark = tuple(c // 2 for c in self.color)
        eye = (20, 20, 20)
        # Body
        pygame.draw.rect(self.screen, body, (r.left + 4, r.top + 6, r.width - 8, r.height - 10))
        # Antennae
        pygame.draw.line(self.screen, body, (r.centerx - 8, r.top + 6), (r.centerx - 12, r.top), 2)
        pygame.draw.line(self.screen, body, (r.centerx + 8, r.top + 6), (r.centerx + 12, r.top), 2)
        # Eyes
        pygame.draw.rect(self.screen, eye, (r.left + 10, r.top + 12, 6, 6))
        pygame.draw.rect(self.screen, eye, (r.right - 16, r.top + 12, 6, 6))
        # Legs
        pygame.draw.line(self.screen, dark, (r.left + 8, r.bottom - 4), (r.left + 4, r.bottom), 2)
        pygame.draw.line(self.screen, dark, (r.right - 8, r.bottom - 4), (r.right - 4, r.bottom), 2)