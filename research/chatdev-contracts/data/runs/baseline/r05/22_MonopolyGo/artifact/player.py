'''
player.py
Player module for the simplified Monopoly Go! game.
Tracks each player's money, position, properties, jail state and bankruptcy.
'''
class Player:
    """A player in the simplified Monopoly Go! game."""
    def __init__(self, name, starting_money=1500):
        self.name = name
        self.money = starting_money
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.jail_free_cards = 0
        self.bankrupt = False
    def receive(self, amount):
        """Add money to the player's balance."""
        if amount > 0:
            self.money += amount
    def pay(self, amount):
        """Pay up to `amount`; returns the actual amount paid (may be less if short)."""
        paid = min(self.money, amount)
        self.money -= paid
        return paid
    def can_afford(self, amount):
        """True when the player's balance covers `amount`."""
        return self.money >= amount
    def add_property(self, prop):
        """Record ownership of a property."""
        if prop not in self.properties:
            self.properties.append(prop)
    def remove_property(self, prop):
        """Release ownership of a property (e.g. on bankruptcy)."""
        if prop in self.properties:
            self.properties.remove(prop)
    def net_worth(self):
        """Cash plus the purchase price of all owned properties."""
        return self.money + sum(p.price for p in self.properties)
    def is_bankrupt(self):
        """True when the player has been declared bankrupt."""
        return self.bankrupt
    def __str__(self):
        return f"{self.name} (${self.money})"