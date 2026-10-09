'''
fleet.py
The AlienFleet class manages the grid of aliens: it builds the formation,
moves it as a single unit (reversing and descending at the screen edges),
speeds up as aliens are destroyed, animates the sprites and drops bombs.
'''
import random
import pygame
import settings
from entities import Alien, Bomb
class AlienFleet:
    def __init__(self):
        self.aliens = []
        self.direction = 1
        self.speed = settings.FLEET_BASE_SPEED
        self.animation_timer_ms = 0
        self.bomb_timer_ms = self._next_bomb_delay()
        self._build()
    def _build(self):
        """Create the rectangular formation of aliens."""
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLS):
                x = settings.FLEET_SIDE_MARGIN + col * settings.ALIEN_H_SPACING
                y = settings.FLEET_TOP_MARGIN + row * settings.ALIEN_V_SPACING
                alien_type = settings.ALIEN_ROW_TYPES[row]
                color = settings.ALIEN_ROW_COLORS[row]
                points = settings.ALIEN_POINTS[row]
                self.aliens.append(Alien(alien_type, color, points, x, y))
    def _next_bomb_delay(self):
        return random.randint(settings.BOMB_TIMER_MIN, settings.BOMB_TIMER_MAX)
    @property
    def alive_aliens(self):
        return [a for a in self.aliens if a.alive]
    def alive_count(self):
        return sum(1 for a in self.aliens if a.alive)
    def update(self, dt_ms, now_ms):
        """Move the fleet, animate it and maybe drop a bomb.
        Returns a list of new Bomb objects created this frame.
        """
        bombs = []
        alive = self.alive_aliens
        if not alive:
            return bombs
        # --- horizontal movement with edge detection ---
        fleet_left = min(a.rect.left for a in alive)
        fleet_right = max(a.rect.right for a in alive)
        dx = self.speed * self.direction
        if fleet_left + dx < 0 or fleet_right + dx > settings.SCREEN_WIDTH:
            self.direction *= -1
            dx = 0
            for alien in alive:
                alien.update_position(0, settings.FLEET_STEP_DOWN)
        else:
            for alien in alive:
                alien.update_position(dx, 0)
        # --- sprite animation ---
        self.animation_timer_ms += dt_ms
        if self.animation_timer_ms >= settings.FLEET_ANIMATION_INTERVAL:
            self.animation_timer_ms = 0
            for alien in alive:
                alien.animate()
        # --- bomb dropping ---
        self.bomb_timer_ms -= dt_ms
        if self.bomb_timer_ms <= 0:
            self.bomb_timer_ms = self._next_bomb_delay()
            shooter = self._pick_bomber(alive)
            if shooter is not None:
                bombs.append(Bomb(shooter.rect.centerx, shooter.rect.bottom))
        return bombs
    def _pick_bomber(self, alive):
        """Choose a random alien that is the lowest one in its column."""
        bottom_most = {}
        for alien in alive:
            col_key = alien.rect.centerx // settings.ALIEN_H_SPACING
            if col_key not in bottom_most or alien.rect.bottom > bottom_most[col_key].rect.bottom:
                bottom_most[col_key] = alien
        return random.choice(list(bottom_most.values())) if bottom_most else None
    def has_reached_bottom(self):
        return any(a.rect.bottom >= settings.INVASION_LINE_Y for a in self.alive_aliens)
    def draw(self, surface):
        for alien in self.aliens:
            if alien.alive:
                alien.draw(surface)