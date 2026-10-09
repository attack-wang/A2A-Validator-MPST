'''Candy piece model with grid position and animated pixel position.'''
import config
import utils
class Candy:
    """A single candy on the board.
    Handles logical grid position (row, col) plus a pixel-space position
    used for smooth swap / fall / clear animations.
    """
    def __init__(self, type_id, row, col):
        self.type_id = type_id
        self.row = row
        self.col = col
        self.x, self.y = utils.grid_to_pixel(row, col)
        self.scale = 1.0
        self.alpha = 255
        self.is_falling = False
        self.vy = 0.0
        self.is_clearing = False
    # --- position helpers -------------------------------------------------
    @property
    def target_x(self):
        return utils.grid_to_pixel(self.row, self.col)[0]
    @property
    def target_y(self):
        return utils.grid_to_pixel(self.row, self.col)[1]
    def snap_to_grid(self, row=None, col=None):
        """Place the candy at a grid cell and align its pixel position."""
        if row is not None:
            self.row = row
        if col is not None:
            self.col = col
        self.x, self.y = utils.grid_to_pixel(self.row, self.col)
        self.is_falling = False
        self.vy = 0.0
    def start_fall(self, initial_y=None):
        """Begin a gravity-driven fall toward the candy's grid cell."""
        if initial_y is not None:
            self.y = initial_y
        self.is_falling = True
        self.vy = config.FALL_INITIAL_SPEED
    def update_fall(self, dt):
        """Advance a falling candy; returns True once it has settled."""
        if not self.is_falling:
            return True
        self.vy = min(self.vy + config.FALL_GRAVITY * dt, config.FALL_MAX_SPEED)
        self.y += self.vy * dt
        if self.y >= self.target_y:
            self.y = self.target_y
            self.is_falling = False
            self.vy = 0.0
            return True
        return False
    def is_at_rest(self):
        return (not self.is_falling
                and abs(self.y - self.target_y) < 0.5
                and abs(self.x - self.target_x) < 0.5)