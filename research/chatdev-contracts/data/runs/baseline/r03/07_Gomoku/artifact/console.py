'''
console.py
This module implements a terminal-based (console) version of the Gomoku
game, allowing two players to play by entering row and column numbers,
with rematch support after each finished game.
'''
from board import Board
from game import GomokuGame
class GomokuConsole:
    """Console-based Gomoku game loop."""
    SYMBOLS = {Board.EMPTY: ".", Board.BLACK: "X", Board.WHITE: "O"}
    def __init__(self):
        self.game = GomokuGame()
    def print_board(self):
        """Print the board with column and row labels."""
        size = self.game.board.size
        header = "    " + " ".join(f"{c % 10}" for c in range(size))
        print(header)
        for r in range(size):
            row_str = " ".join(self.SYMBOLS[self.game.board.grid[r][c]]
                               for c in range(size))
            print(f"{r:2d}  {row_str}")
    def parse_input(self, text):
        """Parse 'row col' input; returns (row, col) or None."""
        parts = text.split()
        if len(parts) != 2:
            return None
        try:
            row, col = int(parts[0]), int(parts[1])
        except ValueError:
            return None
        return (row, col)
    def play_one_game(self):
        """Play a single game until win, draw, or quit.
        Returns True if the game finished, False if the user quit."""
        while True:
            self.print_board()
            player = self.game.get_current_player()
            prompt = f"{player.name} ({player.stone_name}) - enter move: "
            text = input(prompt).strip()
            if text.lower() in ("q", "quit", "exit"):
                return False
            move = self.parse_input(text)
            if move is None or not self.game.board.is_valid_move(*move):
                print("Invalid move. Please try again.\n")
                continue
            row, col = move
            self.game.make_move(row, col)
            print()
            if self.game.state == GomokuGame.STATE_WON:
                self.print_board()
                print(f"\n🎉 {self.game.winner.name} ({self.game.winner.stone_name}) "
                      "wins with five in a row!")
                return True
            elif self.game.state == GomokuGame.STATE_DRAW:
                self.print_board()
                print("\nThe board is full. It's a draw!")
                return True
    def run(self):
        """Main game loop with rematch support."""
        print("=== Gomoku (Five in a Row) ===")
        print(f"{self.game.player1} moves first.")
        print("Enter moves as: row col (e.g., '7 7'). Type 'q' to quit.\n")
        while True:
            finished = self.play_one_game()
            if not finished:
                print("Thanks for playing! Goodbye.")
                break
            again = input("\nPlay again? (y/n): ").strip().lower()
            if again not in ("y", "yes"):
                print("Thanks for playing! Goodbye.")
                break
            self.game.reset()
            print()