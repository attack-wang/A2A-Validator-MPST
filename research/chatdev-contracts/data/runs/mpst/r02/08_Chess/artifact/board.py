'''Board representation, move execution, and rule enforcement.'''
from pieces import Pawn, Knight, Bishop, Rook, Queen, King
from move import Move
class Board:
    def __init__(self):
        self.grid = [[None] * 8 for _ in range(8)]
        self.turn = 'w'
        self.castling_rights = {'w': {'K': True, 'Q': True},
                                'b': {'K': True, 'Q': True}}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []
        self.position_counts = {}
    def setup(self):
        ... (as given)
    def get_piece(self, row, col): ...
    def find_king(self, color): ...
    def is_square_attacked(self, row, col, by_color): ... (as given)
    def is_in_check(self, color): ... (as given)
    def pseudo_legal_moves(self, color=None):
        """All pseudo-legal moves for color (castling included)."""
        if color is None:
            color = self.turn
        moves = []
        for r in range(8):
            for c in range(8):
                piece = self.grid[r][c]
                if piece is not None and piece.color == color:
                    for (tr, tc) in piece.pseudo_legal_moves(self, r, c):
                        target = self.grid[tr][tc]
                        is_ep = False
                        captured = target
                        if piece.kind == 'P' and target is None and tc != c and self.en_passant_target == (tr, tc):
                            is_ep = True
                            captured = self.grid[r][tc]
                        moves.append(Move((r, c), (tr, tc), piece, captured, is_en_passant=is_ep))
                    if piece.kind == 'K':
                        moves.extend(self._castling_moves(r, c))
        return moves