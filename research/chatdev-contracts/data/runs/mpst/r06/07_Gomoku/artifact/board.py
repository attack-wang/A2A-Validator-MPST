'''
board.py
Core game logic for the Gomoku game.
This module defines the Board class, which manages the 15x15 playing
grid, validates stone placements, detects five-in-a-row wins in all
four directions (horizontal, vertical, both diagonals), and tracks
whose turn it is.
'''
class Board:
    """Represents the Gomoku board and all of its game logic."""
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    WIN_COUNT = 5  # number of stones in a row needed to win
    def __init__(self, size=15):
        """Create an empty board of the given size (default 15x15)."""
        self.size = size
        self.grid = [[self.EMPTY for _ in range(size)] for _ in range(size)]
        self.current_player = self.BLACK
        self.last_move = None
        self.winning_line = []
    def reset(self):
        """Clear the board and reset turn state for a new game."""
        self.grid = [[self.EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = self.BLACK
        self.last_move = None
        self.winning_line = []
    def is_valid_move(self, row, col):
        """Return True if (row, col) is inside the board and empty."""
        return (
            0 <= row < self.size
            and 0 <= col < self.size
            and self.grid[row][col] == self.EMPTY
        )
    def place_stone(self, row, col):
        """
        Place a stone for the current player at (row, col).
        Returns a tuple (success, winner, winning_line):
          success       -- True if the move was legal and applied
          winner        -- Board.BLACK / Board.WHITE if that player just won,
                           Board.EMPTY (0) if the game continues, and None
                           when the move was illegal
          winning_line  -- list of (row, col) cells forming the win
        """
        if not self.is_valid_move(row, col):
            return False, None, []
        player = self.current_player
        self.grid[row][col] = player
        self.last_move = (row, col)
        if self.check_win(row, col, player):
            return True, player, list(self.winning_line)
        # Hand the turn over to the other player.
        self.current_player = self.WHITE if player == self.BLACK else self.BLACK
        return True, self.EMPTY, []
    def check_win(self, row, col, player):
        """
        Check whether the stone just placed at (row, col) by `player`
        completes an unbroken line of five. On success the winning
        cells are stored in self.winning_line.
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            line = [(row, col)]
            # Extend in the positive direction.
            r, c = row + dr, col + dc
            while (
                0 <= r < self.size
                and 0 <= c < self.size
                and self.grid[r][c] == player
            ):
                line.append((r, c))
                r += dr
                c += dc
            # Extend in the negative direction.
            r, c = row - dr, col - dc
            while (
                0 <= r < self.size
                and 0 <= c < self.size
                and self.grid[r][c] == player
            ):
                line.append((r, c))
                r -= dr
                c -= dc
            if len(line) >= self.WIN_COUNT:
                self.winning_line = line
                return True
        return False
    def is_full(self):
        """Return True when every cell is occupied (a draw)."""
        return all(
            self.grid[r][c] != self.EMPTY
            for r in range(self.size)
            for c in range(self.size)
        )
    def player_name(self, player):
        """Return a human-readable name for a player code."""
        return "Black" if player == self.BLACK else "White"