'''
Piece definitions for the chess game.
Contains the abstract base class Piece and the six concrete piece types
(Pawn, Knight, Bishop, Rook, Queen, King). Each piece knows its color,
its SAN letter, its material value, its Unicode/ASCII symbols, and how to
generate its pseudo-legal moves from a given square.
'''
from move import Move
class Piece:
    """Base class for all chess pieces."""
    def __init__(self, color):
        self.color = color  # 'w' for white, 'b' for black
    @property
    def name(self):
        return type(self).__name__
    @property
    def letter(self):
        """Uppercase letter used in SAN (empty string for a pawn)."""
        return ''
    @property
    def value(self):
        """Classical material value in pawns, for insufficient-material tests."""
        return 0
    def unicode_symbol(self):
        raise NotImplementedError
    def ascii_symbol(self):
        raise NotImplementedError
    def pseudo_legal_moves(self, board, row, col, game):
        """Generate pseudo-legal moves for this piece from (row, col)."""
        return []
    def _sliding_moves(self, board, row, col, directions):
        """Helper shared by Bishop/Rook/Queen: ray moves in given directions."""
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.in_bounds(r, c):
                target = board.grid[r][c]
                if target is None:
                    moves.append(Move((row, col), (r, c)))
                else:
                    if target.color != self.color:
                        moves.append(Move((row, col), (r, c), captured=target))
                    break
                r += dr
                c += dc
        return moves
    def __repr__(self):
        return "<{} {}>".format(self.color, self.name)
class Pawn(Piece):
    """Pawn: forward moves, double push, diagonal captures, en passant."""
    @property
    def letter(self):
        return ''
    @property
    def value(self):
        return 1
    def unicode_symbol(self):
        return '\u2659' if self.color == 'w' else '\u265F'
    def ascii_symbol(self):
        return 'P' if self.color == 'w' else 'p'
    def pseudo_legal_moves(self, board, row, col, game):
        moves = []
        direction = -1 if self.color == 'w' else 1
        start_row = 6 if self.color == 'w' else 1
        promo_row = 0 if self.color == 'w' else 7
        r1 = row + direction
        # Forward one (and double push from the start rank)
        if board.in_bounds(r1, col) and board.grid[r1][col] is None:
            moves.append(Move((row, col), (r1, col),
                              promotion_needed=(r1 == promo_row)))
            r2 = row + 2 * direction
            if row == start_row and board.grid[r2][col] is None:
                moves.append(Move((row, col), (r2, col), is_double_push=True))
        # Diagonal captures and en passant
        for dc in (-1, 1):
            c1 = col + dc
            if not (board.in_bounds(r1, c1)):
                continue
            target = board.grid[r1][c1]
            if target is not None and target.color != self.color:
                moves.append(Move((row, col), (r1, c1), captured=target,
                                  promotion_needed=(r1 == promo_row)))
            elif target is None and game.en_passant_target == (r1, c1):
                moves.append(Move((row, col), (r1, c1), is_en_passant=True))
        return moves