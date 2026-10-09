'''
game.py
Game controller: owns the Board and the two Players, alternates turns,
applies moves, detects wins/draws, and tracks the running score.
'''
from board import Board
from player import Player
class Game:
    """Coordinates a tic-tac-toe match between two human players."""
    def __init__(self, player1_name="Player 1", player2_name="Player 2"):
        self.board = Board()
        self.players = [
            Player(player1_name, "X"),
            Player(player2_name, "O"),
        ]
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
        self.winning_line = None
    # ------------------------------------------------------------------ state helpers
    @property
    def current_player(self):
        """The player whose turn it is."""
        return self.players[self.current_player_index]
    def get_status(self):
        """Human-readable summary of the current game state."""
        if self.game_over:
            if self.winner is not None:
                return f"{self.winner.name} ({self.winner.symbol}) wins!"
            return "It's a draw!"
        return f"{self.current_player.name}'s turn — place {self.current_player.symbol}"
    def get_score_text(self):
        """Running score across rounds."""
        p1, p2 = self.players
        return f"Score — {p1.name} (X): {p1.wins}   |   {p2.name} (O): {p2.wins}"
    # ------------------------------------------------------------------ gameplay
    def make_move(self, row, col):
        """
        Attempt to place the current player's symbol at (row, col).
        Returns True when the move was applied (board changed), False when
        the move is illegal or the round has already finished.
        """
        if self.game_over:
            return False
        if not self.board.make_move(row, col, self.current_player.symbol):
            return False
        line = self.board.get_winning_line(self.current_player.symbol)
        if line is not None:
            self.game_over = True
            self.winner = self.current_player
            self.winning_line = line
            self.current_player.add_win()
        elif self.board.is_full():
            self.game_over = True
        else:
            self.switch_player()
        return True
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player_index = 1 - self.current_player_index
    def reset(self):
        """Clear the board and start a new round (X always moves first)."""
        self.board.reset()
        self.current_player_index = 0
        self.game_over = False
        self.winner = None
        self.winning_line = None