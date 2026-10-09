'''
board.py
Defines the Board class representing the 15x15 Gomoku board.
Handles stone placement, move validation, and win / draw detection.
'''
class Board:
    """Represents the Gomoku board and its core game logic."""
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    def __init__(self, size=15):
        """Create an empty board of the given size (default 15x15)."""
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
    def reset(self):
        """Clear the board back to its initial empty state."""
        self.grid = [[self.EMPTY for _ in range(self.size)]
                     for _ in range(self.size)]
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    def is_valid_move(self, row, col):
        """A move is valid when it is inside the board and the cell is empty."""
        return self.in_bounds(row, col) and self.grid[row][col] == self.EMPTY
    def place_stone(self, row, col, player):
        """Place a stone for the given player. Returns True on success."""
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        return True
    def get_cell(self, row, col):
        """Return the value of a cell (EMPTY, BLACK or WHITE), or None if out of bounds."""
        if self.in_bounds(row, col):
            return self.grid[row][col]
        return None
    def is_full(self):
        """Return True when every cell is occupied (draw condition)."""
        for row in self.grid:
            if self.EMPTY in row:
                return False
        return True
    def check_win(self, row, col, player):
        """Check whether the stone just placed at (row, col) forms five in a row.
        Scans the four axes (horizontal, vertical, both diagonals) around the
        last placed stone. Returns the list of winning coordinates for
        highlighting, or None if there is no win.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            line = [(row, col)]
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while (self.in_bounds(r, c)
                       and self.grid[r][c] == player):
                    line.append((r, c))
                    r += sign * dr
                    c += sign * dc
            if len(line) >= 5:
                line.sort()
                return line
        return None