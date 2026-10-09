'''
game.py
Defines the Game class that orchestrates turn-taking, applies moves to
the board, detects wins and draws, and reports the final result.
'''
class Game:
    """Manages the flow of a Connect Four match between two players."""
    def __init__(self, board, player1, player2):
        """Store the board and the two players; player 1 moves first."""
        self.board = board
        self.players = [player1, player2]
        self.current_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = (self.current_index + 1) % len(self.players)
    def play(self):
        """Run the game loop until a player wins or the board fills up."""
        print("\n{} ({}) vs {} ({})".format(
            self.players[0].name, self.players[0].disc,
            self.players[1].name, self.players[1].disc))
        self.board.display()
        while True:
            player = self.current_player
            column = player.get_move(self.board)
            row = self.board.drop_disc(column, player.disc)
            self.board.display()
            if self.board.check_win(row, column, player.disc):
                self.announce_result(player)
                break
            if self.board.is_full():
                self.announce_result(None)
                break
            self.switch_player()
    def announce_result(self, winner):
        """Print the final outcome of the match."""
        print()
        if winner is None:
            print("It's a draw! The board is full.")
        else:
            print("{} ({}) wins with four in a row!".format(winner.name, winner.disc))