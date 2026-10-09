'''Piece definitions and movement logic for the chess game.'''
class Piece:
    """Base class for all chess pieces."""
    def __init__(self, color, kind):
        self.color = color          # 'w' or 'b'
        self.kind = kind            # 'P', 'N', 'B', 'R', 'Q', 'K'
        self.has_moved = False
    @property
    def symbol(self):
        symbols = {'w': {'K': 'K', 'Q': 'Q', 'R': 'R', 'B': 'B', 'N': 'N', 'P': 'P'},
                   'b': {'K': 'k', 'Q': 'q', 'R': 'r', 'B': 'b', 'N': 'n', 'P': 'p'}}
        return symbols[self.color][self.kind]
    def pseudo_legal_moves(self, board, row, col):
        raise NotImplementedError
    def copy(self):
        if type(self) is Piece:
            clone = Piece(self.color, self.kind)
        else:
            clone = type(self)(self.color)
        clone.has_moved = self.has_moved
        return clone
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'P')
    def pseudo_legal_moves(self, board, row, col):
        moves = []
        direction = -1 if self.color == 'w' else 1
        start_row = 6 if self.color == 'w' else 1
        r = row + direction
        if 0 <= r < 8 and board.get_piece(r, col) is None:
            moves.append((r, col))
            r2 = row + 2 * direction
            if row == start_row and board.get_piece(r2, col) is None:
                moves.append((r2, col))
        for dc in (-1, 1):
            c = col + dc
            r = row + direction
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece(r, c)
                if target is not None and target.color != self.color:
                    moves.append((r, c))
                elif target is None and board.en_passant_target == (r, c):
                    moves.append((r, c))
        return moves
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'N')
    def pseudo_legal_moves(self, board, row, col):
        offsets = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        moves = []
        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece(r, c)
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'B')
    def pseudo_legal_moves(self, board, row, col):
        return self._slide(board, row, col, ((-1,-1),(-1,1),(1,-1),(1,1)))
    def _slide(self, board, row, col, directions):
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece(r, c)
                if target is None:
                    moves.append((r, c))
                else:
                    if target.color != self.color:
                        moves.append((r, c))
                    break
                r += dr
                c += dc
        return moves
class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'R')
    def pseudo_legal_moves(self, board, row, col):
        return self._slide(board, row, col, ((-1,0),(1,0),(0,-1),(0,1)))
    def _slide(self, ...): same
class Queen(Piece):
    ... both directions
class King(Piece):
    ... single steps (castling handled at board level)