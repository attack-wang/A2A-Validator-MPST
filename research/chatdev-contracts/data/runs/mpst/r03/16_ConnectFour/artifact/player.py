'''
Module: player.py
Defines the Player class for the Connect Four game. Each player owns a
name and a disc symbol ('X' or 'O') and is responsible for reading and
validating column choices from the keyboard before a move is applied.
Column input is converted inside a try/except guard so that any
non-numeric input -- including Unicode digit characters such as '²'
that pass isdigit() but crash int() -- is safely rejected with a
re-prompt instead of terminating the program. An EOFError (stdin
exhausted or closed, e.g. under an automated test harness) is reported
with a clear message and re-raised so the session terminates cleanly;
it must NOT be swallowed with continue, or the prompt loop would spin
forever re-raising EOF on every iteration.
'''
class Player:
    """Represents one participant and their keyboard input for a move."""
    def __init__(self, name, disc):
        """Create a player with a display name and a one-character disc symbol."""
        self.name = name
        self.disc = disc
    def get_move(self, board):
        """Prompt until the player enters a valid, non-full column; return its 0-based index."""
        while True:
            try:
                raw = input(f"{self.name} ({self.disc}), choose a column "
                            f"(1-{board.cols}): ").strip()
            except EOFError:
                # stdin exhausted (non-interactive run / closed stream).
                # Terminate cleanly -- do NOT continue, or the loop spins forever.
                print(f"\nNo more input available. {self.name} cannot move. Game over.")
                raise
            try:
                col = int(raw) - 1
            except ValueError:
                print("Invalid input: please type a number.")
                continue
            if not 0 <= col < board.cols:
                print(f"Out of range: please choose a column between 1 and {board.cols}.")
                continue
            if not board.is_valid_column(col):
                print("That column is already full. Pick a different one.")
                continue
            return col