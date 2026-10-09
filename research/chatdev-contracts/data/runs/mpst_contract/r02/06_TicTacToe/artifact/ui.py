"""Console user interface for the tic-tac-toe game."""

from game import TicTacToe


class ConsoleUI:
    """Renders the board, prompts players, and reports the result."""

    def show_welcome(self):
        print("\n" + "=" * 39)
        print("TIC - TAC - TOE".center(39))
        print("=" * 39)
        print("Player 1 uses X, Player 2 uses O.")
        print("Pick a cell by entering its number:\n")
        print(" 1 | 2 | 3 ")
        print("---+---+---")
        print(" 4 | 5 | 6 ")
        print("---+---+---")
        print(" 7 | 8 | 9 ")
        print("-" * 39)

    def render(self, game):
        b = game.board
        rows = [" {} | {} | {} ".format(*b[r * 3:(r + 1) * 3]) for r in range(3)]
        print("\n" + "\n---+---+---\n".join(rows) + "\n")

    def read_line(self, prompt):
        """Read a line of input; exit cleanly if the input stream is closed."""
        try:
            return input(prompt)
        except EOFError:
            print("\nInput stream closed. Ending the game. Goodbye!")
            raise SystemExit(0)

    def _parse_choice(self, text):
        try:
            return int(text)
        except (TypeError, ValueError):
            return None

    def play_game(self, game):
        while True:
            self.render(game)
            choice = self._parse_choice(
                self.read_line(
                    f"Player {game.current_player}, choose a cell (1-9): "
                ).strip()
            )
            if choice is None or not game.make_move(choice):
                print("Invalid move. Choose an empty cell numbered 1-9.")
                continue
            winner = game.check_winner()
            if winner or game.is_full():
                self.render(game)
                if winner:
                    print(f"*** Player {winner} wins! ***")
                else:
                    print("It's a draw! The board is full.")
                break
            game.switch_player()

    def ask_replay(self):
        return self.read_line("Play again? (y/n): ").strip().lower().startswith("y")

    def show_goodbye(self):
        print("Thanks for playing! Goodbye.")