'''
game.py
Game state and rules engine: turn management, applying moves,
chain-jump continuation, kinging, and win/loss detection.
'''
from pieces import PieceColor
from board import Board
from moves import Move, get_all_moves, get_single_jumps
class Game:
    def __init__(self):
        self.board = Board()
        self.current_color = PieceColor.RED  # Red moves first
        self.game_over = False
        self.winner = None
    def legal_moves(self):
        '''All legal moves for the player to move (captures compulsory).'''
        return get_all_moves(self.board, self.current_color)
    def legal_moves_for(self, start):
        '''Legal moves (respecting compulsory capture) that begin at `start`.'''
        start = tuple(start)
        return [m for m in self.legal_moves() if m.start == start]
    def find_matching_move(self, waypoints):
        '''Match parsed waypoints against the legal moves.
        Exact path match first; then, for convenience, accept a two-square
        "from-to" input for a jump whose full chain is uniquely determined.
        '''
        waypoints = [tuple(w) for w in waypoints]
        candidates = [m for m in self.legal_moves() if m.start == waypoints[0]]
        for move in candidates:
            if list(move.path) == waypoints:
                return move
        if len(waypoints) == 2:
            matches = [m for m in candidates if m.end == waypoints[1]]
            if len(matches) == 1:
                return matches[0]
        return None
    def apply_move(self, move):
        '''Execute a fully validated move on the board.'''
        fr, fc = move.start
        piece = self.board.get_piece(fr, fc)
        self.board.remove_piece(fr, fc)
        for cr, cc in move.captures:
            self.board.remove_piece(cr, cc)
        tr, tc = move.end
        self.board.place_piece(tr, tc, piece)
        # Kinging: crown a man that reaches its crowning row.
        if not piece.is_king and Board.is_king_row(piece.color, tr):
            piece.crown()
        # Switch turn.
        self.current_color = self.current_color.opposite
        self._check_game_over()
    def _check_game_over(self):
        '''The player to move loses if they have no pieces or no legal moves.'''
        if self.board.count_pieces(self.current_color) == 0:
            self.game_over = True
            self.winner = self.current_color.opposite
        elif not self.legal_moves():
            self.game_over = True
            self.winner = self.current_color.opposite