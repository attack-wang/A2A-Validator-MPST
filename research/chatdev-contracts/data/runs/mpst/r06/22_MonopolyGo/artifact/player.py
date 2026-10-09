'''
player.py
Player module for the simplified Monopoly Go! game.
Defines the Player class, which tracks a player's money, board position,
owned properties, and jail status, and provides money/property operations.
'''
STARTING_MONEY = 1500
GO_SALARY = 200
JAIL_FINE = 50
class Player:
    """Represents a single player, their cash, position and assets."""
    def __init__(self, name, money=STARTING_MONEY):
        self.name = name
        self.money = money
        self.position = 0
        self.properties = []          # list of Property objects owned
        self.in_jail = False
        self.jail_turns = 0           # failed attempts to roll doubles
        self.bankrupt = False
    # ----- money -----------------------------------------------------
    def receive(self, amount):
        self.money += amount
        return self.money
    def pay(self, amount):
        """Attempt to pay. Returns True if fully paid, False if bankrupt."""
        if self.money >= amount:
            self.money -= amount
            return True
        # Pay everything they have and go bankrupt (simplified rule).
        self.money = 0
        self.bankrupt = True
        return False
    def can_afford(self, amount):
        return self.money >= amount
    def net_worth(self):
        return self.money + sum(p.price for p in self.properties)
    # ----- properties -------------------------------------------------
    def buy(self, property):
        """Buy a property (assumes affordability checked by caller)."""
        self.money -= property.price
        property.owner = self
        self.properties.append(property)
    def owns(self, property):
        return property in self.properties
    # ----- movement / jail ---------------------------------------------
    def move(self, steps, board_size):
        """Advance `steps` spaces, wrapping around the board.
        Returns True if GO was passed (or landed on)."""
        start = self.position
        self.position = (self.position + steps) % board_size
        # Passed or landed on GO (wrapped around the board)
        return self.position < start or (start + steps) >= board_size
    def send_to_jail(self, jail_position):
        self.position = jail_position
        self.in_jail = True
        self.jail_turns = 0
    def leave_jail(self):
        self.in_jail = False
        self.jail_turns = 0
    def is_bankrupt(self):
        return self.bankrupt