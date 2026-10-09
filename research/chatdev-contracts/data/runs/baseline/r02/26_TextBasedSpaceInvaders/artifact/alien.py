'''alien.py — a single alien belonging to the descending fleet.'''
import pygame
from assets import image_from_pattern, ALIEN_PATTERN
class Alien:
    '''Represents one alien in the fleet.'''
    def __init__(self, game, row, col):
        '''Create an alien and place it in the fleet grid.'''
        self.screen = game.screen
        self.settings = game.settings
        self.row = row
        self.col = col
        self.image = image_from_pattern(ALIEN_PATTERN, (0, 255, 90), scale=3)
        self.rect = self.image.get_rect()
        # Position the alien inside its grid cell
        self.rect.x, self.rect.y = self._grid_position()
        self.x = float(self.rect.x)
    def _grid_position(self):
        '''Compute the pixel position of this alien from its row/column.'''
        margin = 60
        cell_w = (self.settings.screen_width - 2 * margin) / self.settings.alien_cols
        x = margin + cell_w * self.col + (cell_w - self.rect.width) / 2
        y = 90 + self.row * 55
        return x, y
    def check_edges(self):
        '''Return True if the alien is at (or beyond) a screen edge.'''
        screen_rect = self.screen.get_rect()
        return self.rect.left <= 0 or self.rect.right >= screen_rect.right
    def update(self):
        '''Move the alien horizontally by the current fleet speed/direction.'''
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
    def drop(self):
        '''Move the alien down by the fleet drop speed.'''
        self.rect.y += self.settings.fleet_drop_speed
    def blitme(self):
        '''Draw the alien on the screen.'''
        self.screen.blit(self.image, self.rect)