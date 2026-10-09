'''
alien.py
Alien and AlienFleet classes: builds the alien grid, marches it side to
side with edge detection and downward drops, speeds up as it shrinks,
and drops bombs from the bottom-most alien of a random occupied column.
'''
import random
import pygame
import settings
from bullet import Bomb
class Alien:
    """A single alien invader belonging to a fleet row/column."""
    def __init__(self, row, col, x, y):
        self.row = row
        self.col = col
        self.rect = pygame.Rect(x, y, settings.ALIEN_WIDTH, settings.ALIEN_HEIGHT)
        self.alive = True
        if row < len(settings.ALIEN_POINTS_PER_ROW):
            self.points = settings.ALIEN_POINTS_PER_ROW[row]
        else:
            self.points = settings.DEFAULT_ALIEN_POINTS
    def draw(self, screen):
        """Draw the alien as a rounded body with eyes and antennae."""
        color = settings.ALIEN_COLORS[self.row % len(settings.ALIEN_COLORS)]
        r = self.rect
        body = [
            (r.left + 6, r.top),
            (r.right - 6, r.top),
            (r.right, r.top + 8),
            (r.right, r.bottom - 4),
            (r.right - 6, r.bottom),
            (r.left + 6, r.bottom),
            (r.left, r.bottom - 4),
            (r.left, r.top + 8),
        ]
        pygame.draw.polygon(screen, color, body)
        eye_y = r.top + r.height // 2
        pygame.draw.circle(screen, settings.BLACK, (r.centerx - 7, eye_y), 3)
        pygame.draw.circle(screen, settings.BLACK, (r.centerx + 7, eye_y), 3)
        pygame.draw.line(screen, color,
                         (r.centerx - 8, r.top), (r.centerx - 12, r.top - 5), 2)
        pygame.draw.line(screen, color,
                         (r.centerx + 8, r.top), (r.centerx + 12, r.top - 5), 2)
class AlienFleet:
    """The marching grid of aliens with bomb-dropping behaviour."""
    def __init__(self):
        self.aliens = []
        self.direction = 1
        self.speed = settings.ALIEN_HORIZONTAL_SPEED
        self.bomb_timer = random.uniform(settings.BOMB_INTERVAL_MIN,
                                         settings.BOMB_INTERVAL_MAX)
        self._create_fleet()
    def _create_fleet(self):
        """Spawn the full grid of aliens centred horizontally."""
        total_width = (settings.ALIEN_COLS - 1) * settings.ALIEN_X_SPACING
        offset_x = (settings.SCREEN_WIDTH - total_width) // 2
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLS):
                x = offset_x + col * settings.ALIEN_X_SPACING - settings.ALIEN_WIDTH // 2
                y = settings.FLEET_TOP_MARGIN + row * settings.ALIEN_Y_SPACING
                self.aliens.append(Alien(row, col, x, y))
    @property
    def alive_aliens(self):
        """List of aliens that are still alive."""
        return [a for a in self.aliens if a.alive]
    def update(self, dt):
        """March the fleet, drop on edge contact, drop bombs.
        Returns a newly dropped Bomb, or None if no bomb was dropped.
        """
        alive = self.alive_aliens
        if not alive:
            return None
        # speed scales up as the fleet shrinks
        alive_ratio = len(alive) / len(self.aliens)
        speed = settings.ALIEN_HORIZONTAL_SPEED * (
            1.0 + (1.0 - alive_ratio) * settings.FLEET_SPEEDUP_FACTOR)
        dx = speed * dt * self.direction
        leftmost = min(a.rect.left for a in alive)
        rightmost = max(a.rect.right for a in alive)
        if (self.direction > 0
                and rightmost + dx >= settings.SCREEN_WIDTH - settings.FLEET_SIDE_MARGIN):
            self._drop_and_reverse()
        elif (self.direction < 0
                and leftmost + dx <= settings.FLEET_SIDE_MARGIN):
            self._drop_and_reverse()
        else:
            for a in alive:
                a.rect.x += round(dx)
        # bomb timer
        new_bomb = None
        self.bomb_timer -= dt
        if self.bomb_timer <= 0:
            new_bomb = self.drop_bomb()
            self.bomb_timer = random.uniform(settings.BOMB_INTERVAL_MIN,
                                             settings.BOMB_INTERVAL_MAX)
        return new_bomb
    def _drop_and_reverse(self):
        """Step the whole fleet down and reverse its marching direction."""
        self.direction *= -1
        for a in self.alive_aliens:
            a.rect.y += settings.ALIEN_DROP_DISTANCE
    def drop_bomb(self):
        """Drop a bomb from the bottom-most alien of a random occupied column."""
        alive = self.alive_aliens
        if not alive:
            return None
        bottom_per_column = {}
        for a in alive:
            current = bottom_per_column.get(a.col)
            if current is None or a.rect.centery > current.rect.centery:
                bottom_per_column[a.col] = a
        shooter = random.choice(list(bottom_per_column.values()))
        return Bomb(shooter.rect.centerx, shooter.rect.bottom)
    def draw(self, screen):
        """Draw every alive alien."""
        for a in self.alive_aliens:
            a.draw(screen)