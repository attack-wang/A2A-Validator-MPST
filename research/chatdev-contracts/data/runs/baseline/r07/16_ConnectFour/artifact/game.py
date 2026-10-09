'''
game.py
This module defines the Game class, which orchestrates a full session
of Connect Four: alternating turns between two players, applying moves
to the board, detecting wins and draws, and announcing the result.
'''
from board import Board
from player import Player
class Game:
    """Coordinates the flow of a Connect Four match."""
    def __init__(self, player_one: Player, player_two: Player) -> None:
        """
        Initialize the game with two players and an empty board.
        Args:
            player_one: The Player who moves first (uses their disc).
            player_two: The Player who moves second.
        """
        self.board = Board()
        self.players = [player_one, player_two]
        self.current_index = 0
        self.winner = None
    @property
    def current_player(self) -> Player:
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_turn(self) -> None:
        """Hand the turn over to the other player."""
        self.current_index = (self.current_index + 1) % len(self.players)
    def reset(self) -> None:
        """Clear the board and restore the initial turn order."""
        self.board.reset()
        self.current_index = 0
        self.winner = None
    def play(self) -> None:
        """
        Run the main game loop until a player wins or the board is
        full (draw).
        """
        print("\n" + "-" * 46)
        print(f"{self.players[0].name} plays '{self.players[0].disc}' | "
              f"{self.players[1].name} plays '{self.players[1].disc}'")
        print("-" * 46)
        while True:
            self.board.display()
            player = self.current_player
            column = player.get_move(self.board)
            row, col = self.board.drop_disc(column, player.disc)
            if self.board.check_win(row, col, player.disc):
                self.winner = player
                self.board.display()
                self.announce_result()
                return
            if self.board.is_full():
                self.board.display()
                self.announce_result()
                return
            self.switch_turn()
    def announce_result(self) -> None:
        """Print the final outcome of the match."""
        print("=" * 46)
        if self.winner is not None:
            print(f"  {self.winner.name} ({self.winner.disc}) wins with "
                  "four in a row!")
        else:
            print("  It's a draw! The grid is full with no line of four.")
        print("=" * 46)