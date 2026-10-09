'''
cli.py
Console user interface: welcome banner, board rendering, move prompts,
and end-of-game messages. Move prompts detect a closed input stream
(EOFError) and re-raise it so the game loop can terminate gracefully
instead of crashing or retrying forever.
'''
class CLI:
    """Handles every piece of console input and output for the game."""
    def display_welcome(self):
        """Print the welcome banner and short instructions."""
        print("=" * 46)
        print("            WELCOME TO CONNECT FOUR!")
        print("   Two players alternate dropping discs into")
        print("   a 6-row x 7-column grid. Type a column")
        print("   number (1-7) on your turn. Four in a row")
        print("   horizontally, vertically or diagonally wins!")
        print("=" * 46)
    def display_board(self, board):
        """Print the current grid with column numbers above it."""
        header = " ".join(str(col + 1) for col in range(board.cols))
        print("\n " + header)
        for row in board.grid:
            cells = "|".join(cell if cell is not None else "." for cell in row)
            print("|" + cells + "|")
        print("+" + "-" * (2 * board.cols - 1) + "+")
        print()
    def prompt_column(self, player, num_cols):
        """Ask the player for a column number.
        Returns the number as an int, or None when the input is not a
        valid integer (a warning is printed in that case).
        Raises EOFError when the input stream is closed or exhausted.
        EOF is deliberately NOT mapped to None: None means "invalid
        input, try again" and returning it here would cause an
        infinite prompt loop. Re-raising lets Game.play end the match
        cleanly.
        """
        try:
            raw = input(f"{player.name} ({player.disc}), choose a column (1-{num_cols}): ").strip()
        except EOFError:
            # Input stream closed (piped input exhausted, Ctrl+D/Ctrl+Z).
            # Propagate so the caller can stop the game gracefully.
            raise
        try:
            return int(raw)
        except ValueError:
            self.display_invalid_input()
            return None
    def display_invalid_input(self):
        """Warn that the entered text was not a number."""
        print("Invalid input: please type a number.")
    def display_invalid_column(self):
        """Warn that the chosen column is out of range or already full."""
        print("Invalid column: out of range or already full. Try again.")
    def display_winner(self, player):
        """Announce the player who aligned four discs."""
        print(f"\n*** {player.name} ({player.disc}) wins! ***")
    def display_draw(self):
        """Announce that the grid is full and the game is a draw."""
        print("\nThe grid is full - it's a draw!")