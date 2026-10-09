'''
game.py
Game class: manages turns, reads and validates player input,
applies moves (including multi-jump chains), detects game over.
Run this file directly to play:  python game.py
'''
from board import Board
from pieces import RED, BLACK
from rules import Rules
import notation
class Game:
    def __init__(self):
        self.board = Board()
        self.current_color = RED  # red moves first
        self.last_move = None
        self.game_over = False
        self.winner = None
    def switch_turn(self):
        self.current_color = BLACK if self.current_color == RED else RED
    @staticmethod
    def get_player_name(color):
        return 'Red' if color == RED else 'Black'
    def show_help(self):
        print(...)
    def show_legal_moves(self):
        legal, must_capture = Rules.get_legal_moves(self.board, self.current_color)
        ...
    def parse_input(self, raw):
        return notation.parse_move(raw)
    def apply_move(self, positions):
        '''Validate and apply; returns error string or None. Handles chains.'''
        ...
    def continue_jump(self, pos, piece):
        '''Interactive loop for chained jumps.'''
        ...
    def validate_chain(self, positions, color):
        sim = self.board.copy()
        ...
        return None or error string
    def maybe_crown(self, pos, piece):
        if not piece.is_king and pos[0] == Rules.get_king_row(piece.color):
            piece.crown()
            return True
        return False
    def has_won(self):
        opponent = BLACK if self.current_color == RED else RED
        if self.board.count_pieces(opponent) == 0:
            return True
        moves, _ = Rules.get_legal_moves(self.board, opponent)
        return len(moves) == 0  # no pieces OR no legal moves
    def play(self):
        # main loop
        ...