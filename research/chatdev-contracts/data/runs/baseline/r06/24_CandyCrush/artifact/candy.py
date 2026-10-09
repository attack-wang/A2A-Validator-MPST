class Candy:
    __slots__ = ("type_id", "row", "col", "x", "y", "vy", "scale", "alpha", "state")
    def __init__(self, type_id, row, col):
        self.type_id = type_id
        self.row = row
        self.col = col
        self.vy = 0.0
        self.scale = 1.0
        self.alpha = 255
        self.state = 'idle'
        self.x, self.y = self.cell_x(), self.cell_y()
    def cell_x(self): return c.BOARD_X + self.col * c.CELL_SIZE
    def cell_y(self): return c.BOARD_Y + self.row * c.CELL_SIZE
    def snap_to_cell(self):
        self.x, self.y = self.cell_x(), self.cell_y()
        self.vy = 0.0
        self.state = 'idle'
    def update_fall(self, dt):
        target = self.cell_y()
        self.vy = min(self.vy + c.GRAVITY_ACCELERATION * dt, c.MAX_FALL_SPEED)
        self.y += self.vy * dt
        if self.y >= target:
            self.y = target
            self.vy = 0.0
            self.state = 'idle'
            return True
        return False