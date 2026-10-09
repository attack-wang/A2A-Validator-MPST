class TicTacToe:
    """Two-player tic-tac-toe on a standard 3x3 grid."""

    WIN_LINES = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),             # diagonals
    ]

    def __init__(self):
        self.board = [" "] * 9
        self.current = "X"

    def display(self):
        print()
        print("     1   2   3 ")
        print("   -----------")
        for row in range(3):
            cells = [self.board[row * 3 + col] for col in range(3)]
            print(f" {row * 3 + 1} | {cells[0]} | {cells[1]} | {cells[2]} ")
            if row < 2:
                print("   -----------")
        print("   -----------")
        print()

    def winner(self):
        for a, b, c in self.WIN_LINES:
            if self.board[a] != " " and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_full(self):
        return " " not in self.board

    def make_move(self, position):
        if 1 <= position <= 9 and self.board[position - 1] == " ":
            self.board[position - 1] = self.current
            return True
        return False

    def switch_player(self):
        self.current = "O" if self.current == "X" else "X"

    def play(self):
        print("=" * 30)
        print("      TIC-TAC-TOE")
        print("=" * 30)
        print("Player 1: X | Player 2: O")
        print("Enter a number 1-9 to place your mark.")
        self.display()

        while True:
            try:
                choice = input(f"Player {self.current}, enter your move (1-9): ").strip()
                position = int(choice)
            except ValueError:
                print("Invalid input. Please enter a number 1-9.")
                continue

            if not self.make_move(position):
                print("That spot is taken or out of range. Try again.")
                continue

            self.display()
            winner = self.winner()
            if winner:
                print(f"*** Player {winner} wins! ***")
                break
            if self.is_full():
                print("*** It's a draw! ***")
                break
            self.switch_player()