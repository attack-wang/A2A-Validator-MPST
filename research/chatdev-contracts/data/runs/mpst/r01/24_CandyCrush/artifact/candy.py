"""A single candy on the board, with grid position and animation state."""
import math
import random
class Candy:
    IDLE = "idle"
    MOVING = "moving"
    CLEARING = "clearing"
    def __init__(self, type_id, row, col):
        self.type_id = type_id
        self.row = row
        self.col = col
        self.x = 0.0
        self.y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.state = Candy.IDLE
        self.clear_progress = 0.0
        self.vy = 0.0
        self.scale = 1.0
        self.wobble = random.random() * math.tau  # idle bobbing phase