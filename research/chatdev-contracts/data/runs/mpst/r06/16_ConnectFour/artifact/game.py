'''
game.py
Defines the Game class that orchestrates a complete Connect Four match:
it alternates turns between two players, applies their moves to the board,
and ends the game when a winning line is detected or the grid is full.
'''
from board import Board
from player import Player
class Game:
    """Controls the flow of a single Connect Four match."""
    def __init__(self):
        """Set up the board and the two players."""
        self.board = Board()
        self.players = [
            Player("Player 1", Board.DISC_ONE),
            Player("Player 2", Board.DISC_TWO),
        ]
        self.current_player = self.players[0]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_player = (self.players[1]
                               if self.current_player is self.players[0]
                               else self.players[0])
    def play(self):
        """Run the main game loop until a win or a draw occurs."""
        print("Welcome to Connect Four!")
        print("Two players alternate dropping discs into a 7-column, "
              "6-row grid.")
        print("First to line up four in a row (horizontal, vertical or "
              "diagonal) wins.")
        self.board.display()
        while True:
            col = self.current_player.get_move(self.board)
            row = self.board.drop_disc(col, self.current_player.disc)
            self.board.display()
            if self.board.check_win(self.current_player.disc, row, col):
                self._announce_win()
                break
            if self.board.is_full():
                self._announce_draw()
                break
            self.switch_player()
    def _announce_win(self):
        """Print the victory message for the current player."""
        print("{} ({}) wins with four in a row!".format(
            self.current_player.name, self.current_player.disc))
    def _announce_draw(self):
        """Print the draw message when the grid is full."""
        print("The grid is full: the game ends in a draw!")