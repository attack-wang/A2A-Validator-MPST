'''
game.py
ChessGame: turn management, pseudo-legal move generation, legality
filtering via make/undo simulation, castling/en-passant/promotion state,
SAN generation, and game-over detection (checkmate, stalemate, 50-move,
threefold repetition, insufficient material, resignation).
'''
from pieces import Piece
from move import Move
from board import Board, coords_to_square, square_to_coords
def opponent(color):
    return 'b' if color == 'w' else 'w'
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.turn = 'w'
        self.castling_rights = {
            'w': {'K': True, 'Q': True},
            'b': {'K': True, 'Q': True},
        }
        self.en_passant_target = None  # (row, col) of the square that can be captured "onto"
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []  # list of Move
        self.san_history = []   # list of SAN strings
        self.position_counts = {}
        self.resigned = None    # color that resigned, or None
        self._record_position()
    # --- position key for repetition ---
    def _position_key(self):
        return (self.board.serialize(), self.turn,
                self._castling_key(), self.en_passant_target)
    def _castling_key(self):
        cr = self.castling_rights
        return (cr['w']['K'], cr['w']['Q'], cr['b']['K'], cr['b']['Q'])
    def _record_position(self):
        key = self._position_key()
        self.position_counts[key] = self.position_counts.get(key, 0) + 1