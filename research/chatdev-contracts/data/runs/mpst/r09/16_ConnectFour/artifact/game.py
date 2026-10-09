'''
game.py
Defines the Game class that orchestrates the Connect Four match. It manages
turn order, prompts players for column choices, validates input, applies
moves to the Board, detects wins and draws, and displays the results.
'''
from exceptions import ColumnFullError, InvalidColumnError
class Game:
    """Manages the flow of a Connect Four game between two players."""
    def __init__(self, board, players):
        """Initialize the game with a board and an ordered list of players."""
        self._board = board
        self._players = players
        self._turn_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self._players[self._turn_index]
    def play(self):
        """Run the main game loop until a player wins or the board is full."""
        print("Welcome to Connect Four!")
        print(self._board.render())
        try:
            while True:
                player = self.current_player
                column = self.get_valid_move()
                try:
                    row = self._board.drop_disc(column, player.disc)
                except (ColumnFullError, InvalidColumnError) as error:
                    print("Invalid move: {}. Try again.".format(error))
                    continue
                print("\n{} dropped a disc into column {}.".format(player.name, column + 1))
                print(self._board.render())
                if self._board.check_win(row, column, player.disc):
                    print("\n{} wins! Congratulations!".format(player.name))
                    return
                if self._board.is_full():
                    print("\nThe board is full. It's a draw!")
                    return
                self._advance_turn()
        except (KeyboardInterrupt, EOFError):
            print("\nGame interrupted. Exiting.")
            return
    def _advance_turn(self):
        """Switch control to the next player in turn order."""
        self._turn_index = (self._turn_index + 1) % len(self._players)
    def get_valid_move(self):
        """Prompt the current player until a valid, non-full column is chosen."""
        while True:
            prompt = "{}, choose a column (1-{}): ".format(self.current_player.name, self._board.cols)
            raw_input_value = input(prompt).strip()
            try:
                column = int(raw_input_value)
            except ValueError:
                print("Invalid input: '{}' is not a number. Please try again.".format(raw_input_value))
                continue
            index = column - 1
            if index < 0 or index >= self._board.cols:
                print("Invalid move: column must be between 1 and {}. Please try again.".format(self._board.cols))
                continue
            if not self._board.is_valid_column(index):
                print("Invalid move: column {} is already full. Please try again.".format(column))
                continue
            return index