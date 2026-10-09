'''
player.py
Player class: a named participant controlling one piece color.
'''
class Player:
    """A checkers player identified by name and piece color."""
    def __init__(self, name, color):
        """Create a player with a display name and a Piece color."""
        self.name = name
        self.color = color
    def __str__(self):
        """Readable form used in prompts and results, e.g. 'Player 1 (BLACK)'."""
        return f"{self.name} ({self.color})"