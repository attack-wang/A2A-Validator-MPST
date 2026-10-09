'''
game.py
Defines the Game class: drives alternating turns, applies moves,
detects wins/draws, and ends the match appropriately.
'''
class Game:
    """Manages the flow of one Connect Four match between two players."""
    def __init__(self, board, player1, player2):
        """Store the board and players; Player 1 always moves first."""
        self.board = board
        self.players = [player1, player2]
        self.current_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index
    def play(self):
        """Run the loop until a win or draw, then announce the result."""
        self.board.render()
        while True:
            player = self.current_player
            column = player.get_move(self.board)      # validated input
            row = self.board.drop_disc(column, player.disc)
            if row is None:                           # defensive guard
                continue
            self.board.render()
            if self.board.check_win(row, column, player.disc):
                print(f"{player.name} ({player.disc}) wins! Four in a row!")
                return
            if self.board.is_full():
                print("It's a draw! The board is full.")
                return
            self.switch_player()