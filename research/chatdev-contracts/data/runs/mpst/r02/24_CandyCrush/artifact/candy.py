'''Candy entity used on the match-3 board.'''
import random
from constants import CANDY_TYPES
class Candy:
    """Represents a single candy on the board.
    Attributes:
        type_index: Index into CANDY_TYPES determining color/shape.
        row, col: Logical grid position.
        x, y: Current animated pixel position (top-left of the cell).
        scale: Draw scale used for the clear animation (1.0 -> 0.0).
        clearing: True while the candy is playing its clear animation.
        spawn_row: Row the candy started falling from (for animation).
    """
    def __init__(self, type_index, row, col):
        self.type_index = type_index
        self.row = row
        self.col = col
        self.x = 0.0
        self.y = 0.0
        self.scale = 1.0
        self.clearing = False
        self.fall_start_y = None  # pixel y where a fall animation began
    @property
    def name(self):
        return CANDY_TYPES[self.type_index][0]
    @property
    def color(self):
        return CANDY_TYPES[self.type_index][1]
    @property
    def highlight(self):
        return CANDY_TYPES[self.type_index][2]
    @property
    def shape(self):
        return CANDY_TYPES[self.type_index][3]
    @staticmethod
    def random_type():
        return random.randrange(len(CANDY_TYPES))