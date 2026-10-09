'''
Candy entity with grid position, pixel position and animation state.
'''
import random
import settings
class Candy:
    def __init__(self, type_id, row, col):
        self.type = type_id
        self.row = row
        self.col = col
        self.pixel_x, self.pixel_y = self.grid_to_pixel(row, col)
        self.fall_velocity = 0.0
        self.falling = False
        self.target_pixel_y = self.pixel_y
        self.clearing = False
        self.clear_progress = 0.0
    @staticmethod
    def grid_to_pixel(row, col):
        '''Convert grid coordinates to top-left pixel coordinates.'''
        x = settings.BOARD_OFFSET_X + col * settings.CELL_SIZE
        y = settings.BOARD_OFFSET_Y + row * settings.CELL_SIZE
        return x, y
    def start_fall(self, target_pixel_y):
        '''Begin a falling animation toward the given pixel y.'''
        self.falling = True
        self.fall_velocity = 0.0
        self.target_pixel_y = target_pixel_y
    def update_fall(self, dt):
        '''Accelerate downward; snap to target when reached.'''
        self.fall_velocity = min(self.fall_velocity + settings.FALL_ACCELERATION * dt, settings.MAX_FALL_SPEED)
        self.pixel_y += self.fall_velocity * dt
        if self.pixel_y >= self.target_pixel_y:
            self.pixel_y = self.target_pixel_y
            self.falling = False
            self.fall_velocity = 0.0
    def start_clear(self):
        '''Begin the clear/shrink animation.'''
        self.clearing = True
        self.clear_progress = 0.0
    def update_clear(self, dt):
        '''Advance clear animation; returns True when finished.'''
        self.clear_progress += dt / settings.CLEAR_DURATION
        if self.clear_progress >= 1.0:
            self.clear_progress = 1.0
            return True
        return False
    @property
    def center(self):
        '''Center pixel coordinates of this candy.'''
        return (self.pixel_x + settings.CELL_SIZE // 2, self.pixel_y + settings.CELL_SIZE // 2)