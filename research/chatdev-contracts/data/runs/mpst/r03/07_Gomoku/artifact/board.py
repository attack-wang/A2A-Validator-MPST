'''
board.py
Board model for the Gomoku game. Manages the 15x15 grid, validates
stone placement, and detects winning lines of five or more stones.
'''
from constants import BOARD_SIZE, EMPTY, BLACK, WHITE
class Board:
    """Represents the Gomoku board and its rules for placement and winning."""
    def __init__(self, size=BOARD_SIZE):
        """Initialize an empty board of the given size."""
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    def reset(self):
        """Clear the board back to its initial empty state."""
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
    def in_bounds(self, row, col):
        """Return True if (row, col) lies within the board limits."""
        return 0 <= row < self.size and 0 <= col < self.size
    def is_valid_move(self, row, col):
        """A move is valid when inside the board and on an empty intersection."""
        return self.in_bounds(row, col) and self.grid[row][col] == EMPTY
    def place_stone(self, row, col, stone):
        """
        Place a stone (BLACK or WHITE) at (row, col).
        Returns True on success, False if the move is invalid.
        """
        if stone not in (BLACK, WHITE):
            return False
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = stone
        return True
    def get_stone(self, row, col):
        """Return the stone value at (row, col), or EMPTY if out of bounds."""
        if not self.in_bounds(row, col):
            return EMPTY
        return self.grid[row][col]
    def is_full(self):
        """Return True when every intersection is occupied (draw condition)."""
        for row in self.grid:
            if EMPTY in row:
                return False
        return True
    def _count_direction(self, row, col, dr, dc, stone):
        """Count consecutive stones of `stone` starting one step from (row, col)."""
        count = 0
        r, c = row + dr, col + dc
        while self.in_bounds(r, c) and self.grid[r][c] == stone:
            count += 1
            r += dr
            c += dc
        return count
    def get_winning_line(self, row, col):
        """
        If the stone just placed at (row, col) completes five or more in a row,
        return the list of (row, col) coordinates of a contiguous winning line
        (always exactly five stones). Otherwise return None.
        """
        stone = self.get_stone(row, col)
        if stone == EMPTY:
            return None
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            forward = self._count_direction(row, col, dr, dc, stone)
            backward = self._count_direction(row, col, -dr, -dc, stone)
            if forward + backward + 1 >= 5:
                # Build the full contiguous line through the placed stone.
                line = [(row, col)]
                r, c = row + dr, col + dc
                for _ in range(forward):
                    line.append((r, c))
                    r += dr
                    c += dc
                r, c = row - dr, col - dc
                for _ in range(backward):
                    line.append((r, c))
                    r -= dr
                    c -= dc
                # Sort so we can return a clean run of exactly five stones
                # centered around the winning move.
                line.sort()
                # Trim to a contiguous window of five containing (row, col).
                # Find index of placed stone in sorted line.
                # Actually simpler: return the five consecutive stones that
                # include the placed stone. Since line is contiguous and sorted,
                # any window of 5 containing the placed stone works.
                idx = line.index((row, col))
                start = min(max(0, idx - 4), len(line) - 5)
                return line[start:start + 5]
        return None
    def check_win(self, row, col):
        """Return True if the stone at (row, col) is part of five in a row."""
        return self.get_winning_line(row, col) is not None