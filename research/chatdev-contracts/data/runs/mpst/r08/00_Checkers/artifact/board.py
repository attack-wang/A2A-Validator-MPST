'''
board.py
Board class: 8x8 grid, setup, move generation, execution, display.
'''
from piece import Piece
from move import Move
class Board:
    """The 8x8 checkers board with pieces, move generation and execution."""
    SIZE = 8
    COLS = "abcdefgh"
    def __init__(self):
        """Create the grid and set up the standard starting position."""
        self.grid = [[None] * Board.SIZE for _ in range(Board.SIZE)]
        self._setup_starting_position()
    def _setup_starting_position(self):
        """BLACK occupies the top three ranks, RED the bottom three."""
        for row in range(3):
            for col in range(Board.SIZE):
                if self.is_dark_square(row, col):
                    self.grid[row][col] = Piece(Piece.BLACK)
        for row in range(5, Board.SIZE):
            for col in range(Board.SIZE):
                if self.is_dark_square(row, col):
                    self.grid[row][col] = Piece(Piece.RED)
    @staticmethod
    def is_dark_square(row, col):
        """True for the playable (dark) squares where pieces live."""
        return (row + col) % 2 == 0
    @staticmethod
    def in_bounds(row, col):
        """True if (row, col) lies on the board."""
        return 0 <= row < Board.SIZE and 0 <= col < Board.SIZE
    def get_piece(self, row, col):
        """Return the piece on a square, or None if empty/out of bounds."""
        if not self.in_bounds(row, col):
            return None
        return self.grid[row][col]
    def place_piece(self, piece, row, col):
        """Place an existing piece on an in-bounds square."""
        if not self.in_bounds(row, col):
            raise ValueError(f"Square ({row}, {col}) is off the board.")
        self.grid[row][col] = piece
    def remove_piece(self, row, col):
        """Clear a square and return the piece that was there (or None)."""
        piece = self.get_piece(row, col)
        self.grid[row][col] = None
        return piece
    def _forward_directions(self, piece):
        """Diagonal directions this piece may move: men go forward only,
        kings go in all four diagonal directions."""
        if piece.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if piece.color == Piece.BLACK:
            return [(1, -1), (1, 1)]  # BLACK moves toward increasing rows
        return [(-1, -1), (-1, 1)]    # RED moves toward decreasing rows
    def get_simple_moves(self, row, col):
        """All non-capturing diagonal steps for the piece at (row, col)."""
        piece = self.get_piece(row, col)
        if piece is None:
            return []
        moves = []
        for dr, dc in self._forward_directions(piece):
            r2, c2 = row + dr, col + dc
            if self.in_bounds(r2, c2) and self.grid[r2][c2] is None:
                moves.append(Move((row, col), (r2, c2)))
        return moves
    def get_jump_moves(self, row, col):
        """All single jumps (over one enemy piece to an empty square)."""
        piece = self.get_piece(row, col)
        if piece is None:
            return []
        moves = []
        for dr, dc in self._forward_directions(piece):
            mid = (row + dr, col + dc)
            dest = (row + 2 * dr, col + 2 * dc)
            if self.in_bounds(*dest):
                mid_piece = self.grid[mid[0]][mid[1]]
                if (mid_piece is not None and mid_piece.color != piece.color
                        and self.grid[dest[0]][dest[1]] is None):
                    moves.append(Move((row, col), dest, captured=mid))
        return moves
    def get_moves_for_piece(self, row, col, captures_only=False):
        """Moves for one piece; with captures_only=True only jumps are returned
        (used to enforce multi-jump continuation)."""
        jumps = self.get_jump_moves(row, col)
        if captures_only:
            return jumps
        return jumps if jumps else self.get_simple_moves(row, col)
    def get_all_moves(self, color):
        """All legal moves for a color. Forced capture: if any jump exists,
        only jumps are legal this turn."""
        all_jumps = []
        all_simple = []
        for (row, col), _piece in self.iter_pieces(color):
            all_jumps.extend(self.get_jump_moves(row, col))
            all_simple.extend(self.get_simple_moves(row, col))
        return all_jumps if all_jumps else all_simple
    def has_capture(self, color):
        """True if any piece of this color can jump right now."""
        for (row, col), _piece in self.iter_pieces(color):
            if self.get_jump_moves(row, col):
                return True
        return False
    def iter_pieces(self, color=None):
        """Yield ((row, col), piece) for every piece (optionally one color)."""
        for row in range(Board.SIZE):
            for col in range(Board.SIZE):
                p = self.grid[row][col]
                if p is not None and (color is None or p.color == color):
                    yield (row, col), p
    def execute_move(self, move):
        """Apply a legal move; returns {'captured_piece', 'promoted'}.
        A man reaching its last rank is crowned and ends the turn."""
        sr, sc = move.start
        er, ec = move.destination
        piece = self.grid[sr][sc]
        self.grid[sr][sc] = None
        self.grid[er][ec] = piece
        captured_piece = None
        if move.captured:
            cr, cc = move.captured
            captured_piece = self.grid[cr][cc]
            self.grid[cr][cc] = None
        promoted = False
        if not piece.is_king:
            if (piece.color == Piece.BLACK and er == Board.SIZE - 1) or \
               (piece.color == Piece.RED and er == 0):
                piece.promote()
                promoted = True
        return {"captured_piece": captured_piece, "promoted": promoted}
    def count_pieces(self, color):
        """Number of pieces (men + kings) of the given color."""
        return sum(1 for _pos, _p in self.iter_pieces(color))
    def __str__(self):
        """Render the board with a-h / 1-8 coordinates matching the notation."""
        lines = ["   a b c d e f g h"]
        for row in range(Board.SIZE - 1, -1, -1):  # rank 8 on top, rank 1 at bottom
            cells = []
            for col in range(Board.SIZE):
                p = self.grid[row][col]
                cells.append(p.symbol if p else ".")
            lines.append(f" {row + 1} " + " ".join(cells))
        return "\n".join(lines)