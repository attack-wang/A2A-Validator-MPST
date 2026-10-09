'''Candy entity: a single game piece with grid position, pixel position and animation state.'''
import config
class Candy:
    IDLE = 'idle'
    SWAP = 'swap'
    FALL = 'fall'
    CLEAR = 'clear'
    def __init__(self, type_id, row, col):
        self.type_id = type_id
        self.row = row
        self.col = col
        self.x = col * config.CELL_SIZE
        self.y = row * config.CELL_SIZE
        self.tx = self.x
        self.ty = self.y
        self.mode = Candy.IDLE
        self.timer = 0.0
        self.dead = False
        self.fall_speed = 0.0
        self.from_x = 0.0
        self.from_y = 0.0
    @property
    def center(self):
        return (self.x + config.CELL_SIZE // 2, self.y + config.CELL_SIZE // 2)
    def start_swap(self, row, col):
        # logical position updated by board; animate from current pixel pos to target
        self.from_x, self.from_y = self.x, self.y
        self.tx = col * config.CELL_SIZE
        self.ty = row * config.CELL_SIZE
        self.mode = Candy.SWAP
        self.timer = 0.0
    def start_fall(self):
        self.tx = self.col * config.CELL_SIZE
        self.ty = self.row * config.CELL_SIZE
        self.mode = Candy.FALL
        self.fall_speed = 0.0
    def start_clear(self):
        self.mode = Candy.CLEAR
        self.timer = 0.0
    def update(self, dt):
        if self.mode == Candy.SWAP:
            self.timer += dt
            t = min(1.0, self.timer / config.SWAP_DURATION)
            # ease in-out
            e = t * t * (3 - 2 * t)
            self.x = self.from_x + (self.tx - self.from_x) * e
            self.y = self.from_y + (self.ty - self.from_y) * e
            if t >= 1.0:
                self.x, self.y = self.tx, self.ty
                self.mode = Candy.IDLE
        elif self.mode == Candy.FALL:
            self.fall_speed = min(self.fall_speed + config.FALL_GRAVITY * dt, config.MAX_FALL_SPEED)
            self.y += self.fall_speed * dt
            if self.y >= self.ty:
                self.y = self.ty
                self.mode = Candy.IDLE
        elif self.mode == Candy.CLEAR:
            self.timer += dt
            if self.timer >= config.CLEAR_DURATION:
                self.dead = True
    @property
    def clear_progress(self):
        if self.mode == Candy.CLEAR:
            return min(1.0, self.timer / config.CLEAR_DURATION)
        return 0.0
    def is_settled(self):
        return self.mode == Candy.IDLE and not self.dead