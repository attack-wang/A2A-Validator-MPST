'''
game.py
Rules and turn-management layer built on top of Board. It tracks the current
player, applies moves (flipping discs automatically), handles forced passes,
detects the end of the game (board full or neither player able to move) and
reports the running score and the winner.
'''
from board import Board, BLACK, WHITE
class Game:
    """Coordinates two players alternating turns on a Board."""
    def __init__(self):
        self.board = Board()
        self.current_player = BLACK      # Black moves first (official rule)
        self.move_count = 0
        self.consecutive_passes = 0      # bookkeeping for automatic passes
    def opponent_of(self, player=None):
        """Return the opponent of `player` (defaults to the current player)."""
        player = self.current_player if player is None else player
        return self.board.opponent(player)
    def has_valid_move(self, player=None):
        """Return True if `player` (default: current player) has a legal move."""
        player = self.current_player if player is None else player
        return bool(self.board.get_valid_moves(player))
    def switch_turn(self):
        """Hand the turn to the opponent (used when the current player passes)."""
        self.current_player = self.opponent_of()
    def advance_turn(self):
        """
        Give the turn to the opponent after a move. If the opponent has no
        legal move they pass automatically and the same player continues.
        Returns True when a pass occurred.
        """
        opponent = self.opponent_of()
        if self.board.get_valid_moves(opponent):
            self.current_player = opponent
            self.consecutive_passes = 0
            return False
        self.consecutive_passes += 1
        return True
    def is_game_over(self):
        """True when the board is full or neither player can move."""
        if self.board.is_full():
            return True
        return not (self.has_valid_move(BLACK) or self.has_valid_move(WHITE))
    def apply_move(self, row, col):
        """Apply the current player's move, flip discs, then advance the turn."""
        flipped = self.board.apply_move(self.current_player, row, col)
        self.move_count += 1
        self.advance_turn()
        return flipped
    def get_score(self):
        """Return the score as {BLACK: black_count, WHITE: white_count}."""
        black, white = self.board.count_discs()
        return {BLACK: black, WHITE: white}
    def get_winner(self):
        """Return BLACK, WHITE or None (draw). Call only when the game is over."""
        score = self.get_score()
        if score[BLACK] > score[WHITE]:
            return BLACK
        if score[WHITE] > score[BLACK]:
            return WHITE
        return None