'''
board.py
Board module for the simplified Monopoly Go! game.
Defines every kind of board space (properties, chance, jail, taxes, ...)
and the 24-space board layout used by the game.
'''
GO_SALARY = 200
class Space:
    """A single space on the board."""
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind  # e.g. "go", "property", "chance", ...
    def __str__(self):
        return self.name
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name!r}>"
class Property(Space):
    """A purchasable property that charges rent to visitors."""
    def __init__(self, name, price, rent, color):
        super().__init__(name, "property")
        self.price = price
        self.base_rent = rent
        self.color = color
        self.owner = None
    def is_owned(self):
        """True when some player owns this property."""
        return self.owner is not None
    def calculate_rent(self, board):
        """Base rent, doubled when the owner holds a full colour group."""
        rent = self.base_rent
        if self.owner is not None and board.has_monopoly(self.owner, self.color):
            rent *= 2
        return rent
class GoSpace(Space):
    """The GO corner: collecting salary for passing/landing."""
    def __init__(self):
        super().__init__("GO", "go")
class ChanceSpace(Space):
    """Draw a chance card."""
    def __init__(self):
        super().__init__("Chance", "chance")
class JailSpace(Space):
    """Jail square — 'just visiting' unless the player was sent here."""
    def __init__(self):
        super().__init__("Jail", "jail")
class GoToJailSpace(Space):
    """Landing here sends the player straight to Jail."""
    def __init__(self):
        super().__init__("Go To Jail", "go_to_jail")
class FreeParkingSpace(Space):
    """Free Parking — landing here wins the accumulated pot."""
    def __init__(self):
        super().__init__("Free Parking", "free_parking")
class TaxSpace(Space):
    """Tax square — the payment goes into the free-parking pot."""
    def __init__(self, name, amount):
        super().__init__(name, "tax")
        self.amount = amount
class Board:
    """The 24-space simplified Monopoly board."""
    SIZE = 24
    GO_POSITION = 0
    JAIL_POSITION = 5
    FREE_PARKING_POSITION = 11
    GO_TO_JAIL_POSITION = 15
    def __init__(self):
        self.spaces = self._build_spaces()
    def _build_spaces(self):
        """Construct the fixed 24-space layout."""
        return [
            GoSpace(),                                            # 0  GO
            Property("Mediterranean Ave", 60, 2, "brown"),        # 1
            Property("Baltic Ave", 60, 4, "brown"),               # 2
            ChanceSpace(),                                        # 3
            TaxSpace("Income Tax", 100),                          # 4
            JailSpace(),                                          # 5  JAIL
            Property("Oriental Ave", 100, 6, "light blue"),       # 6
            Property("Vermont Ave", 100, 6, "light blue"),        # 7
            Property("Connecticut Ave", 120, 8, "light blue"),    # 8
            ChanceSpace(),                                        # 9
            Property("St. Charles Place", 140, 10, "pink"),       # 10
            FreeParkingSpace(),                                   # 11 FREE PARKING
            Property("States Ave", 140, 10, "pink"),              # 12
            Property("Virginia Ave", 160, 12, "pink"),            # 13
            TaxSpace("Luxury Tax", 75),                           # 14
            GoToJailSpace(),                                      # 15 GO TO JAIL
            Property("St. James Place", 180, 14, "orange"),       # 16
            Property("Tennessee Ave", 180, 14, "orange"),         # 17
            ChanceSpace(),                                        # 18
            Property("New York Ave", 200, 16, "orange"),          # 19
            Property("Kentucky Ave", 220, 18, "red"),             # 20
            Property("Indiana Ave", 220, 18, "red"),              # 21
            Property("Illinois Ave", 240, 20, "red"),             # 22
            Property("Boardwalk", 400, 50, "dark blue"),          # 23
        ]
    def get_space(self, position):
        """Return the space at `position` (wrapping around the board)."""
        return self.spaces[position % self.SIZE]
    def properties(self):
        """All purchasable properties on the board."""
        return [s for s in self.spaces if isinstance(s, Property)]
    def has_monopoly(self, player, color):
        """True when `player` owns every property of the given colour group."""
        group = [p for p in self.properties() if p.color == color]
        if not group:
            return False
        return all(p.owner is player for p in group)
    def render(self, players):
        """Simple text listing of the board with player positions."""
        lines = []
        for i, space in enumerate(self.spaces):
            here = [p.name for p in players if p.position == i and not p.bankrupt]
            marker = f" <- {', '.join(here)}" if here else ""
            owner = ""
            if isinstance(space, Property) and space.is_owned():
                owner = f" [owned by {space.owner.name}]"
            lines.append(f"  {i:2d}. {space.name}{owner}{marker}")
        return "\n".join(lines)