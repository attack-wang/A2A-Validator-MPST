'''
Game module for the Tic-Tac-Toe game.
This module defines the Game class, which orchestrates a full round of
Tic-Tac-Toe: setting up the two players, alternating turns, applying
moves to the board, and announcing the winner or a draw.
'''
from board import Board
from player import Player
class Game:
    """Controls the flow of a single Tic-Tac-Toe round."""
    def __init__(self):
        """Create the board and an empty player list; X always starts."""
        self.board = Board()
        self.players = []
        self.current_player_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_player_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player_index = 1 - self.current_player_index
    def setup(self):
        """Greet the users, collect player names, and explain the controls."""
        print("=" * 46)
        print("        WELCOME TO TIC-TAC-TOE (3x3)")
        print("=" * 46)
        name1 = input("Player 1 name (press Enter for 'Player 1'): ").strip()
        name2 = input("Player 2 name (press Enter for 'Player 2'): ").strip()
        self.players = [
            Player(name1 or "Player 1", "X"),
            Player(name2 or "Player 2", "O"),
        ]
        print()
        print(f"{self.players[0].name} plays as X, {self.players[1].name} plays as O.")
        print("X goes first. Enter moves as 'row,column' (1-3), e.g. 1,1 = top-left.")
        print("Type 'q' during your turn to quit the round.")
    def announce_result(self, winner):
        """Print the final banner for a win or a draw."""
        print("=" * 46)
        if winner is not None:
            print(f"  *** {winner.name} ({winner.symbol}) WINS! ***")
        else:
            print("  *** It's a DRAW! The board is full. ***")
        print("=" * 46)
    def play(self):
        """Run the main turn-based loop until someone wins or the board fills.
        Returns the winning Player, or None for a draw or if the round
        was quit early.
        """
        self.setup()
        winner = None
        while True:
            self.board.display()
            move = self.current_player.get_move(self.board)
            if move is None:  # player chose to quit
                print("Round ended early. Thanks for playing!")
                return None
            row, col = move
            if not self.board.make_move(row, col, self.current_player.symbol):
                # Defensive check: get_move() should guarantee validity, but
                # if the move cannot be applied, re-prompt the SAME player
                # rather than silently skipping their turn. This keeps turn
                # order and board state consistent under all conditions.
                print("Move could not be applied. Please try again.")
                continue
            winning_symbol = self.board.check_winner()
            if winning_symbol is not None:
                self.board.display()
                self.announce_result(self.current_player)
                winner = self.current_player
                break
            if self.board.is_full():
                self.board.display()
                self.announce_result(None)
                break
            self.switch_player()
        return winner