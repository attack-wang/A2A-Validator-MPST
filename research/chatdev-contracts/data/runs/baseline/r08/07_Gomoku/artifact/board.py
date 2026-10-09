'''
board.py
Board model for the Gomoku game. Manages the 15x15 grid, validates
stone placements, and detects win conditions of five consecutive
stones horizontally, vertically, or diagonally.
'''
from constants import BOARD_SIZE, WIN_COUNT, EMPTY
class Board:
    """Gomoku board: grid state, stone placement, and win detection."""
    def __init__(self, size=BOARD_SIZE):
        """Create an empty board of the given size (default 15x15)."""
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    def reset(self):
        """Remove all stones, restoring the board to its initial state."""
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
    def _in_bounds(self, row, col):
        """Return True if (row, col) lies within the board limits."""
        return 0 <= row < self.size and 0 <= col < self.size
    def is_empty(self, row, col):
        """Return True if the intersection at (row, col) holds no stone."""
        return self._in_bounds(row, col) and self.grid[row][col] == EMPTY
    def is_full(self):
        """Return True when every intersection is occupied (draw condition)."""
        return all(cell != EMPTY for row in self.grid for cell in row)
    def get_stone(self, row, col):
        """Return the value at (row, col): EMPTY, BLACK, or WHITE (None if out of bounds)."""
        if self._in_bounds(row, col):
            return self.grid[row][col]
        return None
    def place_stone(self, row, col, player):
        """
        Place a stone for `player` at (row, col).
        Returns True on success; False if the move is out of bounds or
        the intersection is already occupied.
        """
        if not self.is_empty(row, col):
            return False
        self.grid[row][col] = player
        return True
    def check_win(self, row, col, player):
        """
        Check whether the stone just placed at (row, col) by `player`
        completes a line of at least WIN_COUNT consecutive stones.
        Returns the list of (row, col) coordinates forming the winning
        line (including the placed stone), or an empty list if no win.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            line = [(row, col)]
            line.extend(self._collect_direction(row, col, player, dr, dc))
            line.extend(self._collect_direction(row, col, player, -dr, -dc))
            if len(line) >= WIN_COUNT:
                return line
        return []
    def _collect_direction(self, row, col, player, dr, dc):
        """
        Collect coordinates of consecutive `player` stones starting from
        (row, col) and stepping in direction (dr, dc). The starting cell
        itself is not included.
        """
        line = []
        r, c = row + dr, col + dc
        while self._in_bounds(r, c) and self.grid[r][c] == player:
            line.append((r, c))
            r += dr
            c += dc
        return line