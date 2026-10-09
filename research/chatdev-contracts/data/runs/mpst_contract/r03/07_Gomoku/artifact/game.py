"""Game loop for Gomoku."""
from board import Board, EMPTY, BLACK, WHITE


class Game:
    def __init__(self):
        self.board = Board()
        self.current = BLACK

    def _name(self):
        return "Black (X)" if self.current == BLACK else "White (O)"

    def prompt(self):
        try:
            raw = input(f"{self._name()}, enter row and column (1-15), or 'q' to quit: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return None
        if raw in ("q", "quit", "exit"):
            return None
        parts = raw.replace(",", " ").split()
        if len(parts) != 2:
            print("Invalid input. Enter two numbers, e.g. '8 8'.")
            return False
        try:
            r, c = int(parts[0]) - 1, int(parts[1]) - 1
        except ValueError:
            print("Invalid input. Use numbers 1-15.")
            return False
        if not self.board.is_empty(r, c):
            print("Cell occupied or out of bounds. Try again.")
            return False
        return (r, c)

    def run(self):
        print("=== Gomoku (15x15) ===")
        print("Black is X, White is O. First to five in a row wins.")
        self.board.display()
        while True:
            move = self.prompt()
            if move is None:
                print("Game aborted.")
                return
            if move is False:
                continue
            r, c = move
            self.board.place(r, c, self.current)
            self.board.display()
            if self.board.check_win(r, c):
                print(f"{self._name()} wins!")
                return
            if self.board.full():
                print("Draw: the board is full.")
                return
            self.current = WHITE if self.current == BLACK else BLACK