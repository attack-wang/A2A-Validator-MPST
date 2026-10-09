'''
board.py
This module implements the Board class, which manages the 8x8 Reversi grid.
It is responsible for tracking disc placement, identifying valid moves,
computing flippable discs, and applying moves with disc flipping.
'''
from constants import (BOARD_SIZE, EMPTY, BLACK, WHITE, DIRECTIONS)
class Board:
    """Represents the 8x8 Reversi board and its game logic."""
    def __init__(self):
        """Initialize the board with the standard Reversi starting position."""
        self.reset()
    def reset(self):
        """Reset the grid to the standard starting position."""
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        center = BOARD_SIZE // 2  # 4
        # Standard start: two white, two black discs in the center
        self.grid[center - 1][center - 1] = WHITE
        self.grid[center][center] = WHITE
        self.grid[center - 1][center] = BLACK
        self.grid[center][center - 1] = BLACK
    def is_valid_position(self, row, col):
        """Return True if (row, col) lies within the board boundaries."""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    def get_disc(self, row, col):
        """Return the disc (player code or EMPTY) at the given position."""
        if not self.is_valid_position(row, col):
            return None
        return self.grid[row][col]
    def get_flippable_discs(self, row, col, player):
        """
        Return the list of (row, col) opponent discs that would be flipped
        if `player` places a disc at (row, col). Empty list if the move is
        invalid.
        """
        if not self.is_valid_position(row, col):
            return []
        if self.grid[row][col] != EMPTY:
            return []
        opponent = WHITE if player == BLACK else BLACK
        flippable = []
        for dr, dc in DIRECTIONS:
            row_line = []
            r, c = row + dr, col + dc
            # Walk along the direction collecting consecutive opponent discs
            while self.is_valid_position(r, c) and self.grid[r][c] == opponent:
                row_line.append((r, c))
                r += dr
                c += dc
            # The line is flippable only if it ends with one of the player's discs
            if row_line and self.is_valid_position(r, c) and self.grid[r][c] == player:
                flippable.extend(row_line)
        return flippable
    def get_valid_moves(self, player):
        """Return a list of all valid (row, col) moves for the given player."""
        valid_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] == EMPTY and self.get_flippable_discs(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves
    def is_valid_move(self, row, col, player):
        """Return True if `player` may place a disc at (row, col)."""
        return bool(self.get_flippable_discs(row, col, player))
    def place_disc(self, row, col, player):
        """
        Place a disc for `player` at (row, col), flipping all flippable
        opponent discs. Returns the list of flipped positions, or None if
        the move is invalid.
        """
        flippable = self.get_flippable_discs(row, col, player)
        if not flippable:
            return None
        self.grid[row][col] = player
        for r, c in flippable:
            self.grid[r][c] = player
        return flippable
    def is_full(self):
        """Return True if every cell on the board is occupied."""
        return all(
            self.grid[row][col] != EMPTY
            for row in range(BOARD_SIZE)
            for col in range(BOARD_SIZE)
        )
    def count_discs(self):
        """Return a tuple (black_count, white_count) of discs on the board."""
        black = 0
        white = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.grid[row][col] == BLACK:
                    black += 1
                elif self.grid[row][col] == WHITE:
                    white += 1
        return black, white
    def get_grid_copy(self):
        """Return a deep copy of the grid (useful for rendering snapshots)."""
        return [row[:] for row in self.grid]