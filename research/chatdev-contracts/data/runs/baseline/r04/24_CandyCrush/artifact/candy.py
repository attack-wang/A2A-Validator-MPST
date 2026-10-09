'''
candy.py
Candy entity: logical grid position plus pixel position used for smooth
falling / swapping / clearing animations.
'''
import pygame
import config
class Candy:
    """A single candy on the board."""
    RADIUS_RATIO = 0.38  # candy radius relative to cell size
    def __init__(self, type_id, row, col):
        self.type = type_id
        self.row = row
        self.col = col
        # Pixel position (center of the candy)
        self.x, self.y = self.grid_to_pixel(row, col)
        self.scale = 1.0
        self.alpha = 255
        # Falling physics
        self.vy = 0.0
        self.falling = False
    @staticmethod
    def grid_to_pixel(row, col):
        x = config.BOARD_LEFT + col * config.CELL_SIZE + config.CELL_SIZE // 2
        y = config.BOARD_TOP + row * config.CELL_SIZE + config.CELL_SIZE // 2
        return x, y
    @property
    def target_x(self):
        return self.grid_to_pixel(self.row, self.col)[0]
    @property
    def target_y(self):
        return self.grid_to_pixel(self.row, self.col)[1]
    def start_fall(self, stagger=0.0):
        self.falling = True
        self.vy = 0.0
        self._stagger = stagger
    def update_fall(self, dt):
        """Accelerate toward target row; returns True when landed."""
        if not self.falling:
            return True
        if self._stagger > 0:
            self._stagger -= dt
            return False
        ty = self.target_y
        self.vy = min(self.vy + config.FALL_ACCELERATION * dt, config.MAX_FALL_SPEED)
        self.y += self.vy * dt
        if self.y >= ty:
            self.y = ty
            self.vy = 0.0
            self.falling = False
            return True
        return False
    @property
    def landed(self):
        return not self.falling
    def draw(self, surface):
        radius = int(config.CELL_SIZE * self.RADIUS_RATIO * self.scale)
        if radius <= 0:
            return
        color = config.CANDY_COLORS[self.type]
        rect = pygame.Rect(0, 0, radius * 2, radius * 2)
        rect.center = (int(self.x), int(self.y))
        # shadow
        ...