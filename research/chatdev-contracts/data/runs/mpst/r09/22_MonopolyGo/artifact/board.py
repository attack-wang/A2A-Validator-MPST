'''
board.py
Defines the board spaces (Go, Property, Chance, Tax, Jail, GoToJail,
FreeParking) and the Board class that builds the simplified 24-tile
Monopoly Go! board, moves players, and renders an ASCII view of the board.
'''
BOARD_SIZE = 24
GO_SALARY = 200
JAIL_POSITION = 12
JAIL_FINE = 50
class Space:
    kind = "space"
    def __init__(self, name, position, short=None):
        self.name = name
        self.position = position
        self.short = short or name
    def __str__(self):
        return self.name
class Go(Space):
    kind = "go"
class Property(Space):
    kind = "property"
    def __init__(self, name, position, price, rent, short=None):
        super().__init__(name, position, short)
        self.price = price
        self.rent = rent
        self.owner = None
    @property
    def is_available(self):
        return self.owner is None
class Chance(Space):
    kind = "chance"
class Tax(Space):
    kind = "tax"
    def __init__(self, name, position, amount, short=None):
        super().__init__(name, position, short)
        self.amount = amount
class Jail(Space):
    kind = "jail"
class GoToJail(Space):
    kind = "go_to_jail"
class FreeParking(Space):
    kind = "free_parking"
class Board:
    def __init__(self):
        self.spaces = self._build()
        self.pot = 0  # Free Parking pot
    @staticmethod
    def _build():
        s = [None] * BOARD_SIZE
        s[0] = Go("GO", 0, "GO")
        s[1] = Property("Mediterranean Avenue", 1, 60, 10, "Med Ave")
        s[2] = Chance("Chance", 2, "Chance")
        s[3] = Property("Baltic Avenue", 3, 60, 12, "Baltic Ave")
        s[4] = Tax("Income Tax", 4, 100, "Income Tax")
        s[5] = Property("Reading Railroad", 5, 200, 50, "Reading RR")
        s[6] = Property("Oriental Avenue", 6, 100, 20, "Oriental")
        s[7] = Chance("Chance", 7, "Chance")
        s[8] = Property("Vermont Avenue", 8, 100, 20, "Vermont")
        s[9] = Property("Connecticut Avenue", 9, 120, 24, "Connecticut")
        s[10] = Property("St. Charles Place", 10, 140, 28, "St. Charles")
        s[11] = Property("Electric Company", 11, 150, 40, "Electric Co")
        s[12] = Jail("Jail", 12, "JAIL")
        s[13] = Property("States Avenue", 13, 140, 28, "States Ave")
        s[14] = Property("Virginia Avenue", 14, 160, 32, "Virginia")
        s[15] = Property("Pennsylvania Railroad", 15, 200, 50, "Penn RR")
        s[16] = Property("St. James Place", 16, 180, 36, "St. James")
        s[17] = Chance("Chance", 17, "Chance")
        s[18] = Property("Tennessee Avenue", 18, 180, 36, "Tennessee")
        s[19] = FreeParking("Free Parking", 19, "FREE PARK")
        s[20] = Property("New York Avenue", 20, 200, 40, "New York")
        s[21] = GoToJail("Go To Jail", 21, "GO 2 JAIL")
        s[22] = Property("Kentucky Avenue", 22, 220, 44, "Kentucky")
        s[23] = Property("Boardwalk", 23, 400, 80, "Boardwalk")
        return s
    def get_space(self, position):
        return self.spaces[position % BOARD_SIZE]
    def move_forward(self, player, steps):
        """Move player forward; returns True if they passed/landed on GO."""
        target = player.position + steps
        passed_go = target >= BOARD_SIZE
        player.position = target % BOARD_SIZE
        return passed_go
    def move_backward(self, player, steps):
        player.position = (player.position - steps) % BOARD_SIZE
    def teleport(self, player, position):
        player.position = position % BOARD_SIZE
    def add_to_pot(self, amount):
        self.pot += amount
    def take_pot(self):
        amount, self.pot = self.pot, 0
        return amount
    def properties_owned_by(self, player): ...