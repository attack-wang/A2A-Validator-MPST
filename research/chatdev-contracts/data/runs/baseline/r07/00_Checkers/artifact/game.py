'''
game.py - Game state management, turn alternation, and win/draw detection.
'''
from pieces import RED, BLACK
from board import Board
from move import Move, square_name, parse_square
from rules import all_moves, moves_for_piece
class Game:
    def __init__(self):
        self.board = Board()
        self.current = BLACK  # Black moves first per standard rules
        self.game_over = False
        self.winner = None
        self.continue_from = None  # position of piece that must keep jumping
    def legal_moves(self):
        if self.continue_from is not None:
            _, jumps = moves_for_piece(self.board, self.continue_from)
            return jumps
        return all_moves(self.board, self.current)
    def apply_move(self, move):
        piece = self.board.get_piece(move.from_pos)
        self.board.set_piece(move.from_pos, None)
        if move.is_jump:
            self.board.set_piece(move.captured_pos, None)
        promoted = False
        if not piece.is_king:
            if piece.color == RED and move.to_pos[0] == 0:
                piece.promote()
                promoted = True
            elif piece.color == BLACK and move.to_pos[0] == 7:
                piece.promote()
                promoted = True
        self.board.set_piece(move.to_pos, piece)
        return promoted
    def play_turn(self, move):
        """Execute a validated move and advance game state. Returns a status message."""
        promoted = self.apply_move(move)
        messages = []
        if promoted:
            messages.append(f"{self.current} piece promoted to King at {square_name(move.to_pos)}!")
        if move.is_jump:
            # Multi-jump: same piece must continue if further jumps available
            _, further_jumps = moves_for_piece(self.board, move.to_pos)
            if further_jumps and not promoted:
                self.continue_from = move.to_pos
                messages.append("Capture chain available — the same piece must jump again!")
                return messages
        self.continue_from = None
        self.check_game_over()
        if not self.game_over:
            self.current = RED if self.current == BLACK else BLACK
        return messages