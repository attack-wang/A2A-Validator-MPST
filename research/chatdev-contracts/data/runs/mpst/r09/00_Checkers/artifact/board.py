'''
board.py
Board representation for the Checkers game: setup, rendering, and
legal-move/capture generation for pieces of either color.
'''
from piece import Piece, PieceColor
class Board:
    """An 8x8 checkers board with pieces placed on the dark squares."""
    SIZE = 8
    FILES = "abcdefgh"
    def __init__(self):
        self.grid = [[None] * self.SIZE for _ in range(self.SIZE)]
        self._setup()
    def _setup(self):
        """Place 12 Red men (top) and 12 Black men (bottom) on dark squares."""
        for r in range(3):          # grid rows 0-2: Red men
            for c in range(self.SIZE):
                if self.is_dark(r, c):
                    self.grid[r][c] = Piece(PieceColor.RED)
        for r in range(5, 8):       # grid rows 5-7: Black men
            for c in range(self.SIZE):
                if self.is_dark(r, c):
                    self.grid[r][c] = Piece(PieceColor.BLACK)
    @staticmethod
    def is_dark(r, c):
        """True if square (r, c) is a playable (dark) square."""
        return (r + c) % 2 == 0
    @staticmethod
    def in_bounds(r, c):
        """True if (r, c) lies within the 8x8 board."""
        return 0 <= r < Board.SIZE and 0 <= c < Board.SIZE
    @classmethod
    def parse_square(cls, text):
        """Convert algebraic notation like 'b6' to (row, col); None if invalid."""
        text = text.strip().lower()
        if len(text) == 2 and text[0] in cls.FILES and text[1].isdigit():
            c = cls.FILES.index(text[0])
            r = cls.SIZE - int(text[1])   # rank 1 is bottom row (row 7)
            if cls.in_bounds(r, c):
                return (r, c)
        return None
    @staticmethod
    def square_name(r, c):
        """Convert (row, col) to algebraic notation like 'b6'."""
        return f"{Board.FILES[c]}{Board.SIZE - r}"
    def get_piece(self, r, c):
        """Return the piece at (r, c), or None if empty/out of bounds."""
        if not self.in_bounds(r, c):
            return None
        return self.grid[r][c]
    def count_pieces(self, color):
        """Count all pieces of the given color still on the board."""
        return sum(1 for r in range(self.SIZE) for c in range(self.SIZE)
                   if self.grid[r][c] and self.grid[r][c].color is color)
    def display(self):
        """Render the board as a text grid with file letters and rank numbers."""
        lines = []
        lines.append("    a b c d e f g h")
        lines.append("  +-----------------+")
        for r in range(self.SIZE):
            rank = self.SIZE - r
            cells = []
            for c in range(self.SIZE):
                piece = self.grid[r][c]
                cells.append(piece.symbol if piece else ".")
            lines.append(f"{rank} | {' '.join(cells)} | {rank}")
        lines.append("  +-----------------+")
        lines.append("    a b c d e f g h")
        return "\n".join(lines)
    def has_capture(self, color):
        """True if any piece of `color` currently has a capture available."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                piece = self.grid[r][c]
                if piece and piece.color is color and self.get_piece_captures(r, c):
                    return True
        return False
    def get_piece_captures(self, r, c):
        """Return list of landing squares (r2, c2) for legal jumps from (r, c)."""
        piece = self.grid[r][c]
        if piece is None:
            return []
        captures = []
        for dr, dc in piece.directions():
            mid_r, mid_c = r + dr, c + dc
            land_r, land_c = r + 2 * dr, c + 2 * dc
            if not self.in_bounds(land_r, land_c):
                continue
            mid = self.grid[mid_r][mid_c]
            if mid and mid.color is not piece.color and self.grid[land_r][land_c] is None:
                captures.append((land_r, land_c))
        return captures
    def get_piece_moves(self, r, c):
        """Legal destinations for the piece at (r, c), honoring mandatory capture."""
        piece = self.grid[r][c]
        if piece is None:
            return []
        captures = self.get_piece_captures(r, c)
        if captures:
            return captures  # captures take priority for this piece
        if self.has_capture(piece.color):
            return []  # must capture with another piece
        moves = []
        for dr, dc in piece.directions():
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.grid[nr][nc] is None:
                moves.append((nr, nc))
        return moves
    def get_captures_for_piece(self, r, c):
        """Alias kept for game.py compatibility: legal jump landings from (r, c)."""
        return self.get_piece_captures(r, c)
    def player_has_moves(self, color):
        """True if at least one piece of `color` has any legal move."""
        for r in range(self.SIZE):
            for c in range(self.SIZE):
                piece = self.grid[r][c]
                if piece and piece.color is color and self.get_piece_moves(r, c):
                    return True
        return False