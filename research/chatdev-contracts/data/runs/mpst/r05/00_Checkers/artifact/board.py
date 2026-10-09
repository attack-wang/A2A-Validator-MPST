'''
board.py
Defines the Board class: the 8x8 checkers board, its setup, low-level
piece manipulation and text rendering.
Coordinate system (used consistently everywhere):
  * grid rows 0..7, top to bottom; grid row 0 is rank 8
  * grid columns 0..7, left to right; column 0 is file 'a'
  * a square is playable (dark) iff (row + col) % 2 == 1
  * red starts on the bottom three ranks (grid rows 5..7) and moves up
  * black starts on the top three ranks (grid rows 0..2) and moves down
'''
import copy
class Board:
    """An 8x8 draughts board holding Piece objects (or None) per square."""
    SIZE = 8
    def __init__(self):
        """Create an empty grid and place the 24 starting pieces."""
        self.grid = [[None] * Board.SIZE for _ in range(Board.SIZE)]
        self.setup()
    def setup(self):
        """Place 12 red pieces on ranks 1-3 and 12 black pieces on ranks 6-8."""
        self.grid = [[None] * Board.SIZE for _ in range(Board.SIZE)]
        # Import here to avoid circular imports at module load time.
        from piece import Piece
        for r in range(3):            # black's three home ranks (8, 7, 6)
            for c in range(Board.SIZE):
                if self.is_playable(r, c):
                    self.grid[r][c] = Piece('b')
        for r in range(5, Board.SIZE):  # red's three home ranks (3, 2, 1)
            for c in range(Board.SIZE):
                if self.is_playable(r, c):
                    self.grid[r][c] = Piece('r')
    def in_bounds(self, r, c):
        """True if (r, c) lies on the 8x8 board."""
        return 0 <= r < Board.SIZE and 0 <= c < Board.SIZE
    def is_playable(self, r, c):
        """True if (r, c) is a dark square that pieces may occupy."""
        return self.in_bounds(r, c) and (r + c) % 2 == 1
    def get_piece(self, r, c):
        """Return the Piece at (r, c), or None if the square is empty."""
        return self.grid[r][c]
    def place_piece(self, piece, r, c):
        """Put a piece on (r, c); the square must be empty and playable."""
        if not self.is_playable(r, c):
            raise ValueError(f"({r}, {c}) is not a playable dark square")
        if self.grid[r][c] is not None:
            raise ValueError(f"({r}, {c}) is already occupied")
        self.grid[r][c] = piece
    def remove_piece(self, r, c):
        """Take whatever piece sits on (r, c) off the board and return it."""
        piece = self.grid[r][c]
        self.grid[r][c] = None
        return piece
    def move_piece(self, start, end):
        """Low-level primitive: move a piece from start to end.
        If the hop is a two-square jump, the enemy piece at the midpoint is
        removed.  Crowning is applied automatically when a man reaches the
        far rank.  No rule validation happens here — the Game layer owns that.
        """
        piece = self.remove_piece(*start)
        self.place_piece(piece, *end)
        # Remove the captured piece sitting between start and end (if any).
        mid_r = (start[0] + end[0]) // 2
        mid_c = (start[1] + end[1]) // 2
        if abs(end[0] - start[0]) == 2:
            self.remove_piece(mid_r, mid_c)
        # Crown a man that reaches the opposite back rank.
        back_rank = 0 if piece.color == 'r' else Board.SIZE - 1
        if not piece.is_king and end[0] == back_rank:
            piece.make_king()
        return piece
    def snapshot(self):
        """Return a deep copy of the board for safe move simulation."""
        return copy.deepcopy(self)
    def render(self):
        """Return the full board as a labelled text grid with coordinates."""
        lines = []
        # Column file labels along the top.
        lines.append("    a   b   c   d   e   f   g   h")
        lines.append("  +---+---+---+---+---+---+---+---+")
        for r in range(Board.SIZE):
            rank = Board.SIZE - r
            cells = []
            for c in range(Board.SIZE):
                piece = self.grid[r][c]
                cells.append(str(piece) if piece else '.')
            row = f"{rank} | " + " | ".join(cells) + f" | {rank}"
            lines.append(row)
            lines.append("  +---+---+---+---+---+---+---+---+")
        lines.append("    a   b   c   d   e   f   g   h")
        return "\n".join(lines)
    def count_pieces(self, color):
        """Count how many pieces of the given color remain on the board."""
        return sum(1 for r in range(Board.SIZE) for c in range(Board.SIZE)
                   if self.grid[r][c] and self.grid[r][c].color == color)