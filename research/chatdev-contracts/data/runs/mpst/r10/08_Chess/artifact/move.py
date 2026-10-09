'''
move.py
Defines the Move class, a simple record of one chess move used by the
board engine for making, undoing, and describing moves.
'''
class Move:
    """Represents one chess move (start square, end square, and extras)."""
    def __init__(self, start, end, piece, captured=None, promotion=None,
                 is_castle_king_side=False, is_castle_queen_side=False,
                 is_en_passant=False, is_double_push=False):
        self.start = start                  # (row, col) of the moving piece
        self.end = end                      # (row, col) of the destination
        self.piece = piece                  # the Piece object being moved
        self.captured = captured            # Piece object captured, or None
        self.promotion = promotion          # promotion type char ('Q','R','B','N') or None
        self.is_castle_king_side = is_castle_king_side      # O-O
        self.is_castle_queen_side = is_castle_queen_side    # O-O-O
        self.is_en_passant = is_en_passant                  # en passant capture
        self.is_double_push = is_double_push                # pawn moved two squares