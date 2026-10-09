'''
player.py
Defines the Player entity for Connect Four. Each player owns a display
name and a one-character disc symbol ('X' or 'O') that marks their moves
on the board, plus the ability to type in their column choice.
'''
from exceptions import InvalidColumnError
class Player:
    """Represents one of the two participants in a Connect Four match."""
    def __init__(self, name, disc):
        """
        Create a player.
        Args:
            name (str): Human-readable name shown in prompts and banners.
            disc (str): Single-character symbol dropped into columns.
        """
        self._name = name
        self._disc = disc
    @property
    def name(self):
        """Return the player's display name."""
        return self._name
    @property
    def disc(self):
        """Return the disc symbol this player drops into columns."""
        return self._disc
    def choose_column(self, max_column):
        """
        Prompt the player to type a column number and parse it.
        Args:
            max_column (int): Highest legal column (board width, normally 7).
        Returns:
            int: The chosen 1-based column number.
        Raises:
            InvalidColumnError: If the input is not an integer within range.
        """
        prompt = f"{self._name} ({self._disc}), choose a column (1-{max_column}): "
        raw = input(prompt).strip()
        try:
            column = int(raw)
        except ValueError:
            raise InvalidColumnError(raw)
        if not 1 <= column <= max_column:
            raise InvalidColumnError(column)
        return column
    def __str__(self):
        """Return a readable description such as 'Player 1 (X)'."""
        return f"{self._name} ({self._disc})"