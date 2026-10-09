'''
fleet.py
The Fleet class manages the grid of aliens: creating them, moving the
whole formation sideways, dropping it down when an edge is reached,
speeding the aliens up as their numbers shrink, and dropping bombs.
'''
import random
import pygame
import settings
from sprites import Alien, Bomb
class Fleet:
    """Manages the formation of aliens as a single moving unit."""
    def __init__(self, bomb_group):
        self.aliens = pygame.sprite.Group()
        self.bombs = bomb_group
        self.total = settings.ALIEN_ROWS * settings.ALIEN_COLS
        self.drop_multiplier = 1.0  # grows on every edge drop
        self.direction = 1          # 1 = right, -1 = left
        self.speed = settings.ALIEN_SPEED_X
        self._build()
    def _build(self):
        """Create the rectangular grid of aliens and reset fleet state."""
        self.aliens.empty()
        fleet_w = settings.ALIEN_COLS * settings.ALIEN_WIDTH + \
                  (settings.ALIEN_COLS - 1) * settings.ALIEN_H_SPACING
        start_x = (settings.WIDTH - fleet_w) // 2
        start_y = settings.FLEET_TOP_MARGIN
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLS):
                x = start_x + col * (settings.ALIEN_WIDTH + settings.ALIEN_H_SPACING)
                y = start_y + row * (settings.ALIEN_HEIGHT + settings.ALIEN_V_SPACING)
                self.aliens.add(Alien(row, col, x, y))
        self.direction = 1
        self.speed = settings.ALIEN_SPEED_X
        self.drop_multiplier = 1.0
    def rebuild(self):
        """Public alias to build a fresh formation."""
        self._build()
    def update(self):
        """Move the fleet; drop down and reverse when an edge is hit."""
        if not self.aliens:
            return
        # Determine current horizontal extremes
        left = min(a.rect.left for a in self.aliens)
        right = max(a.rect.right for a in self.aliens)
        hit_edge = (self.direction > 0 and right + self.speed >= settings.WIDTH) or \
                   (self.direction < 0 and left - self.speed <= 0)
        if hit_edge:
            self.direction *= -1
            self.drop_multiplier *= settings.DROP_SPEEDUP
            for alien in self.aliens:
                alien.rect.y += settings.ALIEN_DROP_SPEED
        # Fleet speeds up as it shrinks and after each drop; capped for playability
        alive_ratio = len(self.aliens) / self.total
        self.speed = min(
            settings.ALIEN_SPEED_X * self.drop_multiplier *
            (1 + (1 - alive_ratio) * settings.SHRINK_SPEEDUP),
            settings.MAX_FLEET_SPEED,
        )
        dx = int(round(self.speed)) * self.direction
        for alien in self.aliens:
            alien.rect.x += dx
        # Aliens occasionally drop bombs (bottom-most alien of each column)
        self._drop_bombs()
    def _drop_bombs(self):
        """Randomly drop bombs from the bottom-most alien of each column."""
        if len(self.bombs) >= settings.MAX_BOMBS:
            return
        bottom = {}
        for alien in self.aliens:
            col_key = alien.rect.centerx
            if col_key not in bottom or alien.rect.bottom > bottom[col_key].rect.bottom:
                bottom[col_key] = alien
        for alien in bottom.values():
            if random.random() < settings.BOMB_CHANCE:
                self.bombs.add(Bomb(alien.rect.centerx, alien.rect.bottom))
    def lowest_bottom(self):
        """Y coordinate of the lowest alien (0 if the fleet is empty)."""
        if not self.aliens:
            return 0
        return max(a.rect.bottom for a in self.aliens)
    def has_reached(self, y):
        """True when any alien has descended to or below the line y."""
        return self.lowest_bottom() >= y