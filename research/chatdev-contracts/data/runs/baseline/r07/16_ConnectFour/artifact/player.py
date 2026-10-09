'''
player.py
This module defines the Player class, which represents a participant
in the Connect Four game. Each player owns a name and a disc symbol
and provides an interactive method that repeatedly prompts for a
column choice until a valid one is entered. Input parsing uses a
safe try/except conversion so that any non-numeric entry is rejected
gracefully instead of crashing the input loop, and a closed or
interrupted standard input stream raises InputClosed so the caller
can end the session cleanly rather than terminating with a traceback.
'''
from io_utils import safe_input, InputClosed
class Player:
    """Represents a Connect Four player and handles move input."""
    def __init__(self, name: str, disc: str) -> None:
        """
        Initialize a player.
        Args:
            name: Display name shown in prompts and results.
            disc: Single-character symbol for this player's discs.
        """
        self.name = name
        self.disc = disc
    def get_move(self, board) -> int:
        """
        Prompt the player for a column until the choice is valid.
        A choice is valid when it is a whole number within the
        board's column range and the column is not already full.
        Args:
            board: The Board instance used for validation.
        Returns:
            The chosen column number (1-based).
        Raises:
            InputClosed: If the input stream is closed or
                interrupted, so no move can be read.
        """
        while True:
            raw = safe_input(
                f"{self.name} ({self.disc}) - choose a column "
                f"(1-{board.COLUMNS}): "
            )
            if raw is None:
                print("\nInput stream closed. No further moves can "
                      "be read.")
                raise InputClosed
            raw = raw.strip()
            try:
                column = int(raw)
            except ValueError:
                print(f"  Invalid input '{raw}'. Please type a whole "
                      f"number between 1 and {board.COLUMNS}.")
                continue
            if not board.is_valid_column(column):
                if 1 <= column <= board.COLUMNS:
                    print(f"  Column {column} is already full. "
                          "Choose a different column.")
                else:
                    print(f"  Column {column} is out of range. "
                          f"Pick a number between 1 and {board.COLUMNS}.")
                continue
            return column