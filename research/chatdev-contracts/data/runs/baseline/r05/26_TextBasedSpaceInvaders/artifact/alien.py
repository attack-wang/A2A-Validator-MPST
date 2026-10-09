import random
import pygame
from settings import Settings
from bullet import Bomb
from utils import bitmap_to_surface
ALIEN_BITMAP_A = [...]
ALIEN_BITMAP_B = [...]
class Alien:
    def __init__(self, row, col, x, y, points, color):
        self.frames = [
            bitmap_to_surface(ALIEN_BITMAP_A, color, Settings.ALIEN_SCALE),
            bitmap_to_surface(ALIEN_BITMAP_B, color, Settings.ALIEN_SCALE),
        ]
        self.frame = 0
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.points = points
        self.row = row
        self.col = col
        self.x = float(x)
    def move(self, dx, dy):
        self.x += dx
        self.rect.x = round(self.x)
        self.rect.y += dy
    def toggle_frame(self):
        self.frame = 1 - self.frame
        self.image = self.frames[self.frame]
    def draw(self, screen):
        screen.blit(self.image, self.rect)
class AlienFleet:
    """Grid of aliens that marches side-to-side, drops down at edges, and drops bombs."""
    def __init__(self, wave=1):
        self.aliens = []
        self.direction = 1
        self.speed = Settings.ALIEN_HORIZONTAL_SPEED * (Settings.ALIEN_SPEEDUP_PER_WAVE ** (wave - 1))
        self.anim_timer = 0.0
        self.anim_frame = 0
        self._create_fleet()
    def _create_fleet(self):
        spacing_x = 12
        spacing_y = 12
        fleet_width = Settings.ALIEN_COLUMNS * Settings.ALIEN_WIDTH + (Settings.ALIEN_COLUMNS - 1) * spacing_x
        margin_x = (Settings.SCREEN_WIDTH - fleet_width) // 2
        start_y = 70
        rows = Settings.ALIEN_ROWS
        for row in range(rows):
            color = Settings.ALIEN_COLORS[row % len(Settings.ALIEN_COLORS)]
            points = Settings.ALIEN_BASE_POINTS + (rows - 1 - row) * Settings.ALIEN_ROW_BONUS
            for col in range(Settings.ALIEN_COLUMNS):
                x = margin_x + col * (Settings.ALIEN_WIDTH + spacing_x)
                y = start_y + row * (Settings.ALIEN_HEIGHT + spacing_y)
                self.aliens.append(Alien(row, col, x, y, points, color))
    def update(self, dt, bomb_count):
        """Move the fleet, animate it, and maybe drop a bomb. Returns a Bomb or None."""
        if not self.aliens:
            return None
        dx = self.direction * self.speed * dt
        min_left = min(a.rect.left for a in self.aliens)
        max_right = max(a.rect.right for a in self.aliens)
        if (self.direction > 0 and max_right + dx > Settings.SCREEN_WIDTH - Settings.FLEET_EDGE_MARGIN) or \
           (self.direction < 0 and min_left + dx < Settings.FLEET_EDGE_MARGIN):
            self.direction *= -1
            for a in self.aliens:
                a.move(0, Settings.ALIEN_DROP_DISTANCE)
        else:
            for a in self.aliens:
                a.move(dx, 0)
        self.anim_timer += dt
        if self.anim_timer >= Settings.ALIEN_ANIM_INTERVAL:
            self.anim_timer = 0.0
            self.anim_frame = 1 - self.anim_frame
            for a in self.aliens:
                a.toggle_frame()
        return self.attempt_bomb_drop(dt, bomb_count)
    def attempt_bomb_drop(self, dt, current_bomb_count):
        if not self.aliens or current_bomb_count >= Settings.MAX_BOMBS:
            return None
        if random.random() < Settings.BOMB_CHANCE * dt:
            columns = {}
            for a in self.aliens:
                if a.col not in columns or a.rect.top > columns[a.col].rect.top:
                    columns[a.col] = a
            shooter = random.choice(list(columns.values()))
            return Bomb(shooter.rect.centerx, shooter.rect.bottom)
        return None
    def draw(self, screen):
        for a in self.aliens:
            a.draw(screen)