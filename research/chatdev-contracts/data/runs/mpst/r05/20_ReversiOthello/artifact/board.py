'''
board.py
Defines the Board class for the Reversi (Othello) game.
The Board is responsible for:
    * storing the 8x8 grid of discs,
    * validating candidate moves,
    * flipping opponent discs enclosed by the newly placed disc,
    * reporting the current score and game-state information.
Disc colours are represented by integer constants (EMPTY, BLACK, WHITE)
so the module can be reused by any front-end (console, GUI, etc.).
'''
# ---------------------------------------------------------------------------
# Game constants
# ---------------------------------------------------------------------------
BOARD_SIZE = 8      # Standard Othello board is 8x8
EMPTY = 0           # Cell without a disc
BLACK = 1           # Black disc (player 1)
WHITE = 2           # White disc (player 2)
# The eight directions used to search for flippable discs
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]
class Board:
    """Represents the Reversi (Othello) playing board and its rules."""
    def __init__(self):
        """Create an 8x8 grid and set up the standard starting position."""
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        # Standard Othello opening: two black and two white discs in the centre
        self.grid[3][3] = WHITE
        self.grid[3][4] = BLACK
        self.grid[4][3] = BLACK
        self.grid[4][4] = WHITE
    # -- helpers ------------------------------------------------------------
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    def opponent_of(self, player):
        """Return the opponent's colour for the given player."""
        return WHITE if player == BLACK else BLACK
    def get_cell(self, row, col):
        """Return the content of a cell (EMPTY, BLACK or WHITE)."""
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]
    # -- rule logic ----------------------------------------------------------
    def get_discs_to_flip(self, row, col, player):
        """
        Return the list of (row, col) tuples of opponent discs that would be
        flipped if `player` placed a disc on (row, col).
        A move is legal only when at least one disc would be flipped, so this
        method doubles as the validity checker.
        """
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        opponent = self.opponent_of(player)
        flips = []
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            line = []  # opponent discs found in this direction
            # Walk in the direction while we keep seeing opponent discs
            while self.in_bounds(r, c) and self.grid[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            # The line is flippable only if it is terminated by one of the
            # player's own discs (and contains at least one opponent disc)
            if line and self.in_bounds(r, c) and self.grid[r][c] == player:
                flips.extend(line)
        return flips
    def is_valid_move(self, row, col, player):
        """Return True if `player` may place a disc on (row, col)."""
        return len(self.get_discs_to_flip(row, col, player)) > 0
    def get_valid_moves(self, player):
        """Return a list of every legal (row, col) move for `player`."""
        return [
            (r, c)
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
            if self.is_valid_move(r, c, player)
        ]
    def has_valid_move(self, player):
        """Return True if `player` has at least one legal move."""
        return len(self.get_valid_moves(player)) > 0
    def place_disc(self, row, col, player):
        """
        Place a disc for `player` on (row, col) and flip all enclosed
        opponent discs.
        Returns the list of flipped (row, col) tuples, or an empty list if
        the move is illegal (nothing is changed in that case).
        """
        flips = self.get_discs_to_flip(row, col, player)
        if not flips:
            return []
        self.grid[row][col] = player
        for r, c in flips:
            self.grid[r][c] = player
        return flips
    # -- state queries -------------------------------------------------------
    def is_full(self):
        """Return True when every cell holds a disc."""
        return all(
            self.grid[r][c] != EMPTY
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
        )
    def count_discs(self):
        """Return a tuple (black_count, white_count) with the current score."""
        black = sum(row.count(BLACK) for row in self.grid)
        white = sum(row.count(WHITE) for row in self.grid)
        return black, white