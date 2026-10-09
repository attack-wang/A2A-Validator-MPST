"""Console user interface for the tic-tac-toe game."""

from game import TicTacToe

POSITION_MAP = {
    "1": 0, "2": 1, "3": 2,
    "4": 3, "5": 4, "6": 5,
    "7": 6, "8": 7, "9": 8,
}


class ConsoleUI:
    def __init__(self):
        self.game = TicTacToe()

    def _read_line(self, prompt=""):
        """Read one line of input; treat a closed stdin (EOF) as a clean quit."""
        try:
            return input(prompt)
        except EOFError:
            print("\nInput stream closed. Goodbye!")
            raise SystemExit(0)

    def run(self):
        print("Welcome to Tic-Tac-Toe!")
        print("Positions are numbered 1-9 like a keypad:")
        self._print_guide()
        while True:
            self.game.reset()
            self._play_round()
            if not self._ask_replay():
                print("Thanks for playing! Goodbye.")
                break

    def _play_round(self):
        while True:
            self._print_board()
            result = self.game.check_winner()
            if result:
                self._announce(result)
                return
            player = self.game.current_player
            raw = self._read_line(f"Player {player}, choose a position (1-9): ").strip()
            if raw.lower() in ("q", "quit", "exit"):
                print("Game aborted. Goodbye!")
                raise SystemExit(0)
            if raw not in POSITION_MAP:
                print("Invalid input. Please enter a number from 1 to 9.")
                continue
            if not self.game.make_move(POSITION_MAP[raw]):
                print("That square is already taken. Try another.")

    def _announce(self, result):
        self._print_board()
        if result == "Draw":
            print("It's a draw! The board is full.")
        else:
            cells = ", ".join(str(p + 1) for p in self.game.winning_line())
            print(f"Player {result} wins! (line: {cells})")
        history = ", ".join(f"{p}->{pos + 1}" for p, pos in self.game.moves)
        print(f"Move history: {history}")

    def _print_board(self):
        b = self.game.board
        print()
        for row in range(3):
            cells = [b[row * 3 + col] for col in range(3)]
            print(f"  {cells[0]} | {cells[1]} | {cells[2]}")
            if row < 2:
                print(" ---+---+---")
        print()

    def _print_guide(self):
        print("  1 | 2 | 3")
        print(" ---+---+---")
        print("  4 | 5 | 6")
        print(" ---+---+---")
        print("  7 | 8 | 9")
        print("(Type 'q' at any prompt to quit.)")

    def _ask_replay(self):
        while True:
            answer = self._read_line("Play again? (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("Please answer 'y' or 'n'.")