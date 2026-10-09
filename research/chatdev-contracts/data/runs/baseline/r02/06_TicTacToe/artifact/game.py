'''
game.py
Game module for the Tic-Tac-Toe game.
This module defines the Game class, which orchestrates a full session of
tic-tac-toe between two players. Responsibilities include:
  * alternating turns between the two players,
  * applying validated moves to the board,
  * recording a history of every move made,
  * detecting win/draw conditions after each move,
  * announcing the result,
  * offering a rematch.
The rematch prompt uses the centralized safe_input() helper so a closed
or exhausted standard input stream ends the session gracefully instead
of raising an unhandled EOFError.
'''
from board import Board
from player import Player
from io_utils import safe_input
class Game:
    """Manages the flow of tic-tac-toe matches between two players."""
    def __init__(self, player1: Player, player2: Player):
        """Initialize the game with two players, an empty board, and empty history."""
        self.board = Board()
        self.players = [player1, player2]
        self.current_index = 0
        self.move_history = []
    @property
    def current_player(self) -> Player:
        """Return the player whose turn it currently is."""
        return self.players[self.current_index]
    def switch_turn(self):
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index
    def record_move(self, player: Player, row: int, col: int):
        """Append a move to the history using human-readable 1-based coordinates."""
        self.move_history.append((player.name, player.symbol, row + 1, col + 1))
    def show_move_history(self):
        """Print a numbered list of all moves made during the game."""
        if not self.move_history:
            return
        print("Move history:")
        for number, (name, symbol, row, col) in enumerate(self.move_history, start=1):
            print(f"  {number}. {name} ({symbol}) -> row {row}, column {col}")
        print()
    def announce_result(self, winner_symbol):
        """Announce the winner, or a draw if the board filled with no winner."""
        print("=" * 45)
        if winner_symbol:
            winner = next(p for p in self.players if p.symbol == winner_symbol)
            print(f"  *** {winner.name} ({winner.symbol}) WINS! Congratulations! ***")
        else:
            print("  *** It's a draw! The board is full. ***")
        print("=" * 45)
    def play(self):
        """Run the turn-based loop until someone wins or the board is full."""
        print(f"\nNew game started! {self.players[0].name} is X, "
              f"{self.players[1].name} is O.")
        print("Enter moves as 'row,col' using numbers 1-3 (see the board labels).")
        self.board.display()
        while True:
            player = self.current_player
            row, col = player.get_move(self.board)
            self.board.make_move(row, col, player.symbol)
            self.record_move(player, row, col)
            self.board.display()
            winner_symbol = self.board.check_winner()
            if winner_symbol:
                self.announce_result(winner_symbol)
                self.show_move_history()
                return
            if self.board.is_full():
                self.announce_result(None)
                self.show_move_history()
                return
            self.switch_turn()
    def rematch(self) -> bool:
        """Ask whether the players want another round. Returns True for yes."""
        while True:
            answer = safe_input("Play again? (y/n): ").strip().lower()
            if answer in ('y', 'yes'):
                return True
            if answer in ('n', 'no'):
                return False
            print("  Please answer with 'y' or 'n'.")