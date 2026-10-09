'''fleet.py: the alien fleet formation, movement and bombing logic.'''
import random
import pygame
from alien import Alien
from bullet import Bullet
class Fleet:
    def __init__(self, game, level):
        self.game = game
        self.settings = game.settings
        self.level = level
        self.aliens = []
        self.bombs = []
        self.direction = 1
        self.speed = self.settings.fleet_speed + (level - 1) * self.settings.fleet_speed_increment
        self.bomb_interval = max(self.settings.bomb_interval_min, self.settings.bomb_interval - (level - 1) * 0.1)
        self.bomb_timer = self.bomb_interval
        self._create_fleet()
    def _create_fleet(self):
        s = self.settings
        total_width = s.alien_cols * s.alien_width + (s.alien_cols - 1) * s.alien_h_spacing
        start_x = (s.screen_width - total_width) // 2
        start_y = s.fleet_top_margin
        for row in range(s.alien_rows):
            for col in range(s.alien_cols):
                x = start_x + col * (s.alien_width + s.alien_h_spacing)
                y = start_y + row * (s.alien_height + s.alien_v_spacing)
                self.aliens.append(Alien(s, row, col, x, y))
    def update(self, dt):
        dx = self.direction * self.speed * dt
        dy = 0
        if self._hit_edge():
            self.direction *= -1
            dx = self.direction * self.speed * dt
            dy = self.settings.fleet_drop_distance
        for alien in self.aliens:
            alien.update(dx, dy)
        self._update_bombs(dt)
        self._update_bomb_timer(dt)
    def _hit_edge(self):
        s = self.settings
        for alien in self.aliens:
            if self.direction > 0 and alien.rect.right >= s.screen_width - s.fleet_right_margin:
                return True
            if self.direction < 0 and alien.rect.left <= s.fleet_left_margin:
                return True
        return False
    def _update_bomb_timer(self, dt):
        self.bomb_timer -= dt
        if self.bomb_timer <= 0 and self.aliens:
            self._drop_bomb()
            self.bomb_timer = self.bomb_interval
    def _drop_bomb(self):
        shooter = random.choice(self.aliens)
        bomb = Bullet(self.settings, shooter.rect.centerx, shooter.rect.bottom,
                      self.settings.bomb_speed, self.settings.bomb_color,
                      self.settings.bomb_width, self.settings.bomb_height, 1)
        self.bombs.append(bomb)
    def _update_bombs(self, dt):
        for bomb in self.bombs:
            bomb.update(dt)
        self.bombs = [b for b in self.bombs if not b.off_screen]
    def reached_bottom(self):
        s = self.settings
        for alien in self.aliens:
            if alien.rect.bottom >= s.screen_height:
                return True
        return False
    def draw(self, screen):
        for alien in self.aliens:
            alien.draw(screen)
        for bomb in self.bombs:
            bomb.draw(screen)