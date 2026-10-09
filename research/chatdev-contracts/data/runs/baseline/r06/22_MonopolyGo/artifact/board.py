'''
board.py
Board and space definitions for simplified Monopoly Go!
'''
class Space:
    """A generic board space."""
    def __init__(self, name, kind, amount=0):
        self.name = name
        self.kind = kind  # 'go', 'property', 'chance', 'tax', 'jail', 'free_parking', 'go_to_jail'
        self.amount = amount  # only used by 'tax' spaces
class Property(Space):
    """A purchasable property with a price and a base rent."""
    def __init__(self, name, price, rent, color=None):
        super().__init__(name, 'property')
        self.price = price
        self.base_rent = rent
        self.color = color  # None for railroads/utilities (no colour-group bonus)
        self.owner = None
class Board:
    SIZE = 40
    JAIL_POSITION = 10
    FREE_PARKING_POSITION = 20
    GO_TO_JAIL_POSITION = 30
    def __init__(self):
        self.spaces = self._build()
        self.free_parking_pot = 0
    def _build(self):
        """Create the classic 40-space board (simplified prices/rents)."""
        spaces = [Space('GO', 'go')] + [None] * (self.SIZE - 1)
        props = [
            (1, 'Mediterranean Avenue', 60, 2, 'brown'),
            (3, 'Baltic Avenue', 60, 4, 'brown'),
            (5, 'Reading Railroad', 200, 25, None),
            (6, 'Oriental Avenue', 100, 6, 'light blue'),
            (8, 'Vermont Avenue', 100, 6, 'light blue'),
            (9, 'Connecticut Avenue', 120, 8, 'light blue'),
            (11, 'St. Charles Place', 140, 10, 'pink'),
            (12, 'Electric Company', 150, 12, None),
            (13, 'States Avenue', 140, 10, 'pink'),
            (14, 'Virginia Avenue', 160, 12, 'pink'),
            (15, 'Pennsylvania Railroad', 200, 25, None),
            (16, 'St. James Place', 180, 14, 'orange'),
            (18, 'Tennessee Avenue', 180, 14, 'orange'),
            (19, 'New York Avenue', 200, 16, 'orange'),
            (21, 'Kentucky Avenue', 220, 18, 'red'),
            (23, 'Indiana Avenue', 220, 18, 'red'),
            (24, 'Illinois Avenue', 240, 20, 'red'),
            (25, 'B. & O. Railroad', 200, 25, None),
            (26, 'Atlantic Avenue', 260, 22, 'yellow'),
            (27, 'Ventnor Avenue', 260, 22, 'yellow'),
            (28, 'Water Works', 150, 12, None),
            (29, 'Marvin Gardens', 280, 24, 'yellow'),
            (31, 'Pacific Avenue', 300, 26, 'green'),
            (32, 'North Carolina Avenue', 300, 26, 'green'),
            (34, 'Pennsylvania Avenue', 320, 28, 'green'),
            (35, 'Short Line Railroad', 200, 25, None),
            (37, 'Park Place', 350, 35, 'dark blue'),
            (39, 'Boardwalk', 400, 50, 'dark blue'),
        ]
        for pos, name, price, rent, color in props:
            spaces[pos] = Property(name, price, rent, color)
        for pos in (2, 7, 17, 22, 33, 36):
            spaces[pos] = Space('Chance', 'chance')
        spaces[4] = Space('Income Tax', 'tax', amount=100)
        spaces[38] = Space('Luxury Tax', 'tax', amount=75)
        spaces[self.JAIL_POSITION] = Space('Jail / Just Visiting', 'jail')
        spaces[self.FREE_PARKING_POSITION] = Space('Free Parking', 'free_parking')
        spaces[self.GO_TO_JAIL_POSITION] = Space('Go To Jail', 'go_to_jail')
        return spaces
    def get_space(self, position):
        """Return the space object at `position`."""
        return self.spaces[position % self.SIZE]
    def properties_of_color(self, color):
        """Return all properties of a given colour group."""
        return [s for s in self.spaces if isinstance(s, Property) and s.color == color]
    def owns_full_group(self, player, color):
        """True if `player` owns every property of the colour group."""
        group = self.properties_of_color(color)
        return bool(group) and all(p.owner is player for p in group)
    def rent_for(self, space):
        """Rent due on `space`: doubled when the owner holds the full colour group."""
        if space.owner is None:
            return 0
        if space.color and self.owns_full_group(space.owner, space.color):
            return space.base_rent * 2
        return space.base_rent