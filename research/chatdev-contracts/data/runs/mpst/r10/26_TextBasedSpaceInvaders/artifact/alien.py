'''
alien.py
A single alien in the fleet. Stores its row (for scoring/color), rect,
and draws a simple pixel-alien with eyes.
'''
import pygame
# Body colors per row (top row is worth the most points)
ALIEN_ROW_COLORS = [
    (255, 60, 60),     # red
    (255, 140, 0),     # orange
    (255, 200, 0),     # yellow
    (80, 220, 80),     # green
    (80, 160, 255),    # blue
]
class Alien:
    """One invader; knows its row, point value, color, and screen position."""
    def __init__(self, settings, row, col):
        self.settings = settings
        self.row = row
        self.col = col
        self.points = settings.alien_points[row] if row < len(settings.alien_points) else 10
        self.color = ALIEN_ROW_COLORS[row % len(ALIEN_ROW_COLORS)]
        self.rect = pygame.Rect(0, 0, settings.alien_width, settings.alien_height)
        self._position(row, col)
    def _position(self, row, col):
        """Place the alien in the fleet grid."""
        x = self.settings.fleet_side_margin + col * self.settings.alien_x_spacing
        y = self.settings.fleet_top_margin + row * self.settings.alien_y_spacing
        self.rect.topleft = (x, y)
    def update(self, dx, dy):
        """Move by the fleet's step."""
        self.rect.x += dx
        self.rect.y += dy
    def draw(self, screen):
        """Draw the alien body with simple eyes."""
        pygame.draw.rect(screen, self.color, self.rect)
        # eyes
        eye_color = (10, 10, 30)
        eye_w, eye_h = 6, 6
        r = self.rect
        pygame.draw.rect(screen, eye_color,
                         (r.left + r.width // 4 - eye_w // 2, r.top + r.height // 3, eye_w, eye_h))
        pygame.draw.rect(screen, eye_color,
                         (r.left + 3 * r.width // 4 - eye_w // 2, r.top + r.height // 3, eye_w, eye_h))
        # little "mouth" line
        pygame.draw.rect(screen, eye_color,
                         (r.centerx - 6, r.top + 2 * r.height // 3, 12, 3))