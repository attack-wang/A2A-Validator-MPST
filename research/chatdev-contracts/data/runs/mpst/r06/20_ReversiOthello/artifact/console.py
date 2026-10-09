"""
console.py
Text-mode front end for the Reversi (Othello) game.
Runs in any terminal: draws the board with ASCII art, highlights legal
moves, reads moves typed as coordinates (e.g. `d3` or `4 5`) and prints
the running score after every turn.
"""
import string
from board import BLACK, WHITE, COLOR_NAMES
from game import Game
CELL_LETTERS = string.ascii_uppercase  # 'A', 'B', ... for columns
def parse_move(text, size):
    """
    Convert user input into a (row, col) tuple.
    Accepts chess-like coordinates such as `d3` / `D3` or two numbers
    separated by a space or comma such as `3 4` / `3,4` (1-based rows).
    Returns None when the input cannot be parsed.
    """
    text = text.strip().lower().replace(",", " ")
    parts = text.split()
    if len(parts) == 1 and len(parts[0]) >= 2:
        col_letter, row_digits = parts[0][0], parts[0][1:]
        if col_letter.isalpha() and row_digits.isdigit():
            col = ord(col_letter) - ord('a')
            row = int(row_digits) - 1
            if 0 <= row < size and 0 <= col < size:
                return row, col
        return None
    if len(parts) == 2 and all(p.isdigit() for p in parts):
        row, col = int(parts[0]) - 1, int(parts[1]) - 1
        if 0 <= row < size and 0 <= col < size:
            return row, col
    return None
class ReversiConsole:
    """Interactive terminal version of Reversi for two local players."""
    def __init__(self, game=None):
        self.game = game or Game()
    def run(self):
        """Main loop: draw, read moves and report results until quit."""
        print("=== Reversi (Othello) ===")
        print("Black is 'X', White is 'O'. Black moves first.")
        print("Enter moves as a column letter + row number (e.g. 'd3')")
        print("or as 'row col' (e.g. '4 5'). Type 'q' to quit.\n")
        while not self.game.game_over:
            self.game.auto_pass_if_needed()
            if self.game.game_over:
                break
            self.show_status()
            move = self.read_move()
            if move is None:
                continue  # user quit or gave an unusable answer
            row, col = move
            if not self.game.apply_move(row, col):
                print("That is not a legal move - try again.\n")
        self.show_status()
        self.announce_result()
    ...