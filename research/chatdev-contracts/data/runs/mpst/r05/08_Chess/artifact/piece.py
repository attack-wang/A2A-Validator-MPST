'''
piece.py
Defines the Piece base class and all six chess piece types.
Each piece knows its color and can generate its pseudo-legal moves
(moves that follow the piece's movement pattern but ignore whether
the mover's own king ends up in check; legality filtering happens
in game.py).
'''
class Piece:
    """Base class for all chess pieces."""
    letter = ''  # one-letter identifier: 'P', 'N', 'B', 'R', 'Q', 'K'
    def __init__(self, color):
        self.color = color  # 'w' for White, 'b' for Black
    def char(self):
        """Return the display character: uppercase for White, lowercase for Black."""
        return self.letter.upper() if self.color == 'w' else self.letter.lower()
    def pseudo_moves(self, board, row, col, ep_square=None):
        """Return a list of (row, col) destination squares reachable by this
        piece from (row, col) ignoring check restrictions."""
        raise NotImplementedError
    @staticmethod
    def _sliding(board, row, col, directions):
        """Helper: generate destinations along the given (dr, dc) directions
        until blocked."""
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.get(r, c)
                if target is None:
                    moves.append((r, c))
                else:
                    if target.color != board.get(row, col).color:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        return moves
class Pawn(Piece):
    letter = 'P'
    def pseudo_moves(self, board, row, col, ep_square=None):
        moves = []
        direction = -1 if self.color == 'w' else 1
        start_row = 6 if self.color == 'w' else 1
        # Forward one
        r = row + direction
        if 0 <= r < 8 and board.get(r, col) is None:
            moves.append((r, col))
            # Forward two (only from the starting rank, both squares empty)
            r2 = row + 2 * direction
            if row == start_row and board.get(r2, col) is None:
                moves.append((r2, col))
        # Captures (including en passant)
        for dc in (-1, 1):
            c = col + dc
            if 0 <= c < 8:
                target = board.get(r, c)
                if target is not None and target.color != self.color:
                    moves.append((r, c))
                elif ep_square is not None and ep_square == (r, c):
                    moves.append((r, c))
        return moves
class Knight(Piece):
    letter = 'N'
    def pseudo_moves(self, board, row, col, ep_square=None):
        moves = []
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get(r, c)
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves
class Bishop(Piece):
    letter = 'B'
    def pseudo_moves(self, board, row, col, ep_square=None):
        return self._sliding(board, row, col,
                             [(-1, -1), (-1, 1), (1, -1), (1, 1)])
class Rook(Piece):
    letter = 'R'
    def pseudo_moves(self, board, row, col, ep_square=None):
        return self._sliding(board, row, col,
                             [(-1, 0), (1, 0), (0, -1), (0, 1)])
class Queen(Piece):
    letter = 'Q'
    def pseudo_moves(self, board, row, col, ep_square=None):
        return self._sliding(board, row, col,
                             [(-1, -1), (-1, 1), (1, -1), (1, 1),
                              (-1, 0), (1, 0), (0, -1), (0, 1)])
class King(Piece):
    letter = 'K'
    def pseudo_moves(self, board, row, col, ep_square=None):
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board.get(r, c)
                    if target is None or target.color != self.color:
                        moves.append((r, c))
        return moves
PIECE_CLASSES = {
    'P': Pawn, 'N': Knight, 'B': Bishop,
    'R': Rook, 'Q': Queen, 'K': King,
}
def make_piece(letter, color):
    """Factory: create a piece instance from a letter and color."""
    return PIECE_CLASSES[letter.upper()](color)