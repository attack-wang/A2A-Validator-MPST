'''
board.py
Board definition: spaces, properties, special spaces.
'''
class Space:
    """A generic board space."""
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind  # 'go', 'property', 'chance', 'jail', 'free_parking', 'go_to_jail', 'tax'
    def describe(self):
        """Return a short human-readable description of the space."""
        return f"{self.name} ({self.kind})"
class Property(Space):
    """A purchasable property with a fixed price and rent."""
    def __init__(self, name, price, rent):
        super().__init__(name, 'property')
        self.price = price
        self.rent = rent
        self.owner = None
    def is_owned(self):
        """Return True if the property has an owner."""
        return self.owner is not None
    def rent_due(self):
        """Return the rent owed when another player lands here."""
        return self.rent
class Board:
    """The fixed 24-space Monopoly Go! board."""
    SIZE = 24
    def __init__(self):
        self.spaces = self._build()
    def _build(self):
        """Construct the full board layout (Jail must sit at index 5)."""
        spaces = [Space("GO", 'go')]
        layout = [
            Property("Old Kent Road", 60, 10),        # 1
            Space("Chance", 'chance'),                # 2
            Property("Whitechapel Road", 60, 12),     # 3
            Space("Income Tax", 'tax'),               # 4
            Space("Jail / Just Visiting", 'jail'),    # 5 == Player.JAIL_POSITION
            Property("Oriental Avenue", 100, 16),     # 6
            Property("Vermont Avenue", 100, 16),      # 7
            Space("Chance", 'chance'),                # 8
            Property("Connecticut Avenue", 120, 20),  # 9
            Space("Free Parking", 'free_parking'),    # 10
            Property("St. Charles Place", 140, 24),   # 11
            Property("States Avenue", 140, 24),       # 12
            Space("Chance", 'chance'),                # 13
            Property("Virginia Avenue", 160, 28),     # 14
            Space("Go To Jail", 'go_to_jail'),        # 15
            Property("St. James Place", 180, 32),     # 16
            Property("Tennessee Avenue", 180, 32),    # 17
            Space("Chance", 'chance'),                # 18
            Property("New York Avenue", 200, 36),     # 19
            Space("Luxury Tax", 'tax'),               # 20
            Property("Kentucky Avenue", 220, 40),     # 21
            Space("Chance", 'chance'),                # 22
            Property("Indiana Avenue", 220, 40),      # 23
        ]
        spaces.extend(layout)
        return spaces