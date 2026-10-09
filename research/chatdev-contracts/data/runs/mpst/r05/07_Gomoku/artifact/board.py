'''
board.py
Board model for the Gomoku game.
This module defines the `Board` class, which manages the 15 x 15 grid,
validates stone placements, detects five-in-a-row wins in all four
directions (horizontal, vertical, and both diagonals), and identifies
the exact set of stones that form a winning line.
'''
from config import BOARD_SIZE, EMPTY, WIN_LENGTH
class Board:
    """Represents the Gomoku playing board and its placement rules."""
    # The four directions to inspect for a win: horizontal, vertical,
    # main diagonal (down-right) and anti-diagonal (down-left).
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
    def __init__(self, size=BOARD_SIZE):
        """Create an empty board of the given size."""
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    def reset(self):
        """Remove every stone and restore the board to its initial state."""
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
    def is_valid_position(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    def is_empty(self, row, col):
        """Return True if (row, col) is inside the board and has no stone."""
        return self.is_valid_position(row, col) and self.grid[row][col] == EMPTY
    def get_stone(self, row, col):
        """Return the stone at (row, col); EMPTY when off-board or vacant."""
        if self.is_valid_position(row, col):
            return self.grid[row][col]
        return EMPTY
    def place_stone(self, row, col, player):
        """Place `player`'s stone at (row, col).
        Returns True when the cell was empty and the stone was placed,
        False when the move is illegal (off-board or occupied cell).
        """
        if not self.is_empty(row, col):
            return False
        self.grid[row][col] = player
        return True
    def is_full(self):
        """Return True when no empty cell remains (draw condition)."""
        for row in self.grid:
            if EMPTY in row:
                return False
        return True
    def _count_direction(self, row, col, player, dr, dc):
        """Count `player`'s contiguous stones from (row, col) along (dr, dc).
        The stone at (row, col) itself is NOT counted; only the stones
        strictly beyond it in the given direction are.
        """
        count = 0
        r, c = row + dr, col + dc
        while self.get_stone(r, c) == player:
            count += 1
            r += dr
            c += dc
        return count
    def check_win(self, row, col, player):
        """Return True if `player` has >= WIN_LENGTH aligned stones through (row, col)."""
        for dr, dc in self.DIRECTIONS:
            total = (1
                     + self._count_direction(row, col, player, dr, dc)
                     + self._count_direction(row, col, player, -dr, -dc))
            if total >= WIN_LENGTH:
                return True
        return False
    def get_winning_line(self, row, col, player):
        """Return the list of (row, col) cells forming the winning line.
        The returned list contains every contiguous stone of `player`
        through (row, col) along the first direction that reaches
        WIN_LENGTH, or None when there is no win.
        """
        for dr, dc in self.DIRECTIONS:
            cells = [(row, col)]
            r, c = row + dr, col + dc
            while self.get_stone(r, c) == player:
                cells.append((r, c))
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while self.get_stone(r, c) == player:
                cells.append((r, c))
                r -= dr
                c -= dc
            if len(cells) >= WIN_LENGTH:
                return cells
        return None