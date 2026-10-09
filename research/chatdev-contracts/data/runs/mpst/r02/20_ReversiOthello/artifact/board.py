'''
board.py
Core game logic for Reversi (Othello).
This module defines the Board class, which manages the 8x8 grid,
validates moves according to Reversi rules, flips bracketed opponent
discs, and computes the current score.
Disc constants:
    EMPTY  - an unoccupied square
    BLACK  - a black disc (Black always moves first)
    WHITE  - a white disc
'''
# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
EMPTY = 0
BLACK = 1
WHITE = 2
BOARD_SIZE = 8
# The eight directions in which captured discs may lie:
# up-left, up, up-right, left, right, down-left, down, down-right
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
class Board:
    '''
    Represents the Reversi playing board and implements the rules that
    govern disc placement and flipping.
    '''
    def __init__(self):
        '''Create an 8x8 board set up with the standard starting position.'''
        self.size = BOARD_SIZE
        self.grid = [[EMPTY for _ in range(self.size)] for _ in range(self.size)]
        mid = self.size // 2
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE
    def is_inside(self, row, col):
        '''Return True if (row, col) lies within the board boundaries.'''
        return 0 <= row < self.size and 0 <= col < self.size
    def get_disc(self, row, col):
        '''Return the content of a square: EMPTY, BLACK, WHITE (or None if off-board).'''
        if self.is_inside(row, col):
            return self.grid[row][col]
        return None
    def get_flippable_discs(self, row, col, player):
        '''
        Return the list of opponent-disc positions that would be flipped if
        `player` placed a disc on (row, col). The list is empty when the
        square is occupied, off the board, or the move captures nothing.
        '''
        if not self.is_inside(row, col) or self.grid[row][col] != EMPTY:
            return []
        opponent = WHITE if player == BLACK else BLACK
        flippable = []
        for dr, dc in DIRECTIONS:
            captured = []
            r, c = row + dr, col + dc
            # Walk outward, collecting consecutive opponent discs.
            while self.is_inside(r, c) and self.grid[r][c] == opponent:
                captured.append((r, c))
                r += dr
                c += dc
            # The line is only captured if it is terminated by one of the
            # player's own discs.
            if captured and self.is_inside(r, c) and self.grid[r][c] == player:
                flippable.extend(captured)
        return flippable
    def is_valid_move(self, row, col, player):
        '''Return True when `player` may legally place a disc on (row, col).'''
        return len(self.get_flippable_discs(row, col, player)) > 0
    def get_valid_moves(self, player):
        '''Return every legal (row, col) move currently available to `player`.'''
        return [
            (row, col)
            for row in range(self.size)
            for col in range(self.size)
            if self.is_valid_move(row, col, player)
        ]
    def has_valid_move(self, player):
        '''Return True when `player` has at least one legal move.'''
        return len(self.get_valid_moves(player)) > 0
    def place_disc(self, row, col, player):
        '''
        Place a disc for `player` on (row, col), flipping every bracketed
        opponent disc. Returns the list of flipped positions, or None when
        the move is illegal.
        '''
        flippable = self.get_flippable_discs(row, col, player)
        if not flippable:
            return None
        self.grid[row][col] = player
        for r, c in flippable:
            self.grid[r][c] = player
        return flippable
    def is_full(self):
        '''Return True when every square of the board is occupied.'''
        return all(cell != EMPTY for row in self.grid for cell in row)
    def get_score(self):
        '''Return the current score as a tuple (black_discs, white_discs).'''
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white