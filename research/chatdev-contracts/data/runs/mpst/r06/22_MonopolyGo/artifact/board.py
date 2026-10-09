'''
board.py
Board module for the simplified Monopoly Go! game.
Defines the different kinds of board spaces (Go, Property, Chance,
Jail, FreeParking, GoToJail) and the Board that ties them together.
'''
class BoardSpace:
    """Base class for all spaces on the board."""
    kind = "space"
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
class GoSpace(BoardSpace):
    kind = "go"
class Property(BoardSpace):
    kind = "property"
    def __init__(self, name, price, rent):
        super().__init__(name)
        self.price = price
        self.rent = rent
        self.owner = None
    @property
    def is_owned(self):
        return self.owner is not None
    def __str__(self):
        owner = self.owner.name if self.owner else "unowned"
        return f"{self.name} (price ${self.price}, rent ${self.rent}, owner: {owner})"
class ChanceSpace(BoardSpace):
    kind = "chance"
class JailSpace(BoardSpace):
    kind = "jail"
class FreeParkingSpace(BoardSpace):
    kind = "free_parking"
class GoToJailSpace(BoardSpace):
    kind = "go_to_jail"
class Board:
    """The game board: an ordered list of spaces plus lookup helpers."""
    def __init__(self, spaces):
        self.spaces = spaces
    @property
    def size(self):
        return len(self.spaces)
    def get_space(self, position):
        return self.spaces[position % self.size]
    def _find_kind(self, kind):
        """Index of the first space of the given kind (0 as fallback)."""
        for i, space in enumerate(self.spaces):
            if space.kind == kind:
                return i
        return 0
    def go_position(self):
        """Index of the GO space."""
        return self._find_kind("go")
    def jail_position(self):
        """Index of the Jail space."""
        return self._find_kind("jail")
    def properties(self):
        return [s for s in self.spaces if s.kind == "property"]
    @classmethod
    def build_default_board(cls):
        """Create the standard 24-space simplified board."""
        spaces = [
            GoSpace("GO"),
            Property("Mediterranean Ave", 60, 10),
            Property("Baltic Ave", 60, 12),
            ChanceSpace("Chance"),
            Property("Oriental Ave", 100, 18),
            Property("Vermont Ave", 100, 20),
            JailSpace("Jail / Just Visiting"),
            Property("Connecticut Ave", 120, 24),
            Property("St. Charles Pl", 140, 28),
            ChanceSpace("Chance"),
            FreeParkingSpace("Free Parking"),
            Property("States Ave", 160, 32),
            Property("Virginia Ave", 160, 36),
            ChanceSpace("Chance"),
            Property("St. James Pl", 180, 40),
            Property("Tennessee Ave", 200, 44),
            GoToJailSpace("Go To Jail"),
            Property("New York Ave", 220, 48),
            Property("Kentucky Ave", 240, 52),
            ChanceSpace("Chance"),
            Property("Indiana Ave", 260, 56),
            Property("Illinois Ave", 280, 60),
            ChanceSpace("Chance"),
            Property("Park Place", 320, 70),
        ]
        return cls(spaces)