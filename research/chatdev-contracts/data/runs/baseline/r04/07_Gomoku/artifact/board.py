'''
Board model for the Gomoku game.
Stores the 15x15 grid, validates stone placement and detects
winning lines in all four axes.
'''
from constants import BOARD_SIZE, EMPTY, WIN_LENGTH
class Board:
    """15x15 Gomoku board: stores stones, validates moves, detects wins."""
    # Four axes to check: horizontal, vertical, two diagonals
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
    def __init__(self):
        """Create an empty 15x15 board."""
        self.size = BOARD_SIZE
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.last_move = None
        self.winning_line = None
    def reset(self):
        """Clear the board for a new game."""
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.last_move = None
        self.winning_line = None
    def place_stone(self, row, col, player):
        """Place a stone for `player`; return True if valid, False otherwise."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        if self.grid[row][col] != EMPTY:
            return False
        self.grid[row][col] = player
        self.last_move = (row, col)
        self.winning_line = None
        return True
    def get_cell(self, row, col):
        """Return the cell value at (row, col)."""
        return self.grid[row][col]
    def is_full(self):
        """Return True when every intersection is occupied (draw condition)."""
        return all(cell != EMPTY for row in self.grid for cell in row)
    def _count_direction(self, row, col, dr, dc, player):
        """Count consecutive stones of `player` starting from (row, col) in direction (dr, dc)."""
        count = 0
        r, c = row + dr, col + dc
        while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count
    def check_win(self, row, col, player):
        """Return the winning line of cells if `player` just won at (row, col)."""
        for dr, dc in self.DIRECTIONS:
            forward = self._count_direction(row, col, dr, dc, player)
            backward = self._count_direction(row, col, -dr, -dc, player)
            if forward + backward + 1 >= WIN_LENGTH:
                line = [(row - dr * i, col - dc * i) for i in range(backward, 0, -1)]
                line.append((row, col))
                line.extend((row + dr * i, col + dc * i) for i in range(1, forward + 1))
                self.winning_line = line
                return line
        return None