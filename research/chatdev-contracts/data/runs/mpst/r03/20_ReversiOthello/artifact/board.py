'''
board.py
This module defines the Board class, which encapsulates the Reversi (Othello)
game board: an 8x8 grid that stores disc positions, validates moves, flips
discs according to the game rules, and computes the current score.
'''
class Board:
    """Represents the 8x8 Reversi (Othello) board and its rules."""
    SIZE = 8
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    # The eight directions used to search for discs that must be flipped.
    DIRECTIONS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]
    def __init__(self):
        """Create an empty board and place the four initial centre discs."""
        self.grid = [[self.EMPTY for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        mid = self.SIZE // 2
        self.grid[mid - 1][mid - 1] = self.WHITE
        self.grid[mid - 1][mid] = self.BLACK
        self.grid[mid][mid - 1] = self.BLACK
        self.grid[mid][mid] = self.WHITE
    def is_on_board(self, row, col):
        """Return True if (row, col) lies inside the 8x8 grid."""
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    def get_disc(self, row, col):
        """Return the disc (or EMPTY) located at (row, col)."""
        if not self.is_on_board(row, col):
            return None
        return self.grid[row][col]
    def opponent(self, disc):
        """Return the disc colour opposite to `disc`."""
        return self.WHITE if disc == self.BLACK else self.BLACK
    def discs_to_flip(self, row, col, disc):
        """
        Return the list of (row, col) positions of opponent discs that would be
        flipped if `disc` were placed on (row, col). Returns an empty list when
        the move is not legal.
        """
        if not self.is_on_board(row, col) or self.grid[row][col] != self.EMPTY:
            return []
        opponent = self.opponent(disc)
        flips = []
        for dr, dc in self.DIRECTIONS:
            path = []
            r, c = row + dr, col + dc
            # Walk along the direction while we see opponent discs.
            while self.is_on_board(r, c) and self.grid[r][c] == opponent:
                path.append((r, c))
                r += dr
                c += dc
            # A legal capture needs at least one opponent disc terminated by
            # one of our own discs.
            if path and self.is_on_board(r, c) and self.grid[r][c] == disc:
                flips.extend(path)
        return flips
    def is_valid_move(self, row, col, disc):
        """Return True if `disc` may legally be placed on (row, col)."""
        return len(self.discs_to_flip(row, col, disc)) > 0
    def get_valid_moves(self, disc):
        """Return a list of all legal (row, col) moves for `disc`."""
        moves = []
        for row in range(self.SIZE):
            for col in range(self.SIZE):
                if self.is_valid_move(row, col, disc):
                    moves.append((row, col))
        return moves
    def has_valid_move(self, disc):
        """Return True if `disc` has at least one legal move."""
        return len(self.get_valid_moves(disc)) > 0
    def apply_move(self, row, col, disc):
        """
        Place `disc` on (row, col), flip all captured discs and return the
        list of flipped positions. Raises ValueError for illegal moves.
        """
        flips = self.discs_to_flip(row, col, disc)
        if not flips:
            raise ValueError(f"Illegal move: ({row}, {col}) for disc {disc}")
        self.grid[row][col] = disc
        for r, c in flips:
            self.grid[r][c] = disc
        return flips
    def count_discs(self, disc):
        """Return how many discs of `disc` are on the board."""
        return sum(row.count(disc) for row in self.grid)
    def is_full(self):
        """Return True when every square is occupied."""
        return all(cell != self.EMPTY for row in self.grid for cell in row)