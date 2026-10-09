'''
pieces.py
Defines the chess piece classes. Each piece knows its color, its letter,
whether it has moved, and how to generate its pseudo-legal target squares
on a given board. Special moves (castling, en passant, promotion) are
coordinated with the Board class.
'''
class Piece:
    """Base class for all chess pieces."""
    letter = '?'  # single uppercase letter identifying the piece type
    def __init__(self, color):
        self.color = color            # 'w' for white, 'b' for black
        self.has_moved = False        # used for castling rights and pawn double moves
    @property
    def symbol(self):
        """Board symbol: uppercase for white, lowercase for black."""
        return self.letter if self.color == 'w' else self.letter.lower()
    def pseudo_legal_moves(self, board, f, r):
        """Return a list of (file, rank) squares this piece could move to,
        ignoring whether the move leaves the mover's king in check."""
        raise NotImplementedError
    @staticmethod
    def _ray_moves(board, f, r, directions, color):
        """Generate targets along open rays (used by bishop/rook/queen)."""
        targets = []
        for df, dr in directions:
            nf, nr = f + df, r + dr
            while board.in_bounds(nf, nr):
                target = board.get(nf, nr)
                if target is None:
                    targets.append((nf, nr))
                else:
                    if target.color != color:
                        targets.append((nf, nr))
                    break
                nf += df
                nr += dr
        return targets
class Pawn(Piece):
    letter = 'P'
    def pseudo_legal_moves(self, board, f, r):
        targets = []
        step = 1 if self.color == 'w' else -1
        start_rank = 1 if self.color == 'w' else 6
        # Single push
        if board.in_bounds(f, r + step) and board.is_empty(f, r + step):
            targets.append((f, r + step))
            # Double push from the starting rank
            if r == start_rank and board.is_empty(f, r + 2 * step):
                targets.append((f, r + 2 * step))
        # Diagonal captures (including en passant)
        for df in (-1, 1):
            nf, nr = f + df, r + step
            if not board.in_bounds(nf, nr):
                continue
            target = board.get(nf, nr)
            if target is not None and target.color != self.color:
                targets.append((nf, nr))
            elif target is None and board.en_passant_target == (nf, nr):
                targets.append((nf, nr))
        return targets
class Knight(Piece):
    letter = 'N'
    OFFSETS = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))
    def pseudo_legal_moves(self, board, f, r):
        targets = []
        for df, dr in self.OFFSETS:
            nf, nr = f + df, r + dr
            if board.in_bounds(nf, nr):
                target = board.get(nf, nr)
                if target is None or target.color != self.color:
                    targets.append((nf, nr))
        return targets
class Bishop(Piece):
    letter = 'B'
    DIRECTIONS = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    def pseudo_legal_moves(self, board, f, r):
        return self._ray_moves(board, f, r, self.DIRECTIONS, self.color)
class Rook(Piece):
    letter = 'R'
    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    def pseudo_legal_moves(self, board, f, r):
        return self._ray_moves(board, f, r, self.DIRECTIONS, self.color)
class Queen(Piece):
    letter = 'Q'
    DIRECTIONS = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
    def pseudo_legal_moves(self, board, f, r):
        return self._ray_moves(board, f, r, self.DIRECTIONS, self.color)
class King(Piece):
    letter = 'K'
    DIRECTIONS = ((1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
    def pseudo_legal_moves(self, board, f, r):
        targets = []
        for df, dr in self.DIRECTIONS:
            nf, nr = f + df, r + dr
            if board.in_bounds(nf, nr):
                target = board.get(nf, nr)
                if target is None or target.color != self.color:
                    targets.append((nf, nr))
        # Castling targets are appended by the Board (needs rook & attack checks).
        targets.extend(board.castling_targets(self.color))
        return targets