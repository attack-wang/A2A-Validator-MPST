"""Board module: defines spaces, properties, and the game board."""
from constants import BOARD_LAYOUT, ... 
class Space:
    """A single space on the board."""
    def __init__(self, kind, name):
        self.kind = kind  # 'go', 'property', 'chance', 'jail', 'free_parking', 'go_to_jail'
        self.name = name
class Property(Space):
    """A purchasable property with a price and rent."""
    def __init__(self, name, price, rent):
        super().__init__("property", name)
        self.price = price
        self.rent = rent
        self.owner = None
    @property
    def is_owned(self):
        return self.owner is not None
    @property
    def is_mortgaged...  # skip mortgaging for simplicity
class Board:
    """The game board: a circular list of spaces."""
    def __init__(self):
        self.spaces = []
        self._build()
    def _build(self):
        for entry in BOARD_LAYOUT:
            kind = entry[0]
            if kind == "property":
                self.spaces.append(Property(entry[1], entry[2], entry[3]))
            else:
                self.spaces.append(Space(kind, entry[1]))
    def size(self):
        return len(self.spaces)
    def get_space(self, position):
        return self.spaces[position % len(self.spaces)]
    def unowned_properties(self):
        return [s for s in self.spaces if isinstance(s, Property) and s.owner is None]
    def properties_owned_by(self, player):
        return [s for s in self.spaces if isinstance(s, Property) and s.owner is player]