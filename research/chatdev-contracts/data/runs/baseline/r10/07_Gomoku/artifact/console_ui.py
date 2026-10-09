'''
console_ui.py
Provides a text-based user interface for playing Gomoku in a terminal.
Handles reading player input (e.g., "H8" or "8 8"), displaying the board,
and printing game status messages.
'''
from board import PLAYER_NAMES
from game import GomokuGame
class ConsoleUI:
    def __init__(self, game):
        self.game = game
    def parse_input(self, text):
        """Parse input like 'H8', 'h8', '8 8' into (row, col) 0-indexed."""
        text = text.strip()
        if not text:
            return None
        parts = text.replace(",", " ").split()
        # Format 1: "8 8" -> 1-indexed row and column numbers.
        if len(parts) == 2 and all(p.isdigit() for p in parts):
            row, col = int(parts[0]) - 1, int(parts[1]) - 1
        # Format 2: "H8" -> column letter + 1-indexed row number.
        elif (len(parts) == 1 and len(parts[0]) >= 2
              and parts[0][0].isalpha() and parts[0][1:].isdigit()):
            col = ord(parts[0][0].upper()) - ord("A")
            row = int(parts[0][1:]) - 1
        else:
            return None
        if self.game.board.is_valid_position(row, col):
            return (row, col)
        return None
    def run(self):
        """Main console loop: show the board, read moves, report the result."""
        print("Welcome to Gomoku! Black (X) moves first.")
        print("Enter a move as 'H8' or '8 8'. Commands: 'undo', 'quit'.")
        while True:
            print("\n" + self.game.board.display())
            print(self.game.get_status_message())
            if self.game.game_over:
                if self.game.winner is not None and self.game.winning_line:
                    cells = ", ".join(
                        f"{chr(ord('A') + c)}{r + 1}" for r, c in self.game.winning_line)
                    print("Winning line: " + cells)
                if self.ask_play_again():
                    self.game.reset()
                    continue
                break
            command = input(f"{PLAYER_NAMES[self.game.current_player]} move: ").strip()
            if command.lower() in ("q", "quit", "exit"):
                break
            if command.lower() in ("u", "undo"):
                if not self.game.undo_move():
                    print("Nothing to undo.")
                continue
            move = self.parse_input(command)
            if move is None:
                print("Invalid input or out of range. Use e.g. 'H8' or '8 8'.")
                continue
            if not self.game.play_move(move[0], move[1]):
                print("That intersection is already occupied. Try again.")
    def ask_play_again(self):
        """Ask whether the players want a rematch."""
        answer = input("Play again? (y/n): ").strip().lower()
        return answer in ("y", "yes")