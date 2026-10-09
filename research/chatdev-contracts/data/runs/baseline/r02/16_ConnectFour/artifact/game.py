'''
game.py
This module defines the Game class, which orchestrates the Connect Four
match: turn alternation, input handling, validation, and end-game detection.
'''
from board import Board
from player import Player
from renderer import Renderer
QUIT = 'quit'  # sentinel: end the game gracefully
class Game:
    """Manages the flow of a Connect Four game between two players."""
    QUIT_COMMANDS = {'q', 'quit', 'exit'}
    def __init__(self):
        """Set up the board, two players, and the console renderer."""
        self.board = Board()
        self.renderer = Renderer()
        self.players = [Player("Player 1", 'X'), Player("Player 2", 'O')]
        self.current_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def get_column_choice(self):
        """
        Prompt the current player for a column number.
        Returns a 0-indexed column, None for invalid input (re-prompt),
        or the QUIT sentinel when input ends or the player quits.
        """
        self.renderer.show_turn(self.current_player, self.board.cols)
        try:
            raw = input("> ").strip()
        except EOFError:
            # stdin closed/exhausted (non-interactive or piped input ran out)
            self.renderer.show_message("\nInput stream ended. Game stopped.")
            return QUIT
        except KeyboardInterrupt:
            self.renderer.show_message("\nGame interrupted. Goodbye!")
            return QUIT
        if raw.lower() in self.QUIT_COMMANDS:
            return QUIT
        if not raw.isdigit():
            self.renderer.show_message("Invalid input. Please type a number.")
            return None
        try:
            col = int(raw) - 1  # convert 1-indexed input to 0-indexed
        except ValueError:
            # defensive: unicode digits like '²' pass isdigit() but fail int()
            self.renderer.show_message("Invalid input. Please type a number.")
            return None
        if not self.board.is_valid_column(col):
            self.renderer.show_message(
                "Invalid column. It is out of range or already full.")
            return None
        return col
    def play(self):
        """Run the main loop until a player wins, the board is full,
        or the input stream ends."""
        self.renderer.show_message("Welcome to Connect Four!")
        self.renderer.show_message(
            f"{self.players[0]} vs {self.players[1]}. Let's play!")
        self.renderer.show_message("(Type 'q' at any prompt to quit.)")
        while True:
            self.renderer.render_board(self.board)
            col = self.get_column_choice()
            if col == QUIT:
                self.renderer.show_message("Game over. Thanks for playing!")
                break
            if col is None:
                continue  # re-prompt the same player after invalid input
            row = self.board.drop_disc(col, self.current_player.disc)
            if self.board.check_win(row, col, self.current_player.disc):
                self.renderer.render_board(self.board)
                self.renderer.show_message(
                    f"{self.current_player.name} wins! Four in a row!")
                break
            if self.board.is_full():
                self.renderer.render_board(self.board)
                self.renderer.show_message("It's a draw! The board is full.")
                break
            self.current_index = 1 - self.current_index  # switch turns