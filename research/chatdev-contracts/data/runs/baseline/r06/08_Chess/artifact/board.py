'''Board representation and attack detection.'''
from pieces import ...
class Board:
    def __init__(self):
        self.grid = [[None]*8 for _ in range(8)]
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None
        self.setup_initial_position()
    def setup_initial_position(self): ...
    def get(self, r, c): return self.grid[r][c]
    def set(self, r, c, piece): self.grid[r][c] = piece
    @staticmethod
    def in_bounds(r,c)
    def is_attacked(self, r, c, by_color): ...
    def find_king(self, color): ...
    def copy(self): deep-ish copy (pieces are immutable-ish; but promotion replaces piece, so sharing piece objects is fine as long as we never mutate a Piece in place — we don't). So copy = new Board without setup, grid rows copied (piece references shared), castling_rights copied, ep target copied.