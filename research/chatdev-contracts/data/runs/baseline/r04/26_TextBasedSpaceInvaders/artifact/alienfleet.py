'''
Grid of aliens that marches side to side, descends at edges, and drops bombs.
'''
import random
import pygame
import settings
from alien import Alien
from bullet import Bullet
class AlienFleet:
    def __init__(self):
        self.aliens = []
        self.direction = 1
        self.speed = settings.ALIEN_HORIZONTAL_SPEED
        self.fire_timer = 0.0
        self._build()
    def _build(self):
        self.aliens = []
        margin_x = 60
        top_y = 70
        gap_x = 18
        gap_y = 16
        for row in range(settings.ALIEN_ROWS):
            for col in range(settings.ALIEN_COLS):
                x = margin_x + col * (settings.ALIEN_WIDTH + gap_x)
                y = top_y + row * (settings.ALIEN_HEIGHT + gap_y)
                self.aliens.append(Alien(col, row, x, y))
    def update(self, dt):
        dx = self.direction * self.speed * dt
        dy = 0.0
        if self.aliens:
            leftmost = min(a.rect.left for a in self.aliens)
            rightmost = max(a.rect.right for a in self.aliens)
            if (self.direction > 0 and rightmost + dx > settings.SCREEN_WIDTH - 12) or \
               (self.direction < 0 and leftmost + dx < 12):
                self.direction *= -1
                self.speed *= settings.ALIEN_SPEEDUP
                dy = settings.ALIEN_DESCENT_STEP
        for alien in self.aliens:
            alien.update(dx, dy)
            alien.animate(dt)
        return self._maybe_fire(dt)
    def _maybe_fire(self, dt):
        '''With some probability, a random bottom-most alien drops a bomb.'''
        bombs = []
        if self.aliens and random.random() < settings.ALIEN_FIRE_CHANCE * dt:
            shooters = self._bottom_aliens()
            if shooters:
                shooter = random.choice(shooters)
                bombs.append(Bullet(shooter.rect.centerx, shooter.rect.bottom,
                                    settings.BOMB_SPEED, settings.COLOR_ALIEN_BOMB,
                                    settings.BOMB_WIDTH, settings.BOMB_HEIGHT))
        return bombs
    def _bottom_aliens(self):
        '''Return the lowest alien in each column (only they can shoot).'''
        bottom = {}
        for alien in self.aliens:
            col_key = alien.col
            if col_key not in bottom or alien.rect.top > bottom[col_key].rect.top:
                bottom[col_key] = alien
        return list(bottom.values())
    def all_destroyed(self):
        '''True when no aliens remain (victory condition).'''
        return len(self.aliens) == 0
    def reached_bottom(self):
        '''True when any alien has descended to the game-over line.'''
        if not self.aliens:
            return False
        lowest = max(a.rect.bottom for a in self.aliens)
        return lowest >= settings.ALIEN_BOTTOM_LIMIT