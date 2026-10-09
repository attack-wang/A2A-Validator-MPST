'''
game.py
Defines the Game class, which orchestrates the tic-tac-toe match:
turn alternation, move processing, win/draw detection, score keeping,
and round resets.
'''
from board import Board
class Game:
    """Controls the state and flow of a two-player tic-tac-toe game."""
    STATE_ONGOING = "ongoing"
    STATE_WON = "won"
    STATE_DRAW = "draw"
    def __init__(self, player_x="Player 1 (X)", player_o="Player 2 (O)"):
        """Create a new game with an empty board; X always moves first."""
        self.board = Board()
        self.players = {"X": player_x, "O": player_o}
        self.starting_mark = "X"
        self.current_mark = self.starting_mark
        self.state = self.STATE_ONGOING
        self.winner = None
        self.scores = {"X": 0, "O": 0, "Draw": 0}
    def get_current_player(self):
        """Return the name of the player who moves next."""
        return self.players[self.current_mark]
    def get_current_mark(self):
        """Return the mark ("X" or "O") of the player who moves next."""
        return self.current_mark
    def get_winner_name(self):
        """
        Return the name of the winning player.
        Returns:
            str | None: the winner's player name, or None when the
            game has not been won.
        """
        if self.winner is None:
            return None
        return self.players[self.winner]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_mark = "O" if self.current_mark == "X" else "X"
    def play_turn(self, row, col):
        """
        Attempt to play the current player's mark at (row, col).
        The move is rejected when the game is already finished or the
        target cell is occupied. After a successful move the state is
        re-evaluated: a win is recorded, a full board ends in a draw,
        and otherwise the turn passes to the other player.
        Returns:
            bool: True when the move was accepted, False otherwise.
        """
        if self.state != self.STATE_ONGOING:
            return False
        if not self.board.make_move(row, col, self.current_mark):
            return False
        winner = self.board.check_winner()
        if winner is not None:
            self.state = self.STATE_WON
            self.winner = winner
            self.scores[winner] += 1
        elif self.board.is_full():
            self.state = self.STATE_DRAW
            self.scores["Draw"] += 1
        else:
            self.switch_player()
        return True
    def reset_game(self):
        """
        Start a fresh round while keeping the running scores.
        Whenever the previous round has finished, the player who starts
        the next round alternates so neither side keeps the first-move
        advantage.
        """
        if self.state != self.STATE_ONGOING:
            self.starting_mark = "O" if self.starting_mark == "X" else "X"
        self.board.reset()
        self.state = self.STATE_ONGOING
        self.winner = None
        self.current_mark = self.starting_mark
    def reset_scores(self):
        """Zero out the running scoreboard."""
        self.scores = {"X": 0, "O": 0, "Draw": 0}