'''
player.py
Defines the Player class used by the Connect Four game. Each Player owns a
name and a disc symbol ('X' or 'O') and is responsible for reading and
validating their own column choice from the console. Input-stream
interruptions (EOF or Ctrl+C) are handled gracefully and treated as a quit.
'''
from typing import Optional
from board import Board
class Player:
    """Represents a Connect Four player with a name and a disc symbol."""
    def __init__(self, name: str, disc: str) -> None:
        """Initialize the player with a name and a one-character disc."""
        self.name: str = name
        self.disc: str = disc
    def get_move(self, board: Board) -> Optional[int]:
        """
        Prompt the player for a column choice until the input is valid.
        Return the zero-based column index, or None if the player quits
        (via 'q', EOF, or Ctrl+C).
        """
        while True:
            try:
                raw = input(
                    f"{self.name} ({self.disc}), choose a column "
                    f"(1-{board.cols}, or 'q' to quit): "
                ).strip()
            except (EOFError, KeyboardInterrupt):
                # Input stream closed or user interrupted: treat as quit.
                print()
                return None
            if raw.lower() == 'q':
                return None
            try:
                col = int(raw) - 1
            except ValueError:
                print("Invalid input: please enter a number.")
                continue
            if not board.is_valid_column(col):
                if 0 <= col < board.cols:
                    print("That column is full. Choose another one.")
                else:
                    print(f"Column must be between 1 and {board.cols}.")
                continue
            return col