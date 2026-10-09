"""
board.py
Core game logic for the Reversi (Othello) board game.
Defines board constants (EMPTY, BLACK, WHITE), the eight movement
directions used for disc flipping, and the `Board` class that manages
the 8x8 grid, legal move detection, disc placement/flipping and score
keeping.
"""
EMPTY = 0
BLACK = 1
WHITE = 2
BOARD_SIZE = 8
# All eight directions: horizontal, vertical and diagonal.
DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
)
COLOR_NAMES = {BLACK: "Black", WHITE: "White"}
class Board:
    """Represents the 8x8 Reversi board and implements the game rules."""
    def __init__(self, size=BOARD_SIZE):
        """Create a new board with the standard starting position."""
        if size < 4 or size % 2 != 0:
            raise ValueError("Board size must be an even number >= 4")
        self.size = size
        self.grid = [[EMPTY] * size for _ in range(size)]
        mid = size // 2
        # Standard Othello opening: white top-left/bottom-right of centre,
        # black top-right/bottom-left.
        self.grid[mid - 1][mid - 1] = WHITE
        self.grid[mid - 1][mid] = BLACK
        self.grid[mid][mid - 1] = BLACK
        self.grid[mid][mid] = WHITE
    # -- helpers -----------------------------------------------------
    def in_bounds(self, row, col):
        """Return True if (row, col) lies inside the board."""
        return 0 <= row < self.size and 0 <= col < self.size
    def get_cell(self, row, col):
        """Return the cell content at (row, col)."""
        if not self.in_bounds(row, col):
            raise IndexError(f"Cell ({row}, {col}) is outside the board")
        return self.grid[row][col]
    @staticmethod
    def opponent_of(player):
        """Return the opponent's colour for `player`."""
        return 3 - player  # BLACK(1) <-> WHITE(2)
    # -- rule logic --------------------------------------------------
    def get_flippable_discs(self, player, row, col):
        """
        Return the list of opponent discs that would be flipped if
        `player` placed a disc on the empty cell (row, col).
        A disc is flippable when it lies on a straight line (horizontal,
        vertical or diagonal) between the new disc and another disc of
        the player's own colour, with only opponent discs in between.
        Returns an empty list when the move is not legal.
        """
        if not self.in_bounds(row, col) or self.grid[row][col] != EMPTY:
            return []
        opponent = self.opponent_of(player)
        flippable = []
        for dr, dc in DIRECTIONS:
            line = []
            r, c = row + dr, col + dc
            # Walk over the contiguous run of opponent discs.
            while self.in_bounds(r, c) and self.grid[r][c] == opponent:
                line.append((r, c))
                r += dr
                c += dc
            # The run must be terminated by one of the player's own discs.
            if line and self.in_bounds(r, c) and self.grid[r][c] == player:
                flippable.extend(line)
        return flippable
    def is_valid_move(self, player, row, col):
        """Return True if `player` may place a disc on (row, col)."""
        return bool(self.get_flippable_discs(player, row, col))
    def get_valid_moves(self, player):
        """Return a list of every legal (row, col) move for `player`."""
        return [
            (r, c)
            for r in range(self.size)
            for c in range(self.size)
            if self.is_valid_move(player, r, c)
        ]
    def has_valid_move(self, player):
        """Return True if `player` has at least one legal move."""
        return bool(self.get_valid_moves(player))
    def place_disc(self, player, row, col):
        """
        Place a disc for `player` on (row, col) and flip all captured
        opponent discs. Returns the total number of the player's discs
        gained by the move (the new disc plus every flipped disc).
        Raises ValueError when the move is not legal.
        """
        flippable = self.get_flippable_discs(player, row, col)
        if not flippable:
            raise ValueError(
                f"Illegal move for {COLOR_NAMES[player]} at ({row}, {col})"
            )
        self.grid[row][col] = player
        for r, c in flippable:
            self.grid[r][c] = player
        return 1 + len(flippable)
    # -- state queries -------------------------------------------------
    def get_score(self):
        """Return a dict mapping each colour to its disc count."""
        score = {EMPTY: 0, BLACK: 0, WHITE: 0}
        for row in self.grid:
            for cell in row:
                score[cell] += 1
        return score
    def is_full(self):
        """Return True when every cell holds a disc."""
        return all(cell != EMPTY for row in self.grid for cell in row)
    def is_game_over(self):
        """Return True when the board is full or neither side can move."""
        if self.is_full():
            return True
        return not (self.has_valid_move(BLACK) or self.has_valid_move(WHITE))
    def copy(self):
        """Return an independent deep copy of the board."""
        clone = Board.__new__(Board)
        clone.size = self.size
        clone.grid = [row[:] for row in self.grid]
        return clone
    # -- rendering -------------------------------------------------------
    def __str__(self):
        """Return a plain-text rendering of the board (no move hints)."""
        return self.to_text(highlight=set())
    def to_text(self, highlight=None):
        """
        Return a text rendering of the board.
        `highlight` is an optional set of (row, col) cells (typically the
        legal moves) that are drawn with a '*' marker.
        """
        highlight = highlight or set()
        header = "   " + " ".join(chr(ord('A') + c) for c in range(self.size))
        lines = [header]
        for r in range(self.size):
            cells = []
            for c in range(self.size):
                if (r, c) in highlight:
                    cells.append("*")
                elif self.grid[r][c] == BLACK:
                    cells.append("X")
                elif self.grid[r][c] == WHITE:
                    cells.append("O")
                else:
                    cells.append(".")
            lines.append(f" {r + 1} " + " ".join(cells))
        return "\n".join(lines)