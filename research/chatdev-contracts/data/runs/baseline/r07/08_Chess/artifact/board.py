'''
Board representation for the chess game.
The Board stores an 8x8 grid of Piece objects (or None), knows how to set
up the standard initial position, locate kings, test square attacks, and
render itself in Unicode or ASCII art for the terminal.
'''
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
class Board:
    """8x8 chess board; row 0 is rank 1 (White's back rank), row 7 is rank 8."""
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup()
    def setup(self):
        """Place all pieces on the standard starting squares."""
        back = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col in range(8):
            self.grid[0][col] = back[col]('w')
            self.grid[1][col] = Pawn('w')
            self.grid[6][col] = Pawn('b')
            self.grid[7][col] = back[col]('b')
    @staticmethod
    def in_bounds(r, c):
        """True if (r, c) lies on the board."""
        return 0 <= r < 8 and 0 <= c < 8
    def get(self, r, c):
        """Return the piece on (r, c) or None."""
        if self.in_bounds(r, c):
            return self.grid[r][c]
        return None
    def set(self, r, c, piece):
        """Place a piece on (r, c)."""
        if self.in_bounds(r, c):
            self.grid[r][c] = piece
    def find_king(self, color):
        """Return the (row, col) of the given color's king, or None."""
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if isinstance(piece, King) and piece.color == color:
                    return (r, c)
        return None
    def is_attacked(self, r, c, by_color):
        """True if square (r, c) is attacked by any piece of by_color."""
        # Pawn attacks
        pawn_row = r + (1 if by_color == 'w' else -1)
        for dc in (-1, 1):
            if self.in_bounds(pawn_row, c + dc):
                p = self.grid[pawn_row][c + dc]
                if isinstance(p, Pawn) and p.color == by_color:
                    return True
        # Knight attacks
        for dr, dc in Knight.OFFSETS:
            rr, cc = r + dr, c + dc
            if self.in_bounds(rr, cc):
                p = self.grid[rr][cc]
                if isinstance(p, Knight) and p.color == by_color:
                    return True
        # King adjacency
        for dr, dc in King.STEPS:
            rr, cc = r + dr, c + dc
            if self.in_bounds(rr, cc):
                p = self.grid[rr][cc]
                if isinstance(p, King) and p.color == by_color:
                    return True
        # Sliding attacks: rook/queen along orthogonal, bishop/queen along diagonal
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            rr, cc = r + dr, c + dc
            while self.in_bounds(rr, cc):
                p = self.grid[rr][cc]
                if p is not None:
                    if p.color == by_color and isinstance(p, (Rook, Queen)):
                        return True
                    break
                rr += dr
                cc += dc
        for dr, dc in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
            rr, cc = r + dr, c + dc
            while self.in_bounds(rr, cc):
                p = self.grid[rr][cc]
                if p is not None:
                    if p.color == by_color and isinstance(p, (Bishop, Queen)):
                        return True
                    break
                rr += dr
                cc += dc
        return False