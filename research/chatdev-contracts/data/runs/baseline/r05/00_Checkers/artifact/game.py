'''
game.py
Game state controller: owns the board, tracks whose turn it is, applies
validated moves, and enforces the draw rule (40 quiet plies per side).
'''
from board import Board
from pieces import Player
class Game:
    FIRST_PLAYER = Player.BLACK  # American checkers: Black (darker) moves first
    QUIET_PLY_LIMIT = 80  # 40 moves per side without capture or man advance
    def __init__(self):
        self.board = Board()
        self.current_player = self.FIRST_PLAYER
        self.quiet_plies = 0
        self.history = []
    def legal_moves(self):
        return self.board.legal_moves(self.current_player)
    def apply_player_move(self, move):
        mover = self.board.get_piece(move.start.row, move.start.col)
        if mover is None or mover.player is not self.current_player:
            raise ValueError("Move does not start with the current player's piece.")
        moved_man = mover is not None and not mover.is_king
        promoted = self.board.apply_move(move)
        if move.is_capture or moved_man:
            self.quiet_plies = 0
        else:
            self.quiet_plies += 1
        self.history.append(move)
        self.current_player = self.current_player.opponent
        return promoted