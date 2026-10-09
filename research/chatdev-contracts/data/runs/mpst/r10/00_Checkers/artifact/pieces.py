'''
pieces.py
Defines the Piece class and color constants for the Checkers game.
'''
RED = 'red'
BLACK = 'black'
# Directions are (row_delta, col_delta) pairs.
# Row 0 is the top of the board (rank 8); row 7 is the bottom (rank 1).
# Red starts at the bottom and moves "up" the board (toward row 0).
# Black starts at the top and moves "down" the board (toward row 7).
FORWARD_RED = ((-1, -1), (-1, 1))
FORWARD_BLACK = ((1, -1), (1, 1))
ALL_DIRECTIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
PIECE_SYMBOLS = {
    (RED, False): 'r',
    (RED, True): 'R',
    (BLACK, False): 'b',
    (BLACK, True): 'B',
}
class Piece:
    """A single checkers piece (man or king) belonging to one player."""
    def __init__(self, color, is_king=False):
        self.color = color
        self.is_king = is_king
    def make_king(self):
        self.is_king = True
    @property
    def king_row(self):
        """Row index a piece must reach to be crowned."""
        return 0 if self.color == RED else 7
    def move_directions(self):
        """Directions this piece may move/capture in."""
        if self.is_king:
            return ALL_DIRECTIONS
        return FORWARD_RED if self.color == RED else FORWARD_BLACK
    def symbol(self):
        return PIECE_SYMBOLS[(self.color, self.is_king)]
    def __repr__(self):
        return f"Piece({self.color}, {'king' if self.is_king else 'man'})"