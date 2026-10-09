class ConsoleUI:
    """User-friendly console interface for the tic-tac-toe game."""

    def show_welcome(self):
        print("=== Tic-Tac-Toe ===")
        print("Two players alternate placing X and O on a 3x3 grid.")
        print("Enter moves as: row column (e.g., 1 2). Rows and columns are 1-3.")
        print("The game ends when a player wins or the board is full.\n")

    def render(self, game):
        print(f"Player {game.current_player}'s turn.")
        print("  1   2   3")
        for idx, row in enumerate(game.board, start=1):
            print(f"{idx} " + " | ".join(row))
            if idx < 3:
                print("  ---------")
        print()

    def get_move(self, player):
        """Prompt until the player enters two valid numbers in 1-3."""
        while True:
            raw = input(f"Player {player}, enter row and column (1-3): ").strip().split()
            if len(raw) == 2 and all(p.isdigit() and 1 <= int(p) <= 3 for p in raw):
                return int(raw[0]) - 1, int(raw[1]) - 1
            print("Invalid input. Please enter two numbers between 1 and 3.")

    def show_invalid(self):
        print("That cell is already taken or out of range. Try again.\n")

    def show_result(self, winner):
        if winner:
            print(f"Player {winner} wins! Congratulations!")
        else:
            print("It's a draw! The board is full.")