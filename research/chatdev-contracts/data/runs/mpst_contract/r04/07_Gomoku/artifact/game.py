"""Game loop module for the Gomoku game."""

from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.current = Board.BLACK

    @staticmethod
    def player_name(player):
        return "Black (X)" if player == Board.BLACK else "White (O)"

    @staticmethod
    def parse_move(text):
        parts = text.strip().split()
        if len(parts) != 2:
            return None
        try:
            row, col = int(parts[0]), int(parts[1])
        except ValueError:
            return None
        return row - 1, col - 1

    def run(self):
        print("Gomoku - 15x15 board. Enter moves as 'row col' (1-15). Type 'quit' to exit.")
        while True:
            print()
            print(self.board.render())
            print(f"{self.player_name(self.current)} to move.")
            text = input("Move: ").strip().lower()
            if text in ("quit", "exit", "q"):
                print("Game aborted.")
                return
            move = self.parse_move(text)
            if move is None:
                print("Invalid input. Enter two numbers 1-15, e.g. '8 8'.")
                continue
            row, col = move
            if not self.board.place(row, col, self.current):
                print("That cell is unavailable. Try again.")
                continue
            if self.board.check_win(row, col, self.current):
                print()
                print(self.board.render())
                print(f"{self.player_name(self.current)} wins with five in a row!")
                return
            if self.board.is_full():
                print()
                print(self.board.render())
                print("The board is full. It's a draw.")
                return
            self.current = Board.WHITE if self.current == Board.BLACK else Board.BLACK