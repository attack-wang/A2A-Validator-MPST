'''
board.py
Core game logic for the Reversi (Othello) board.
This module is completely independent of any GUI framework so that the
rules of Reversi can be unit-tested or reused with other front-ends.
Board representation:
    A BOARD_SIZE x BOARD_SIZE (default 8x8) grid stored as a list of lists.
    Each cell holds one of the integer constants:
        EMPTY (0) - no disc on the cell
        BLACK (1) - a black disc
        WHITE (2) - a white disc
'''
# Cell states
EMPTY = 0
BLACK = 1
WHITE = 2
BOARD_SIZE = 8
# The eight directions used for capture checks (row delta, column delta).
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
class Board:
    '''Represents the Reversi board and implements the flipping rules.'''
    def __init__(self, size=BOARD_SIZE):
        '''Initialise an empty board and place the four starting discs.'''
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]
        self._setup_starting_position()
    def _setup_starting_position(self):
        '''Place the four starting discs in the centre of the board.'''
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid][mid] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
    def in_bounds(self, row, col):
        '''Return True if (row, col) lies inside the board.'''
        return 0 <= row < self.size and 0 <= col < self.size
    def get_disc(self, row, col):
        '''Return the cell value at (row, col), or None if out of bounds.'''
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]
    def is_empty(self, row, col):
        '''Return True if (row, col) is on the board and has no disc.'''
        return self.in_bounds(row, col) and self.grid[row][col] == EMPTY
    def _flips_in_direction(self, row, col, player, dr, dc):
        '''Return discs that would be flipped from (row, col) in one direction.
        A capture requires a contiguous line of opponent discs starting next
        to (row, col) and ending at one of the player's own discs. Returns an
        empty list when the line is not closed by the player's disc.
        '''
        opponent = BLACK if player == WHITE else WHITE
        flips = []
        r, c = row + dr, col + dc
        while self.in_bounds(r, c) and self.grid[r][c] == opponent:
            flips.append((r, c))
            r += dr
            c += dc
        if flips and self.in_bounds(r, c) and self.grid[r][c] == player:
            return flips
        return []
    def flips_for_move(self, row, col, player):
        '''Return every disc that would be flipped if player plays (row, col).'''
        if not self.is_empty(row, col):
            return []
        flips = []
        for dr, dc in DIRECTIONS:
            flips.extend(self._flips_in_direction(row, col, player, dr, dc))
        return flips
    def is_valid_move(self, row, col, player):
        '''Return True if placing player's disc at (row, col) flips at least one disc.'''
        return bool(self.flips_for_move(row, col, player))
    def get_valid_moves(self, player):
        '''Return a list of all (row, col) cells where player may legally move.'''
        return [(r, c) for r in range(self.size) for c in range(self.size)
                if self.is_valid_move(r, c, player)]
    def place_disc(self, row, col, player):
        '''Place a disc and flip captured discs.
        Returns the list of flipped positions, or None if the move is invalid.
        '''
        flips = self.flips_for_move(row, col, player)
        if not flips:
            return None
        self.grid[row][col] = player
        for r, c in flips:
            self.grid[r][c] = player
        return flips
    def count_discs(self):
        '''Return a (black, white) tuple with the number of discs on the board.'''
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white
    def is_full(self):
        '''Return True when every cell holds a disc.'''
        return all(cell != EMPTY for row in self.grid for cell in row)
    def reset(self):
        '''Clear the board and restore the standard starting position.'''
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        self._setup_starting_position()