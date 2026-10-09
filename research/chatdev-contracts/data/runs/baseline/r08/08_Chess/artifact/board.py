'''
board.py
Board representation, initial setup, attack detection and terminal display.
Internal coordinates: row 0 is rank 8 (Black's back rank, top of the printed
board), row 7 is rank 1 (White's back rank). Column 0 is file 'a'.
'''
from pieces import Piece
WHITE = 'w'
BLACK = 'b'
FILE_CHARS = 'abcdefgh'
def opposite(color):
    return BLACK if color == WHITE else WHITE
class Board:
    """8x8 chess board holding Piece objects (or None) in a grid."""
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup_initial_position()
    def setup_initial_position(self):
        """Place the 32 pieces on their standard starting squares."""
        back_rank = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        self.grid = [[None] * 8 for _ in range(8)]
        for col in range(8):
            self.grid[0][col] = Piece(BLACK, back_rank[col])
            self.grid[1][col] = Piece(BLACK, 'P')
            self.grid[6][col] = Piece(WHITE, 'P')
            self.grid[7][col] = Piece(WHITE, back_rank[col])
    def get_piece(self, row, col):
        return self.grid[row][col]
    def set_piece(self, row, col, piece):
        self.grid[row][col] = piece
    def in_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    def find_king(self, color):
        """Return (row, col) of the given color's king, or None."""
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece and piece.color == color and piece.piece_type == 'K':
                    return (row, col)
        return None
    def is_square_attacked(self, row, col, by_color):
        """True if square (row, col) is attacked by any piece of by_color."""
        # Pawn attacks: a white pawn on (r+1, c±1) attacks (r, c);
        # a black pawn on (r-1, c±1) attacks (r, c).
        pawn_row = row + 1 if by_color == WHITE else row - 1
        for dc in (-1, 1):
            r, c = pawn_row, col + dc
            if self.in_bounds(r, c):
                piece = self.grid[r][c]
                if piece and piece.color == by_color and piece.piece_type == 'P':
                    return True
        # Knight attacks
        knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                          (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in knight_offsets:
            r, c = row + dr, col + dc
            if self.in_bounds(r, c):
                piece = self.grid[r][c]
                if piece and piece.color == by_color and piece.piece_type == 'N':
                    return True
        # King adjacency (used for illegal king-adjacency and attack tests)
        king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                        (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_offsets:
            r, c = row + dr, col + dc
            if self.in_bounds(r, c):
                piece = self.grid[r][c]
                if piece and piece.color == by_color and piece.piece_type == 'K':
                    return True
        # Sliding pieces: rook/queen on orthogonal rays, bishop/queen on diagonals
        orthogonal = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        diagonal = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for rays, types in ((orthogonal, ('R', 'Q')), (diagonal, ('B', 'Q'))):
            for dr, dc in rays:
                r, c = row + dr, col + dc
                while self.in_bounds(r, c):
                    piece = self.grid[r][c]
                    if piece is not None:
                        if piece.color == by_color and piece.piece_type in types:
                            return True
                        break  # any piece blocks the ray
                    r += dr
                    c += dc
        return False
    def display(self, unicode_mode=True):
        """Return a list of printable lines showing the board with coordinates."""
        lines = []
        header = '   ' + '  '.join(FILE_CHARS)  # hmm spacing
        ...