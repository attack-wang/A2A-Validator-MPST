'''
board.py
Defines the Board: an 8x8 grid holding Piece objects, plus helpers for
setting up the initial position, querying squares, detecting attacks,
locating kings and copying the position.
'''
from piece import Pawn, Knight, Bishop, Rook, Queen, King
class Board:
    """An 8x8 chess board. Row 0 is rank 8 (Black's back rank), row 7 is
    rank 1 (White's back rank); column 0 is file 'a', column 7 is file 'h'."""
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup()
    def setup(self):
        """Place all 32 pieces on their starting squares."""
        back = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        # White pieces
        for c, cls in enumerate(back):
            self.grid[7][c] = cls('w')
            self.grid[6][c] = Pawn('w')
        # Black pieces
        for c, cls in enumerate(back):
            self.grid[0][c] = cls('b')
            self.grid[1][c] = Pawn('b')
    def get(self, row, col):
        """Return the piece at (row, col) or None if empty/off-board."""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return None
    def set(self, row, col, piece):
        """Place `piece` (or None) at (row, col)."""
        self.grid[row][col] = piece
    def is_attacked(self, row, col, by_color):
        """Return True if square (row, col) is attacked by any piece of
        `by_color` in the current position."""
        # Pawn attacks: a white pawn on (row+1, col±1) attacks (row, col);
        # a black pawn on (row-1, col±1) attacks (row, col).
        dr = 1 if by_color == 'w' else -1
        for dc in (-1, 1):
            r, c = row + dr, col + dc
            p = self.get(r, c)
            if isinstance(p, Pawn) and p.color == by_color:
                return True
        # Knight attacks
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]:
            p = self.get(row + dr, col + dc)
            if isinstance(p, Knight) and p.color == by_color:
                return True
        # King attacks (adjacent squares)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                p = self.get(row + dr, col + dc)
                if isinstance(p, King) and p.color == by_color:
                    return True
        # Sliding pieces: rook/queen along ranks & files, bishop/queen
        # along diagonals.
        for dr, dc, kinds in ((-1, 0, (Rook, Queen)), (1, 0, (Rook, Queen)),
                              (0, -1, (Rook, Queen)), (0, 1, (Rook, Queen)),
                              (-1, -1, (Bishop, Queen)), (-1, 1, (Bishop, Queen)),
                              (1, -1, (Bishop, Queen)), (1, 1, (Bishop, Queen))):
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                p = self.grid[r][c]
                if p is not None:
                    if p.color == by_color and isinstance(p, kinds):
                        return True
                    break
                r += dr
                c += dc
        return False
    def find_king(self, color):
        """Return the (row, col) of `color`'s king, or None (should never
        happen in a legal position)."""
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if isinstance(p, King) and p.color == color:
                    return (r, c)
        return None
    def copy(self):
        """Return a deep-ish copy of the board (new Piece objects)."""
        new = Board.__new__(Board)
        new.grid = []
        for r in range(8):
            row = []
            for c in range(8):
                p = self.grid[r][c]
                if p is None:
                    row.append(None)
                else:
                    q = object.__new__(type(p))
                    q.color = p.color
                    row.append(q)
            new.grid.append(row)
        return new