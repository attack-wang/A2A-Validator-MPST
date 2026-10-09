'''
board.py
This module defines the Board class, which represents the 8x8 Reversi
(Othello) game board. It encapsulates all core board logic including:
- Board initialization with the standard four starting discs
- Validation of candidate moves
- Detection of flippable opponent discs in all eight directions
- Placement of discs and automatic flipping of captured discs
- Score counting and board-state queries (full board, valid moves, etc.)
'''
# Cell state constants
EMPTY = 0
BLACK = 1
WHITE = -1
# The eight directions (row delta, column delta) used to search for
# flippable discs around a candidate placement.
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
BOARD_SIZE = 8
class Board:
    """Represents the Reversi board and implements its rules."""
    def __init__(self, size=BOARD_SIZE):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self.reset()
    def reset(self):
        """Reset the board to the standard Reversi starting position."""
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE
    def is_valid_position(self, row, col):
        """Return True if (row, col) lies within the board boundaries."""
        return 0 <= row < self.size and 0 <= col < self.size
    def get_disc(self, row, col):
        """Return the disc state at (row, col): EMPTY, BLACK or WHITE."""
        if not self.is_valid_position(row, col):
            return None
        return self.grid[row][col]
    def get_flippable_discs(self, row, col, player):
        """
        Return the list of (row, col) positions of opponent discs that would
        be flipped if `player` placed a disc on the empty cell (row, col).
        Returns an empty list if the move is not legal.
        """
        if not self.is_valid_position(row, col):
            return []
        if self.grid[row][col] != EMPTY:
            return []
        opponent = -player
        flippable = []
        for dr, dc in DIRECTIONS:
            line = []
            r, c = row + dr, col + dc
            # Walk along the direction collecting opponent discs.
            while self.is_valid_position(r, c) and self.grid[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            # The line is only capturable if it ends on one of our own discs
            # and contains at least one opponent disc.
            if line and self.is_valid_position(r, c) and self.grid[r][c] == player:
                flippable.extend(line)
        return flippable
    def is_valid_move(self, row, col, player):
        """Return True if `player` may legally place a disc on (row, col)."""
        return len(self.get_flippable_discs(row, col, player)) > 0
    def get_valid_moves(self, player):
        """Return a list of all legal (row, col) moves for `player`."""
        moves = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_valid_move(row, col, player):
                    moves.append((row, col))
        return moves
    def has_valid_move(self, player):
        """Return True if `player` has at least one legal move."""
        return len(self.get_valid_moves(player)) > 0
    def place_disc(self, row, col, player):
        """
        Place a disc for `player` on (row, col) and flip all captured discs.
        Returns the list of flipped positions, or None if the move is illegal.
        """
        flippable = self.get_flippable_discs(row, col, player)
        if not flippable:
            return None
        self.grid[row][col] = player
        for r, c in flippable:
            self.grid[r][c] = player
        return flippable
    def get_score(self):
        """
        Return the current score as a dictionary:
        {'black': <count>, 'white': <count>}
        """
        black = 0
        white = 0
        for row in self.grid:
            for cell in row:
                if cell == BLACK:
                    black += 1
                elif cell == WHITE:
                    white += 1
        return {'black': black, 'white': white}
    def is_full(self):
        """Return True if every cell on the board is occupied."""
        for row in self.grid:
            for cell in row:
                if cell == EMPTY:
                    return False
        return True