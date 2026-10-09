'''
alien.py
Alien sprite and AlienFleet manager. A single Alien knows how to
move with the fleet, drop down a row and draw itself. AlienFleet
builds the grid of rows/columns, moves the whole formation, reverses
direction at screen edges, lets aliens drop bombs and reports when
the invasion has reached the bottom or has been wiped out.
'''
import random
import pygame
from bullet import EnemyBullet
class Alien:
    """One invader in the descending fleet."""
    def __init__(self, settings, screen, row, col):
        self.settings = settings
        self.screen = screen
        self.row = row
        self.col = col
        self.points = settings.POINTS_PER_ROW[min(row, len(settings.POINTS_PER_ROW) - 1)]
        self.image = pygame.Surface((settings.ALIEN_WIDTH, settings.ALIEN_HEIGHT), pygame.SRCALPHA)
        self._draw_alien_image(row)
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    def _draw_alien_image(self, row):
        """Draw a blocky invader face; color varies by row."""
        color = self.settings.COLOR_ALIEN_ROW_A if row % 2 == 0 else self.settings.COLOR_ALIEN_ROW_B
        w, h = self.image.get_size()
        # body
        pygame.draw.rect(self.image, color, (2, 6, w - 4, h - 10), border_radius=6)
        # antennae
        pygame.draw.line(self.image, color, (6, 8), (2, 2), 2)
        pygame.draw.line(self.image, color, (w - 6, 8), (w - 2, 2), 2)
        # eyes
        pygame.draw.rect(self.image, (20, 20, 20), (8, 12, 6, 6))
        pygame.draw.rect(self.image, (20, 20, 20), (w - 14, 12, 6, 6))
        # mouth
        pygame.draw.rect(self.image, (20, 20, 20), (w // 2 - 6, h - 12, 12, 3))
    def set_position(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
    def draw(self):
        self.screen.blit(self.image, self.rect)
class AlienFleet:
    """Grid of aliens that marches sideways and descends."""
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.aliens = []
        self.direction = 1          # 1 = right, -1 = left
        self.speed = settings.FLEET_HORIZONTAL_SPEED
        self.initial_count = 0
        self._build_fleet()
    def _build_fleet(self):
        """Create rows x columns aliens, centered near the top."""
        self.aliens = []
        margin_x = 60
        top_y = 70
        spacing_x = self.settings.ALIEN_WIDTH + 14
        spacing_y = self.settings.ALIEN_HEIGHT + 14
        fleet_width = self.settings.ALIEN_COLUMNS * spacing_x
        start_x = (self.settings.SCREEN_WIDTH - fleet_width) // 2 + margin_x // 2
        for row in range(self.settings.ALIENT_ROWS):  # careful typo
            for col in range(self.settings.ALIENT_COLUMNS):
                alien = Alien(self.settings, self.screen, row, col)
                x = start_x + col * spacing_x
                y = top_y + row * spacing_y
                alien.set_position(x, y)
                self.aliens.append(alien)