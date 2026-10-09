'''
Console fallback interface for the Gomoku game.
Provides a text-based UI so the game stays fully playable even when the
optional pygame dependency is missing. Players type moves as "row col"
(1-based indices) and the board plus status message are reprinted after
every turn until a player forms five in a row or the board fills up.
'''
from board import Board
from game import Game
class ConsoleUI:
    """Text-based user interface driving the Game controller."""
    SYMBOLS = {Board.EMPTY: ".", Board.BLACK: "X", Board.WHITE: "O"}
    def __init__(self, game):
        self.game = game
    def _player_name(self):
        """Return 'Black' or 'White' for the player who must move."""
        return "Black" if self.game.current_player == Board.BLACK else "White"
    def render(self):
        """Print the board with 1-based row/column labels and the status."""
        board = self.game.board
        header = "   " + " ".join(f"{c + 1:2d}" for c in range(board.size))
        print(header)
        for r in range(board.size):
            cells = " ".join(f"{self.SYMBOLS[board.get_stone(r, c)]:>2s}"
                             for c in range(board.size))
            print(f"{r + 1:2d} {cells}")
        print(self.game.status_message())
    def parse_input(self, text):
        """Convert 'row col' text into (row, col) board coordinates.
        Accepts two integers separated by spaces or commas using 1-based
        indices; returns None when the input is malformed or out of range.
        """
        parts = text.replace(",", " ").split()
        if len(parts) != 2:
            return None
        try:
            row, col = int(parts[0]) - 1, int(parts[1]) - 1
        except ValueError:
            return None
        if 0 <= row < self.game.board.size and 0 <= col < self.game.board.size:
            return row, col
        return None
    def run(self):
        """Read moves from stdin until the game ends or the user quits."""
        print("=== Gomoku (Five in a Row) - console mode ===")
        print("Enter moves as 'row col' (1-15), or 'quit' to exit.")
        while not self.game.is_over:
            self.render()
            try:
                raw = input(f"{self._player_name()} move> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGame aborted.")
                return
            if raw.lower() in ("quit", "exit", "q"):
                print("Game aborted.")
                return
            pos = self.parse_input(raw)
            if pos is None:
                print("Invalid input. Enter two numbers, e.g. '8 8'.")
                continue
            row, col = pos
            if not self.game.try_move(row, col):
                print("That intersection is occupied. Choose an empty one.")
        self.render()
        print("Game over. Thanks for playing!")