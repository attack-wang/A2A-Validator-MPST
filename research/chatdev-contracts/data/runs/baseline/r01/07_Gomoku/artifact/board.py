'''
board.py
This module implements the core Gomoku game logic on a 15x15 board. The Board
class stores stone positions, validates moves, places stones, detects winning
alignments (horizontal, vertical, and both diagonals) and full-board draws.
It is fully independent of any GUI framework so it can be unit-tested or reused
with other front-ends.
'''
from constants import (BOARD_SIZE, WIN_COUNT, PLAYER_EMPTY, PLAYER_BLACK,
                       PLAYER_WHITE)
# The four directions to scan when checking for a winning alignment:
# horizontal, vertical, main diagonal, anti-diagonal.
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
class Board:
    """Game board holding the 15x15 grid and all pure game logic."""
    def __init__(self, size=BOARD_SIZE):
        self._size = size
        self._grid = [[PLAYER_EMPTY for _ in range(size)] for _ in range(size)]
        self._stones_placed = 0
    @property
    def size(self):
        return self._size
    def reset(self):
        """Clear the board back to an empty starting state."""
        self._grid = [[PLAYER_EMPTY for _ in range(self._size)] for _ in range(self._size)]
        self._stones_placed = 0
    def in_bounds(self, row, col):
        """Return True if (row, col) lies on the board."""
        return 0 <= row < self._size and 0 <= col < self._size
    def is_valid_move(self, row, col):
        """A move is valid when inside the board and on an empty intersection."""
        return self.in_bounds(row, col) and self._grid[row][col] == PLAYER_EMPTY
    def place_stone(self, row, col, player_id):
        """Place a stone for player_id at (row, col). Returns True on success."""
        if not self.is_valid_move(row, col):
            return False
        self._grid[row][col] = player_id
        self._stones_placed += 1
        return True
    def get_stone(self, row, col):
        """Return the player id occupying (row, col), or PLAYER_EMPTY."""
        if not self.in_bounds(row, col):
            return None
        return self._grid[row][col]
    def is_full(self):
        """Return True when every intersection is occupied (draw condition)."""
        return self._stones_placed >= self._size * self._size
    def check_win(self, row, col):
        """
        Check whether the stone just placed at (row, col) completes an
        unbroken line of at least WIN_COUNT stones in any direction.
        Returns the list of (row, col) coordinates forming the winning line,
        or None when there is no win.
        """
        player_id = self._grid[row][col]
        if player_id == PLAYER_EMPTY:
            return None
        for d_row, d_col in DIRECTIONS:
            line = [(row, col)]
            # Extend in the positive direction of (d_row, d_col).
            line += self._collect_line(row, col, d_row, d_col, player_id)
            # Extend in the opposite direction.
            line += self._collect_line(row, col, -d_row, -d_col, player_id)
            if len(line) >= WIN_COUNT:
                line.sort()
                return line
        return None
    def _collect_line(self, row, col, d_row, d_col, player_id):
        """Collect consecutive same-player stones stepping from (row, col)."""
        collected = []
        n_row, n_col = row + d_row, col + d_col
        while (self.in_bounds(n_row, n_col)
               and self._grid[n_row][n_col] == player_id):
            collected.append((n_row, n_col))
            n_row += d_row
            n_col += d_col
        return collected