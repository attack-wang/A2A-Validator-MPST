'''
board.py
Board representation for the checkers game: an 8x8 grid in which only
the 32 dark squares are playable.  The board owns the Piece objects,
knows how to place / move / remove them, how to crown kings and how to
render itself as an ASCII diagram with algebraic coordinates.
'''
from piece import Piece, PieceColor
BOARD_SIZE = 8
class Board:
    """The 8x8 checkers board and the pieces standing on it."""
    def __init__(self):
        self.setup_initial_position()
    # -- square helpers ------------------------------------------------
    @staticmethod
    def is_inside(row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE
    @staticmethod
    def is_playable(row, col):
        """Only the dark squares (where row+col is odd) are playable."""
        return Board.is_inside(row, col) and (row + col) % 2 == 1
    def get_piece(self, row, col):
        if not self.is_inside(row, col):
            return None
        return self._grid[row][col]
    def is_empty(self, row, col):
        return self.is_inside(row, col) and self._grid[row][col] is None
    # -- setup ----------------------------------------------------------
    def setup_initial_position(self):
        """Place 12 black men on the top three ranks and 12 red men on the bottom three."""
        self._grid = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self.is_playable(row, col):
                    continue
                if row <= 2:
                    self._grid[row][col] = Piece(PieceColor.BLACK)
                elif row >= 5:
                    self._grid[row][col] = Piece(PieceColor.RED)
    # -- iteration ------------------------------------------------------
    def _pieces_of(self, color):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self._grid[row][col]
                if piece is not None and piece.color is color:
                    yield row, col, piece
    def piece_count(self, color):
        return sum(1 for _ in self._pieces_of(color))
    # -- mutation -------------------------------------------------------
    def place_piece(self, piece, row, col):
        if not self.is_playable(row, col):
            raise ValueError(f"({row}, {col}) is not a playable dark square.")
        self._grid[row][col] = piece
    def remove_piece(self, row, col):
        self._grid[row][col] = None
    def move_piece(self, from_sq, to_sq):
        fr, fc = from_sq
        tr, tc = to_sq
        self._grid[tr][tc] = self._grid[fr][fc]
        self._grid[fr][fc] = None
    def crown_if_needed(self, row, col):
        """Crown the piece on (row, col) if it reached its back rank. Returns True if crowned."""
        piece = self._grid[row][col]
        if piece is None or piece.is_king:
            return False
        if (piece.color is PieceColor.RED and row == 0) or \
           (piece.color is PieceColor.BLACK and row == 7):
            piece.crown()
            return True
        return False
    # -- rendering ------------------------------------------------------
    def render(self):
        """Return the board as an ASCII diagram with algebraic coordinates."""
        lines = []
        header = '    ' + '   '.join(chr(ord('a') + c) for c in range(BOARD_SIZE))
        lines.append(header)
        lines.append('  +' + '---+' * BOARD_SIZE)
        for row in range(BOARD_SIZE):
            cells = []
            for col in range(BOARD_SIZE):
                piece = self._grid[row][col]
                if piece is None:
                    cells.append(' ' if self.is_playable(row, col) else '.')
                else:
                    cells.append(str(piece))
            rank = 8 - row
            lines.append(f"{rank} | " + ' | '.join(cells) + ' |')
            lines.append('  +' + '---+' * BOARD_SIZE)
        return '\n'.join(lines)
    def __str__(self):
        return self.render()