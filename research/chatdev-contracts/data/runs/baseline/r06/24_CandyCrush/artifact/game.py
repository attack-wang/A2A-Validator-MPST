"""Game state machine: input, swap validation, cascades, scoring, timers."""
import random
import constants as c
from board import Board
class Game:
    def __init__(self):
        self.board = Board(c.GRID_ROWS, c.GRID_COLS, c.NUM_CANDY_TYPES)
        self.reset()
    def reset(self):
        self.board.generate()
        self.score = 0
        self.moves_left = c.INITIAL_MOVES
        self.time_left = float(c.TIME_LIMIT_SECONDS)
        self.state = "idle"
        self.selected = None  # (row, col)
        self.cascade = 0
        self.swap_anim = None  # dict(candy_a, candy_b, t, duration, revert)
        self.clearing = []  # list of dicts {candy, t}
        self.falling = []   # candies
        self.popups = []    # dicts {text, x, y, t, color}
        self.message = ""
        self.message_timer = 0.0
        self.hint = None    # (pos_a, pos_b)
        self.hint_timer = 0.0
        self.game_over = False
        self.won = False