'''
board.py
Board model for the Gomoku game: grid management, stone placement
and win / draw detection.
'''
from config import BOARD_SIZE, EMPTY
class Board:
    """Represents the 15x15 Gomoku board and its rules."""
    # Directions used for five-in-a-row detection:
    # horizontal, vertical, main diagonal, anti-diagonal
    DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.winning_cells = []
    def reset(self):
        """Clear every stone and forget the stored winning line."""
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.winning_cells = []
    def is_valid_move(self, row, col):
        """Return True when (row, col) lies inside the board and is empty."""
        return (0 <= row < self.size and 0 <= col < self.size
                and self.grid[row][col] == EMPTY)
    def place_stone(self, row, col, player):
        """
        Place a stone for `player` at (row, col) when the move is valid.
        Returns True on success, False otherwise.
        """
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        return True
    def get_stone(self, row, col):
        """Return the value at (row, col): EMPTY, PLAYER_BLACK or PLAYER_WHITE."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None
    def check_win(self, row, col, player):
        """
        Check whether the stone just placed at (row, col) by `player`
        completes five or more in a row in any direction. The winning
        cells are stored in `winning_cells` for highlighting.
        Returns True when the player has won.
        """
        for dr, dc in self.DIRECTIONS:
            cells = [(row, col)]
            for sign in (1, -1):
                r, c = row + sign * dr, col + sign * dc
                while (0 <= r < self.size and 0 <= c < self.size
                       and self.grid[r][c] == player):
                    cells.append((r, c))
                    r += sign * dr
                    c += sign * dc
            if len(cells) >= 5:
                self.winning_cells = cells
                return True
        return False
    def is_full(self):
        """Return True when no empty intersection remains (draw)."""
        return all(cell != EMPTY for line in self.grid for cell in line)