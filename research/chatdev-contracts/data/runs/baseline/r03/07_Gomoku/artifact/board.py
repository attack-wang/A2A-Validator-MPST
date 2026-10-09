'''
board.py
This module defines the Board class, which manages the Gomoku board:
stone placement, bounds/validity checks, win detection, and draw detection.
'''
class Board:
    """Represents the Gomoku board and its stones."""
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    def __init__(self, size=15):
        """Initialize an empty board of the given size (default 15x15)."""
        if size < 5:
            raise ValueError("board size must be at least 5")
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.last_move = None
    def reset(self):
        """Clear the board and reset last-move tracking."""
        self.grid = [[self.EMPTY for _ in range(self.size)]
                     for _ in range(self.size)]
        self.last_move = None
    def is_in_bounds(self, row, col):
        """Return True if (row, col) lies on the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    def get_stone(self, row, col):
        """Return the stone at (row, col), or EMPTY if out of bounds."""
        if not self.is_in_bounds(row, col):
            return self.EMPTY
        return self.grid[row][col]
    def is_valid_move(self, row, col):
        """A move is valid if it is in bounds and the cell is empty."""
        return self.is_in_bounds(row, col) and self.grid[row][col] == self.EMPTY
    def place_stone(self, row, col, stone):
        """Place a stone at (row, col). Returns True on success."""
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = stone
        self.last_move = (row, col)
        return True
    def is_full(self):
        """Return True if every cell is occupied."""
        return all(self.grid[r][c] != self.EMPTY
                   for r in range(self.size) for c in range(self.size))
    def check_win(self, row, col):
        """Return True if the stone at (row, col) completes five or more
        in a row horizontally, vertically, or diagonally."""
        stone = self.grid[row][col]
        if stone == self.EMPTY:
            return False
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while self.is_in_bounds(r, c) and self.grid[r][c] == stone:
                    count += 1
                    r += sign * dr
                    c += sign * dc
            if count >= 5:
                return True
        return False