'''
player.py
Defines the Player class for Simplified Monopoly Go!.
Tracks each player's money, board position, owned properties, jail state,
Get Out of Jail Free cards, and bankruptcy status, and computes net worth
(cash + property purchase prices) used to declare the winner.
'''
class Player:
    STARTING_MONEY = 1500
    def __init__(self, name, money=STARTING_MONEY):
        self.name = name
        self.money = money
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.jail_free_cards = []   # Get Out of Jail Free cards (used by chance.py and game.py)
        self.bankrupt = False
    def receive(self, amount):
        """Add money to the player's cash."""
        self.money += amount
    def pay(self, amount):
        """Attempt to pay; returns the amount actually paid (capped at available cash)."""
        paid = min(self.money, amount)
        self.money -= paid
        return paid
    def is_bankrupt(self):
        """Return True if the Game has declared this player bankrupt."""
        return self.bankrupt
    def net_worth(self):
        """Cash plus the purchase price of every owned property."""
        return self.money + sum(prop.price for prop in self.properties)