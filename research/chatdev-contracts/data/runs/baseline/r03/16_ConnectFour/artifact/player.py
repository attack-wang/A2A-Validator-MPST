'''
Player module for the Connect Four game.
Defines the Player class, which stores each participant's display
name and the disc symbol used to mark their cells on the board.
'''
class Player:
    """Represents a single Connect Four participant."""
    def __init__(self, name: str, disc: str) -> None:
        """Initialize the player with a display name and a disc symbol."""
        self.name = name
        self.disc = disc
    def __str__(self) -> str:
        """Return a readable label such as 'Player 1 (X)'."""
        return f"{self.name} ({self.disc})"