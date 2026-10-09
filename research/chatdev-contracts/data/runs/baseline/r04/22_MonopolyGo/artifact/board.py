"""Board and space definitions for Monopoly Go!"""
from game_constants import BOARD_LAYOUT
class Space:
    """A single square on the board."""
    def __init__(self, index, name, kind):
        self.index = index
        self.name = name
        self.kind = kind
    def __str__(self):
        return f"[{self.index:2d}] {self.name}"
class PropertySpace(Space):
    """A purchasable property with price and rent."""
    def __init__(self, index, name, price, rent):
        super().__init__(index, name, "property")
        self.price = price
        self.rent = rent
        self.owner = None
    @property
    def is_owned(self):
        return self.owner is not None and not self.owner.bankrupt
    def __str__(self):
        owner = self.owner.name if self.owner else "unowned"
        return f"{super().__str__()}  ${self.price} rent ${self.rent} owner: {owner}"
class GoSpace(Space):
    """The GO square."""
    def __init__(self, index, name):
        super().__init__(index, name, "go")
class ChanceSpace(Space):
    """A chance card square."""
    def __init__(self, index, name):
        super().__init__(index, name, "chance")
class JailSpace(Space):
    """Jail / just visiting square."""
    def __init__(self, index, name):
        super().__init__(index, name, "jail")
class FreeParkingSpace(Space):
    """Free parking square (collects the pot)."""
    def __init__(self, index, name):
        super().__init__(index, name, "free_parking")
class GoToJailSpace(Space):
    """Go-to-jail square."""
    def __init__(self, index, name):
        super().__init__(index, name, "go_to_jail")
class Board:
    """Builds the board from BOARD_LAYOUT."""
    def __init__(self):
        self.spaces = []
        for idx, (kind, name, price, rent) in enumerate(BOARD_LAYOUT):
            if kind == "property":
                self.spaces.append(PropertySpace(idx, name, price, rent))
            elif kind == "chance":
                self.spaces.append(ChanceSpace(idx, name))
            elif kind == "jail":
                self.spaces.append(JailSpace(idx, name))
            elif kind == "free_parking":
                self.spaces.append(FreeParkingSpace(idx, name))
            elif kind == "go_to_jail":
                self.spaces.append(GoToJailSpace(idx, name))
            else:  # "go"
                self.spaces.append(GoSpace(idx, name))
    def __len__(self):
        return len(self.spaces)
    def get_space(self, index):
        return self.spaces[index % len(self.spaces)]
    def property_spaces(self):
        return [s for s in self.spaces if isinstance(s, PropertySpace)]