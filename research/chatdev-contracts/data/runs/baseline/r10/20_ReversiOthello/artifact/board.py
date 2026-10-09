'''
board.py
This module contains the Board class, which represents the 8x8 Reversi
board: disc placement, valid-move detection, disc flipping, and scoring.
'''
EMPTY = 0
BLACK = 1
WHITE = 2
BOARD_SIZE = 8
# All 8 directions: horizontal, vertical, and diagonal.
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]
class Board:
    """8x8 Reversi board with move validation and disc flipping."""
    def __init__(self):
        """Create an empty 8x8 grid and place the four starting discs."""
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)]
                     for _ in range(BOARD_SIZE)]
        # Standard starting position in the center of the board.
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE
    @staticmethod
    def get_opponent(player):
        """Return the opponent's color."""
        return WHITE if player == BLACK else BLACK
    @staticmethod
    def in_bounds(row, col):
        """Return True if (row, col) lies within the 8x8 board."""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    def get_flippable_discs(self, row, col, player):
        """
        Return the list of opponent discs that would be flipped if `player`
        played at (row, col). An empty list means the move is not valid.
        """
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        opponent = self.get_opponent(player)
        flippable = []
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            line = []
            while self.in_bounds(r, c) and self.grid[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            if line and self.in_bounds(r, c) and self.grid[r][c] == player:
                flippable.extend(line)
        return flippable
    def is_valid_move(self, row, col, player):
        """A move is valid only if it flips at least one opponent disc."""
        return len(self.get_flippable_discs(row, col, player)) > 0
    def get_valid_moves(self, player):
        """Return a list of all valid (row, col) moves for `player`."""
        return [(row, col)
                for row in range(BOARD_SIZE)
                for col in range(BOARD_SIZE)
                if self.is_valid_move(row, col, player)]
    def has_valid_move(self, player):
        """Return True if `player` has at least one valid move."""
        return len(self.get_valid_moves(player)) > 0
    def make_move(self, row, col, player):
        """Place a disc at (row, col) and flip all captured discs."""
        flippable = self.get_flippable_discs(row, col, player)
        if not flippable:
            return False
        self.grid[row][col] = player
        for r, c in flippable:
            self.grid[r][c] = player
        return True
    def count_discs(self):
        """Return the current score as (black_count, white_count)."""
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white
    def is_full(self):
        """Return True if no empty cells remain."""
        return all(cell != EMPTY for row in self.grid for cell in row)