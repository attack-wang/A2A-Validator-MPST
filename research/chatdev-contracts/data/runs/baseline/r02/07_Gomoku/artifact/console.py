'''
console.py
Text-based console interface for the Gomoku game.
Used as a fallback when tkinter is unavailable.
'''
from board import EMPTY, BLACK, WHITE
STONE_SYMBOLS = {EMPTY: ".", BLACK: "X", WHITE: "O"}
class ConsoleUI:
    """Text-based Gomoku interface."""
    def __init__(self, game):
        self.game = game
    def print_board(self):
        board = self.game.board
        header = "   " + " ".join(f"{i % 10}" for i in range(board.size))
        print(header)
        for r in range(board.size):
            row_str = " ".join(STONE_SYMBOLS[board.get_stone(r, c)]
                               for c in range(board.size))
            print(f"{r:2d} {row_str}")
        print()
    def get_move(self):
        while True:
            raw = input(f"{self.game.current_player}, enter move as 'row col' "
                        f"(0-{self.game.board.size - 1}): ").strip()
            parts = raw.replace(",", " ").split()
            if len(parts) != 2:
                print("Invalid input. Please enter two numbers separated by a space.")
                continue
            try:
                row, col = int(parts[0]), int(parts[1])
            except ValueError:
                print("Invalid input. Please enter integers.")
                continue
            if self.game.board.is_valid_move(row, col):
                return row, col
            print("That cell is out of bounds or already occupied. Try again.")
    def run(self):
        print("=== Gomoku (Five in a Row) ===")
        print("Black plays X and moves first. Enter moves as 'row col'.\n")
        while not self.game.is_over():
            self.print_board()
            row, col = self.get_move()
            self.game.make_move(row, col)
        self.print_board()
        if self.game.state == STATE_DRAW:
            print("The game is a draw!")
        else:
            print(f"{self.game.winner} wins! Five in a row!")