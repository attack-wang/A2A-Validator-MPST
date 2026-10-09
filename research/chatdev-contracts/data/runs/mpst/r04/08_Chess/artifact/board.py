'''
board.py
Chess board representation and full rules engine:
- piece movement generation (pseudo-legal + legal filtering)
- check / checkmate / stalemate detection
- castling (with through-check verification)
- en passant
- pawn promotion
- make_move / undo_move with complete state restoration
- draw detection helpers (50-move rule, threefold repetition)
'''
from pieces import Piece
from move import Move
# Direction vectors
KNIGHT_DELTAS = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
BISHOP_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
ROOK_DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
KING_DIRS = BISHOP_DIRS + ROOK_DIRS
class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.setup_initial_position()
        self.turn = 'W'
        self.castling_rights = {'W': {'K': True, 'Q': True}, 'B': {'K': True, 'Q': True}}
        self.en_passant_target = None  # (row, col) or None
        self.halfmove_clock = 0
        self.move_history = []
        self.position_counts = {}  # for threefold repetition
    def setup_initial_position(self):
        back = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        for c in range(8):
            self.grid[0][c] = Piece('B', back[c])
            self.grid[1][c] = Piece('B', 'P')
            self.grid[6][c] = Piece('W', 'P')
            self.grid[7][c] = Piece('W', back[c])
    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return None
    def find_king(self, color):
        for r in range(8):
            for c in range(8):
                p = self.grid[r][c]
                if p and p.color == color and p.type == 'K':
                    return (r, c)
        return None
    def is_attacked(self, row, col, by_color):
        """Is square (row, col) attacked by any piece of by_color?"""
        # Pawn attacks
        pr = row + (1 if by_color == 'W' else -1)
        # White pawns attack upward (toward row-1); a white pawn on (pr, pc) attacks (pr-1, pc±1)
        ...