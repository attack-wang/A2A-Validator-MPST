'''
board.py
Board layout and rendering for the simplified Monopoly Go! game.
Defines the individual space types (GO, properties, chance, tax, jail,
free parking, go-to-jail) and the Board class that builds the 24-space
track, answers position queries and prints a text rendering of the board.
'''
from utils import divider
class Space:
    """Base class for one square on the board."""
    def __init__(self, position, name, space_type):
        self.position = position
        self.name = name
        self.space_type = space_type
class PropertySpace(Space):
    """A purchasable property with a price and a flat rent."""
    def __init__(self, position, name, price, rent):
        super().__init__(position, name, "property")
        self.price = price
        self.rent = rent
        self.owner = None  # Player instance or None (Bank)
    def owner_name(self):
        return self.owner.name if self.owner is not None else "Bank"
    def is_owned(self):
        return self.owner is not None
class TaxSpace(Space):
    """A tax square whose payment feeds the Free Parking pot."""
    def __init__(self, position, name, amount):
        super().__init__(position, name, "tax")
        self.amount = amount
class ChanceSpace(Space):
    """A square that draws a card from the chance deck."""
    def __init__(self, position, name="Chance"):
        super().__init__(position, name, "chance")
class GoSpace(Space):
    """The GO square; passing it pays the GO bonus."""
    def __init__(self, position=0, name="GO"):
        super().__init__(position, name, "go")
class JailSpace(Space):
    """Jail square; landing here is 'just visiting'."""
    def __init__(self, position, name="Jail"):
        super().__init__(position, name, "jail")
class FreeParkingSpace(Space):
    """Free Parking square; landing here collects the pot."""
    def __init__(self, position, name="Free Parking"):
        super().__init__(position, name, "free_parking")
class GoToJailSpace(Space):
    """Go To Jail square; landing here sends the player to jail."""
    def __init__(self, position, name="Go To Jail"):
        super().__init__(position, name, "go_to_jail")
class Board:
    """The 24-space simplified Monopoly Go! board."""
    SIZE = 24
    GO_BONUS = 200
    JAIL_POSITION = 6
    FREE_PARKING_POSITION = 12
    def __init__(self):
        self.spaces = self._build()
    @property
    def size(self):
        return self.SIZE
    def _build(self):
        layout = [
            GoSpace(0),
            PropertySpace(1, "Mediterranean Ave", 60, 10),
            PropertySpace(2, "Baltic Ave", 60, 10),
            ChanceSpace(3),
            PropertySpace(4, "Oriental Ave", 100, 20),
            TaxSpace(5, "Income Tax", 100),
            JailSpace(Board.JAIL_POSITION),
            PropertySpace(7, "Vermont Ave", 100, 20),
            PropertySpace(8, "Connecticut Ave", 120, 30),
            ChanceSpace(9),
            PropertySpace(10, "St. Charles Place", 140, 40),
            PropertySpace(11, "States Ave", 140, 40),
            FreeParkingSpace(Board.FREE_PARKING_POSITION),
            PropertySpace(13, "Virginia Ave", 160, 50),
            PropertySpace(14, "St. James Place", 180, 60),
            ChanceSpace(15),
            PropertySpace(16, "Tennessee Ave", 180, 60),
            PropertySpace(17, "New York Ave", 200, 70),
            GoToJailSpace(18),
            PropertySpace(19, "Kentucky Ave", 220, 80),
            TaxSpace(20, "Luxury Tax", 75),
            PropertySpace(21, "Ventnor Ave", 240, 90),
            ChanceSpace(22),
            PropertySpace(23, "Boardwalk", 400, 150),
        ]
        return layout
    def get_space(self, position):
        """Return the space at the given (wrapped) position."""
        return self.spaces[position % self.SIZE]
    def properties_owned_by(self, player):
        """Return all property spaces currently owned by the player."""
        return [s for s in self.spaces
                if isinstance(s, PropertySpace) and s.owner is player]
    def display(self, players):
        """Print a text rendering of the board with owners and player tokens."""
        print(divider("BOARD"))
        for s in self.spaces:
            detail = ""
            if isinstance(s, PropertySpace):
                detail = f"price ${s.price:<3} rent ${s.rent:<3} owner: {s.owner_name()}"
            elif isinstance(s, TaxSpace):
                detail = f"tax ${s.amount} -> Free Parking pot"
            tokens = "".join(p.token for p in players
                             if p.position == s.position and not p.bankrupt)
            token_note = f"  << {tokens} >>" if tokens else ""
            print(f"[{s.position:>2}] {s.name:<20} {s.space_type:<12} {detail}{token_note}")
        print(divider())