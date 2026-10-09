'''
Board model: space definitions, ownership lookup and text rendering.
'''
class Space:
    """One square on the board."""
    def __init__(self, name, kind, price=0, rent=0):
        self.name = name
        self.kind = kind  # "go", "property", "chance", "jail", "free_parking"
        self.price = price
        self.rent = rent
        self.owner = None
class Board:
    """The simplified 24-space Monopoly Go! board."""
    SIZE = 24
    JAIL_POSITION = 16
    FREE_PARKING_POSITION = 10
    GO_POSITION = 0
    GO_SALARY = 200
    def __init__(self):
        self.spaces = self._build()
    def _build(self):
        """Create all board spaces in order."""
        defs = [
            ("GO", "go", 0, 0),
            ("Mediterranean Ave", "property", 60, 10),
            ("Baltic Ave", "property", 60, 12),
            ("Chance", "chance", 0, 0),
            ("Connecticut Ave", "property", 100, 14),
            ("Vermont Ave", "property", 100, 16),
            ("Chance", "chance", 0, 0),
            ("Oriental Ave", "property", 120, 18),
            ("St. Charles Place", "property", 140, 20),
            ("States Ave", "property", 140, 22),
            ("Free Parking", "free_parking", 0, 0),
            ("Virginia Ave", "property", 160, 24),
            ("Pennsylvania Ave", "property", 180, 26),
            ("Chance", "chance", 0, 0),
            ("North Carolina Ave", "property", 180, 28),
            ("Tennessee Ave", "property", 200, 30),
            ("Jail", "jail", 0, 0),
            ("St. James Place", "property", 200, 30),
            ("New York Ave", "property", 220, 34),
            ("Chance", "chance", 0, 0),
            ("Kentucky Ave", "property", 240, 36),
            ("Indiana Ave", "property", 240, 38),
            ("Marvin Gardens", "property", 260, 40),
            ("Park Place", "property", 280, 42),
        ]
        return [Space(name, kind, price, rent) for (name, kind, price, rent) in defs]