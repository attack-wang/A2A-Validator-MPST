"""
pieces.py
Chess piece definitions for the terminal chess game.
Each piece knows its color, its letter (used in algebraic notation and
ASCII rendering), its unicode glyph, and how to generate its pseudo-legal
moves on a given board.  Pseudo-legal moves are later filtered by the
Game class so that a player never makes a move that leaves their own
king in check.
"""
WHITE = 'w'
BLACK = 'b'
def opponent(color):
    """Return the opposite color of the given color ('w' or 'b')."""
    return BLACK if color == WHITE else WHITE
class Piece:
    """Abstract base class for every chess piece."""
    value = 0        # relative material value (informational)
    letter = ''      # uppercase SAN letter ('' for pawns)
    def __init__(self, color):
        self.color = color
    # -- rendering helpers -------------------------------------------------
    @property
    def glyph(self):
        """Unicode chess glyph for this piece."""
        raise NotImplementedError
    @property
    def ascii_char(self):
        """Single ASCII character representing this piece."""
        return self.letter.upper() if self.color == WHITE else self.letter.lower()
    # -- move generation ----------------------------------------------------
    def pseudo_moves(self, board, row, col, game):
        """
        Return a list of (row, col) tuples this piece could move to,
        ignoring whether the move leaves the mover's king in check.
        """
        raise NotImplementedError
    def __repr__(self):
        return f'<{type(self).__name__} {self.color}>'
def _slide(board, row, col, directions):
    """Generate ray moves (used by rook/bishop/queen)."""
    color = board.get_piece(row, col).color
    moves = []
    for drow, dcol in directions:
        r, c = row + drow, col + dcol
        while 0 <= r < 8 and 0 <= c < 8:
            target = board.get_piece(r, c)
            if target is None:
                moves.append((r, c))
            elif target.color != color:
                moves.append((r, c))
                break
            else:
                break
            r += drow
            c += dcol
    return moves
class Rook(Piece):
    """Rook: slides along ranks and files."""
    value = 5
    letter = 'R'
    @property
    def glyph(self):
        return '♖' if self.color == WHITE else '♜'
    def pseudo_moves(self, board, row, col, game):
        return _slide(board, row, col, ((1, 0), (-1, 0), (0, 1), (0, -1)))
class Bishop(Piece):
    value = 3
    letter = 'B'
    @property
    def glyph(self):
        return '♗' if self.color == WHITE else '♝'
    def pseudo_moves(self, board, row, col, game):
        return _slide(board, row, col, ((1, 1), (1, -1), (-1, 1), (-1, -1)))
class Queen(Piece):
    value = 9
    letter = 'Q'
    @property
    def glyph(self):
        return '♕' if self.color == WHITE else '♛'
    def pseudo_moves(self, board, row, col, game):
        return _slide(board, row, col, ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)))
class Knight(Piece):
    value = 3
    letter = 'N'
    @property
    def glyph(self):
        return '♘' if self.color == WHITE else '♞'
    def pseudo_moves(self, board, row, col, game):
        offsets = ((2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2))
        moves = []
        color = self.color
        for dr, dc in offsets:
            r, c = row+dr, col+dc
            if 0 <= r < 8 and 0 <= c < 8:
                t = board.get_piece(r, c)
                if t is None or t.color != color:
                    moves.append((r, c))
        return moves
class King(Piece):
    value = 0  # king can't be captured
    letter = 'K'
    @property
    def glyph(self):
        return '♔' if self.color == WHITE else '♚'
    def pseudo_moves(self, board, row, col, game):
        moves = []
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row+dr, col+dc
                if 0 <= r < 8 and 0 <= c < 8:
                    t = board.get_piece(r, c)
                    if t is None or t.color != self.color:
                        moves.append((r, c))
        # Castling (requires game state: rights + attack info)
        home = 7 if self.color == WHITE else 0
        if row == home and col == 4:
            enemy = opponent(self.color)
            rights = game.castling_rights.get(self.color, {})
            king_side = rights.get('K', False)
            queen_side = rights.get('Q', False)
            if king_side:
                rook = board.get_piece(home, 7)
                if (isinstance(rook, Rook) and rook.color == self.color
                        and board.get_piece(home, 5) is None
                        and board.get_piece(home, 6) is None
                        and not board.is_attacked(home, 4, enemy)
                        and not board.is_attacked(home, 5, enemy)
                        and not board.is_attacked(home, 6, enemy)):
                    moves.append((home, 6))
            if queen_side:
                rook = board.get_piece(home, 0)
                if (isinstance(rook, Rook) and rook.color == self.color
                        and board.get_piece(home, 1) is None
                        and board.get_piece(home, 2) is None
                        and board.get_piece(home, 3) is None
                        and not board.is_attacked(home, 4, enemy)
                        and not board.is_attacked(home, 3, enemy)
                        and not board.is_attacked(home, 2, enemy)):
                    moves.append((home, 2))
        return moves
class Pawn(Piece):
    value = 1
    letter = ''
    @property
    def glyph(self):
        return '♙' if self.color == WHITE else '♟'
    def pseudo_moves(self, board, row, col, game):
        moves = []
        step = -1 if self.color == WHITE else 1
        start_row = 6 if self.color == WHITE else 1
        # one square forward
        r = row + step
        if 0 <= r < 8 and board.get_piece(r, col) is None:
            moves.append((r, col))
            # two squares forward from the starting rank
            if row == start_row:
                r2 = row + 2 * step
                if board.get_piece(r2, col) is None:
                    moves.append((r2, col))
        # diagonal captures (incl. en passant)
        for dc in (-1, 1):
            r = row + step
            c = col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece(r, c)
                if target is not None and target.color != self.color:
                    moves.append((r, c))
                elif target is None and game.en_passant_target == (r, c):
                    moves.append((r, c))
        return moves
def make_piece(letter, color):
    """Factory: build a piece object from its SAN letter and color."""
    letter = letter.upper()
    if letter == 'K': return King(color)
    if letter == 'Q': return Queen(color)
    if letter == 'R': return Rook(color)
    if letter == 'B': return Bishop(color)
    if letter == 'N': return Knight(color)
    if letter == 'P': return Pawn(color)
    raise ValueError(f'unknown piece letter: {letter}')