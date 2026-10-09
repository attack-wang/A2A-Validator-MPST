'''
game.py
Game loop: alternates turns between the two players, validates column
choices, applies moves to the board, and stops on a win, a draw, or an
ended input stream (EOF), which now terminates the match gracefully
instead of crashing with a traceback.
'''
class Game:
    """Coordinates the flow of a complete Connect Four match."""
    def __init__(self, board, player1, player2, ui):
        """Store the board, the two players, and the console interface."""
        self.board = board
        self.players = [player1, player2]
        self.ui = ui
        self.current_index = 0  # Player 1 always starts
    def play(self):
        """Run the match until a player wins, the grid is full, or the
        input stream is closed (EOF), in which case the game ends with
        a friendly message instead of an unhandled exception.
        """
        self.ui.display_board(self.board)
        while True:
            player = self.players[self.current_index]
            try:
                col = self.get_valid_move(player)  # 0-based column index
            except EOFError:
                # stdin was closed/exhausted mid-prompt; stop cleanly.
                print("\nInput stream closed (EOF). Game ended. Goodbye!")
                return
            row = self.board.drop_disc(col, player.disc)
            self.ui.display_board(self.board)
            if self.board.check_win(row, col, player.disc):
                self.ui.display_winner(player)
                break
            if self.board.is_full():
                self.ui.display_draw()
                break
            self.switch_turn()
    def get_valid_move(self, player):
        """Prompt the current player until a valid, non-full column is
        chosen. Returns the chosen column as a 0-based index. EOFError
        from the prompt propagates to play() so the match can stop.
        """
        while True:
            choice = self.ui.prompt_column(player, self.board.cols)
            if choice is None:
                continue  # non-numeric input; warning already displayed
            col = choice - 1  # convert 1-based user input to 0-based index
            if self.board.is_valid_column(col):
                return col
            self.ui.display_invalid_column()
    def switch_turn(self):
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index