'''
board.py
Board representation and rules for Gomoku (Five in a Row).
The Board class stores the 15x15 grid, validates moves, places stones,
and checks whether the most recently placed stone completes an
unbroken line of five (horizontally, vertically, or diagonally).
'''
# Cell values
EMPTY = 0
BLACK = 1
WHITE = 2
class Board:
    """The Gomoku playing field and its rules."""
    def __init__(self, size=15):
        """
        Create an empty board.
        :param size: number of rows/columns (standard Gomoku: 15).
        """
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]
    # ------------------------------------------------------------------ #
    # Queries
    # ------------------------------------------------------------------ #
    def in_bounds(self, row, col):
        """True if (row, col) lies on the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    def is_valid_move(self, row, col):
        """True if (row, col) is on the board and currently empty."""
        return self.in_bounds(row, col) and self.grid[row][col] == EMPTY
    def get_stone(self, row, col):
        """
        Return the cell value at (row, col).
        Returns None for coordinates outside the board, which makes
        boundary checks in the win detection trivial.
        """
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None
    def is_full(self):
        """True when every cell is occupied (draw condition)."""
        return all(cell != EMPTY for row in self.grid for cell in row)
    # ------------------------------------------------------------------ #
    # Mutations
    # ------------------------------------------------------------------ #
    def place_stone(self, row, col, stone):
        """
        Put a stone on the board.
        :return: True if the stone was placed, False for invalid moves.
        """
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = stone
        return True
    def reset(self):
        """Remove all stones from the board."""
        self.grid = [[EMPTY] * self.size for _ in range(self.size)]
    # ------------------------------------------------------------------ #
    # Win detection
    # ------------------------------------------------------------------ #
    def check_win(self, row, col, stone):
        """
        Decide whether the stone just placed at (row, col) wins the game.
        Scans the four axes (horizontal, vertical, both diagonals) and
        counts contiguous stones of the same colour through (row, col).
        Five or more in a line completes the win (free-style Gomoku).
        """
        directions = ((0, 1), (1, 0), (1, 1), (1, -1))
        for dr, dc in directions:
            count = 1  # the stone that was just placed
            # Walk in the positive direction of the axis.
            r, c = row + dr, col + dc
            while self.get_stone(r, c) == stone:
                count += 1
                r += dr
                c += dc
            # Walk in the negative direction of the axis.
            r, c = row - dr, col - dc
            while self.get_stone(r, c) == stone:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False