class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current = "X"

    def display(self):
        print()
        print("    1   2   3")
        for i, row in enumerate(self.board):
            print(f"  {i + 1} " + " | ".join(row))
            if i < 2:
                print("   ---+---+---")
        print()

    def make_move(self, row, col):
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == " ":
            self.board[row][col] = self.current
            return True
        return False

    def check_win(self):
        b = self.board
        lines = [
            b[0], b[1], b[2],
            [b[0][0], b[1][0], b[2][0]],
            [b[0][1], b[1][1], b[2][1]],
            [b[0][2], b[1][2], b[2][2]],
            [b[0][0], b[1][1], b[2][2]],
            [b[0][2], b[1][1], b[2][0]],
        ]
        return any(line[0] != " " and line[0] == line[1] == line[2] for line in lines)

    def is_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def switch(self):
        self.current = "O" if self.current == "X" else "X"

    @staticmethod
    def read_input(prompt):
        try:
            return input(prompt).strip().lower()
        except EOFError:
            print()
            return "q"
        except KeyboardInterrupt:
            print()
            return "q"

    def play(self):
        print("Welcome to Tic-Tac-Toe!")
        print("Player X and Player O take turns.")
        print("Enter moves as 'row column' (e.g., '2 3'). Type 'q' to quit.")
        while True:
            self.reset()
            while True:
                self.display()
                move = self.read_input(f"Player {self.current}, enter your move (row col): ")
                if move == "q":
                    print("Game ended by player. Goodbye!")
                    return
                parts = move.split()
                if len(parts) != 2 or not all(p.isdigit() for p in parts):
                    print("Invalid input. Enter two numbers between 1 and 3.")
                    continue
                row, col = int(parts[0]) - 1, int(parts[1]) - 1
                if not self.make_move(row, col):
                    print("That cell is taken or out of range. Try again.")
                    continue
                if self.check_win():
                    self.display()
                    print(f"Player {self.current} wins! Congratulations!")
                    break
                if self.is_full():
                    self.display()
                    print("It's a draw! The board is full.")
                    break
                self.switch()
            again = self.read_input("Play again? (y/n): ")
            if again != "y":
                print("Thanks for playing! Goodbye.")
                return