'''
game.py
Defines the Game class, which controls the flow of a Connect Four match.
Responsibilities:
  * Create the board and the two players.
  * Alternate turns between players.
  * Prompt each player for a column, validate the choice, and re-prompt
    on invalid input (non-numeric, out of range, or full column).
  * Update and re-render the board after every successful move.
  * Detect a win (four in a row) or a draw (full grid) and end the game.
  * Offer a rematch after a game finishes.
  * Handle closed/interrupted input streams (EOFError, KeyboardInterrupt)
    gracefully instead of crashing with a raw traceback.
'''
from board import Board
from player import Player
class GameOver(Exception):
    """Raised when the input stream is closed or the session is interrupted."""
def safe_input(prompt):
    """
    Read a line from stdin, converting EOF/interrupt conditions into a
    clean GameOver signal instead of letting EOFError or
    KeyboardInterrupt escape as a raw traceback.
    """
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        raise GameOver
class Game:
    """Controls one Connect Four match from start to finish."""
    def __init__(self):
        """Set up the board, the two players, and the starting turn."""
        self.board = Board(rows=6, cols=7)
        self.players = [
            Player("Player 1", "X"),
            Player("Player 2", "O"),
        ]
        self.current_index = 0
    @property
    def current_player(self):
        """Return the player whose turn it is."""
        return self.players[self.current_index]
    def switch_player(self):
        """Hand the turn over to the other player."""
        self.current_index = 1 - self.current_index
    def get_player_move(self, player):
        """
        Prompt the player for a column until a valid choice is given.
        Accepts integers 1..7 (1-based, matching the printed header).
        Re-prompts on non-numeric input, out-of-range columns, and
        columns that are already full. If the input stream is closed
        (EOF) or the session is interrupted (Ctrl+C), the game ends
        cleanly with a friendly message instead of a traceback.
        """
        while True:
            try:
                raw = safe_input(
                    f"{player}, choose a column (1-{self.board.cols}): "
                ).strip()
            except GameOver:
                print("\nInput stream closed. Ending game. Goodbye!")
                raise SystemExit(0)
            try:
                col = int(raw) - 1  # convert to 0-based index
            except ValueError:
                # Catches all non-parseable input, including Unicode
                # characters like '²' or '①' that pass str.isdigit()
                # but cannot be converted by int().
                print("Invalid input: please type a number.")
                continue
            if not self.board.is_valid_column(col):
                print("Invalid column: out of range or already full. Try again.")
                continue
            return col
    def play(self):
        """Run one full game until a player wins or the grid is full."""
        print("=" * 40)
        print("            CONNECT FOUR")
        print("=" * 40)
        print(f"{self.players[0]} vs {self.players[1]}")
        print("Form a line of four discs to win!")
        self.board.render()
        while True:
            player = self.current_player
            col = self.get_player_move(player)
            self.board.drop_disc(col, player.disc)
            self.board.render()
            if self.board.check_win(player.disc):
                print(f"*** {player.name} wins! ***")
                break
            if self.board.is_full():
                print("The grid is full. It's a draw!")
                break
            self.switch_player()
    def wants_rematch(self):
        """
        Ask whether the players want another game.
        A closed/interrupted input stream is treated as "no" so the
        program still exits gracefully instead of crashing.
        """
        try:
            answer = safe_input("Play again? (y/n): ").strip().lower()
        except GameOver:
            return False  # EOF/interrupt → treat as "no", exit gracefully
        return answer in ("y", "yes")
    def run(self):
        """Keep starting new games as long as the players want rematches."""
        while True:
            self.play()
            if not self.wants_rematch():
                print("Thanks for playing Connect Four. Goodbye!")
                break
            # Reset state for the next match
            self.board = Board(rows=6, cols=7)
            self.current_index = 0