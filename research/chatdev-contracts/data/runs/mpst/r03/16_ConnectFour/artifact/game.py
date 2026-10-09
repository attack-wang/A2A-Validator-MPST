'''
Module: game.py
Defines the Game class, which orchestrates a full session of Connect Four:
it owns the Board and the two Players, alternates turns, applies each move,
checks for a win or a draw after every placement, and reports the outcome.
'''
from board import Board
from player import Player
class Game:
    """Controls turn order, move application, and end-of-game detection."""
    DISC_ONE = 'X'
    DISC_TWO = 'O'
    def __init__(self):
        """Create a fresh board and two players; Player 1 moves first."""
        self.board = Board()
        self.players = [
            Player("Player 1", self.DISC_ONE),
            Player("Player 2", self.DISC_TWO),
        ]
        self.current_index = 0
        self.game_over = False
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = (self.current_index + 1) % len(self.players)
    def play(self):
        """Run the main loop until someone wins or the grid fills up."""
        print("=" * 40)
        print("        Welcome to Connect Four!")
        print("=" * 40)
        print(f"Line up four {self.DISC_ONE}'s or {self.DISC_TWO}'s "
              "horizontally, vertically, or diagonally to win.")
        self.board.display()
        while not self.game_over:
            player = self.current_player
            col = player.get_move(self.board)
            row = self.board.drop_disc(col, player.disc)
            self.board.display()
            if self.board.check_win(row, col, player.disc):
                self.handle_win(player)
            elif self.board.is_full():
                self.handle_draw()
            else:
                self.switch_player()
    def handle_win(self, player):
        """Announce the winner and stop the loop."""
        print(f"Congratulations, {player.name}! "
              f"Four in a row with '{player.disc}' - you win!")
        self.game_over = True
    def handle_draw(self):
        """Announce a draw when the grid is full with no winner."""
        print("The grid is full and nobody lined up four. It's a draw!")
        self.game_over = True