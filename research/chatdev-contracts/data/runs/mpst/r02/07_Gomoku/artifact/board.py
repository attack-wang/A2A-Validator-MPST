'''
board.py
Game logic module containing the Board class.
The Board is responsible for the pure game state of Gomoku:
storing stones on a 15x15 grid, validating moves, and detecting
winning lines (five or more consecutive stones horizontally,
vertically, or diagonally). It contains no GUI code.
'''
from config import BOARD_SIZE, EMPTY
class Board:
    """Represents the Gomoku board and its game logic."""
    # The four directions to examine when checking for a win:
    # horizontal, vertical, and the two diagonals.
    DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
    def reset(self):
        """Clear the board back to its initial empty state."""
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
    def is_valid_move(self, row, col):
        """Return True if (row, col) is inside the board and empty."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col] == EMPTY
        return False
    def place_stone(self, row, col, player):
        """
        Place a stone for `player` at (row, col).
        Returns True if the move was valid and applied, False otherwise.
        """
        if not self.is_valid_move(row, col):
            return False
        self.grid[row][col] = player
        return True
    def get_stone(self, row, col):
        """Return the player occupying (row, col), or EMPTY."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col]
        return None
    def is_full(self):
        """Return True if every intersection is occupied (draw)."""
        for row in self.grid:
            for cell in row:
                if cell == EMPTY:
                    return False
        return True
    def check_win(self, row, col, player):
        """
        Check whether the stone just placed by `player` at (row, col)
        completes five or more in a row.
        Returns:
            A list of (row, col) tuples describing the winning line
            (exactly five stones), or an empty list if no win.
        """
        for dr, dc in self.DIRECTIONS:
            cells = [(row, col)]
            # Count in the positive direction of the axis
            r, c = row + dr, col + dc
            while self.get_stone(r, c) == player:
                cells.append((r, c))
                r += dr
                c += dc
            # Count in the negative direction of the axis
            r, c = row - dr, col - dc
            while self.get_stone(r, c) == player:
                cells.insert(0, (r, c))
                r -= dr
                c -= dc
            if len(cells) >= 5:
                # Return exactly five consecutive stones containing the
                # last move so the GUI can highlight a clean line.
                for i in range(len(cells) - 4):
                    window = cells[i:i + 5]
                    if (row, col) in window:
                        return window
                return cells[-5:]
        return []