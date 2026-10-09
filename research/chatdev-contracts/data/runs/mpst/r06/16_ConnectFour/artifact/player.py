'''
player.py
Defines the Player class representing one Connect Four participant. Each
player owns a name and a disc symbol and is responsible for reading a
validated column choice from the console. A closed input stream (EOFError)
is reported with a clear message and re-raised so the top level can exit
cleanly instead of crashing with a traceback.
'''
class Player:
    """A Connect Four participant and their console input behaviour."""
    def __init__(self, name, disc):
        """
        Create a player.
        Args:
            name (str): Human-readable player name.
            disc (str): The symbol this player drops ('X' or 'O').
        """
        self.name = name
        self.disc = disc
    def get_move(self, board):
        """
        Prompt the player until they supply a valid, non-full column.
        Args:
            board (Board): The current game board used for validation.
        Returns:
            int: Zero-based index of the chosen column.
        Raises:
            EOFError: If the input stream is closed; re-raised after
                printing a friendly message so the top level exits cleanly.
        """
        while True:
            try:
                raw = input("{}, choose a column (1-{}): "
                            .format(self.name, board.cols)).strip()
            except EOFError:
                print("\nInput stream closed: no further moves can be read.")
                raise
            # isdecimal() guarantees int() will succeed; isdigit() would
            # also accept characters like '²' that crash int().
            if not raw.isdecimal():
                print("Invalid input: please type a number.")
                continue
            col = int(raw) - 1
            if col < 0 or col >= board.cols:
                print("Column out of range: pick between 1 and {}."
                      .format(board.cols))
                continue
            if not board.is_valid_column(col):
                print("Column {} is full: choose another one."
                      .format(col + 1))
                continue
            return col