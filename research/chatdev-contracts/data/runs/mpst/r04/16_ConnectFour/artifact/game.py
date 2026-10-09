'''
game.py
Defines the Game class for the Connect Four game.
The Game orchestrates a full match: it alternates turns between the
two players, applies their moves to the board, checks for a winning
line or a full board after every move, and announces the result.
'''
from board import Board
class Game:
    """Runs one Connect Four match from the first move to the result."""
    def __init__(self, player1, player2, board=None):
        """Store the two players and create (or accept) a board."""
        self.board = board if board is not None else Board()
        self.players = (player1, player2)
        self.current_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = (self.current_index + 1) % len(self.players)
    def play(self):
        """Run the turn loop until someone wins or the board is full."""
        print("\nStarting a new game! Player 1 goes first.\n")
        self.board.display()
        while True:
            player = self.current_player
            column = player.get_move(self.board)
            self.board.drop_disc(column, player.disc)
            winning_line = self.board.find_winning_line(player.disc)
            board_full = self.board.is_full()
            print(f"\n{player.name} drops a '{player.disc}' into column {column + 1}.")
            if winning_line is not None:
                self.board.display(highlight=winning_line)
                self.announce_winner(player)
                return player
            self.board.display()
            if board_full:
                self.announce_draw()
                return None
            self.switch_player()
    def announce_winner(self, player):
        """Print the victory message for the winning player."""
        print(f"\n*** {player.name} ({player.disc}) connects four and wins the game! ***")
    def announce_draw(self):
        """Print the message shown when the board fills with no winner."""
        print("\n*** The board is full. It's a draw! ***")