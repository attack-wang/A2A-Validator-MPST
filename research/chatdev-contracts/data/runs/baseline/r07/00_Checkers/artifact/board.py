'''
board.py - 8x8 board representation, initial setup, and console rendering.
The board stores pieces on the dark squares only, where a square (row, col)
is dark (playable) when (row + col) is odd. Black starts on the top three
ranks, Red on the bottom three.
'''
from pieces import Piece, RED, BLACK
FILES = "abcdefgh"
CELL_WIDTH = 3
class Board:
    """The 8x8 checkers board and the pieces placed on it."""
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup()
    def setup(self):
        """Place 12 Black pieces on the top ranks and 12 Red pieces on the bottom ranks."""
        for row in range(3):
            for col in range(8):
                if self.is_playable((row, col)):
                    self.grid[row][col] = Piece(BLACK)
        for row in range(5, 8):
            for col in range(8):
                if self.is_playable((row, col)):
                    self.grid[row][col] = Piece(RED)
    def is_inside(self, pos):
        """True if (row, col) lies within the 8x8 board."""
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8
    def is_playable(self, pos):
        """True if the square is a dark (playable) checkers square."""
        row, col = pos
        return (row + col) % 2 == 1
    def get_piece(self, pos):
        """Return the Piece at (row, col), or None if the square is empty."""
        row, col = pos
        return self.grid[row][col]
    def set_piece(self, pos, piece):
        """Place `piece` (or None) on square (row, col)."""
        row, col = pos
        self.grid[row][col] = piece
    def render(self):
        """Return the board as a multi-line string for console display."""
        lines = []
        # Column labels aligned over the 3-character-wide cells.
        header = "     " + "  ".join(FILES)
        lines.append(header)
        border = "    +" + "---+" * 8
        lines.append(border)
        for row in range(8):
            rank = 8 - row
            cells = []
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None:
                    cells.append(" {} ".format(piece.symbol))
                elif self.is_playable((row, col)):
                    cells.append(" . ")
                else:
                    cells.append("   ")
            lines.append(" {:>1} |".format(rank) + "|".join(cells) + "|")
            lines.append(border)
        return "\n".join(lines)