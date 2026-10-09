"""Player module: defines the Player class for Monopoly Go!"""
class Player:
    """Represents a player in the game, tracking money, position, and assets."""
    def __init__(self, name, starting_money):
        self.name = name
        self.money = starting_money
        self.position = 0
        self.properties = []  # list of Property objects owned
        self.in_jail = False
        self.jail_turns = 0  # consecutive turns spent in jail
        self.get_out_of_jail_cards = 0
        self.bankrupt = False
    def receive(self, amount):
        """Add money to the player's balance."""
        self.money += amount
    def pay(self, amount):
        """
        Attempt to pay amount.
        Returns True if fully paid, False if the player cannot afford it.
        (Caller decides how to handle bankruptcy.)
        """
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    def pay_all(self, amount):
        """Pay as much as possible (used when going bankrupt). Returns amount actually paid."""
        paid = min(self.money, amount)
        self.money -= paid
        return paid
    def is_bankrupt(self):
        return self.bankrupt
    def net_worth(self):
        """Total worth: cash + property purchase values."""
        return self.money + sum(p.price for p in self.properties)
    def move(self, steps, board_size):
        """Move forward by steps, wrapping around the board. Returns True if passed GO."""
        old = self.position
        self.position = (self.position + steps) % board_size
        return self.position <= old and (old + steps) >= board_size  # passed GO