'''
game.py
Core chess rules engine: move generation (including castling, en passant and
promotions), make/undo, check detection, SAN parsing and game-state helpers
(checkmate / stalemate / draw detection).
'''
import re
from pieces import Piece
from move import Move, square_name, parse_square, FILE_CHARS
from board import Board, WHITE, BLACK, opposite
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.turn = WHITE
        self.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant_target = None   # (row, col) square that can be captured en passant
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.position_counts = {}       # for threefold repetition
        self.history = []               # list of (san, move, undo) for the real game
        self.note_position()
    # ------------------------------------------------------------------ moves
    def generate_pseudo_legal_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color:
                    if piece.piece_type == 'P':
                        moves += self._pawn_moves(row, col, piece)
                    elif piece.piece_type == 'N':
                        moves += self._knight_moves(row, col, piece)
                    elif piece.piece_type == 'B':
                        moves += self._bishop_moves(row, col, piece)
                    elif piece.piece_type == 'R':
                        moves += self._rook_moves(row, col, piece)
                    elif piece.piece_type == 'Q':
                        moves += self._queen_moves(row, col, piece)
                    elif piece.piece_type == 'K':
                        moves += self._king_moves(row, col, piece)
        return moves
    def generate_legal_moves(self, color):
        legal = []
        for move in self.generate_pseudo_legal_moves(color):
            undo = self.make_move(move)
            if not self.is_in_check(color):
                legal.append(move)
            self.undo_move(move, undo)
        return legal