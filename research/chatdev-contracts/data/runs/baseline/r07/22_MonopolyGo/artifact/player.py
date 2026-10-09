'''
player.py
Player model for the simplified Monopoly Go! game.
Tracks each player's money, board position, property ownership,
jail status, Get Out of Jail Free cards and bankruptcy state, and
provides helpers for paying/receiving money and net worth.
'''
class Player:
    """One player: money, position, jail state and owned properties."""
    STARTING_MONEY = 1500
    JAIL_FINE = 50
    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.money = Player.STARTING_MONEY
        self.position = 0
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_cards = 0
        self.bankrupt = False
        self.properties = []  # PropertySpace objects owned
    @property
    def net_worth(self):
        """Cash plus the purchase price of all owned properties."""
        return self.money + sum(p.price for p in self.properties)
    def receive(self, amount):
        """Add money to the player's balance."""
        self.money += amount
    def pay(self, amount):
        """Deduct money; returns True when the full amount was available."""
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    def pay_as_much_as_possible(self, amount):
        """Pay what the player can (used right before bankruptcy)."""
        paid = self.money
        self.money = 0
        return paid
    def send_to_jail(self, jail_position):
        """Move the player to jail and reset jail turn counters."""
        self.position = jail_position
        self.in_jail = True
        self.jail_turns = 0
    def leave_jail(self, paid=False, used_card=False):
        """Release the player from jail, applying fine/card if used."""
        if paid:
            self.money -= Player.JAIL_FINE
        if used_card:
            self.get_out_of_jail_cards -= 1
        self.in_jail = False
        self.jail_turns = 0
    def bankrupt_now(self):
        """Mark the player bankrupt and return owned properties to the bank."""
        self.bankrupt = True
        self.money = 0
        for prop in self.properties:
            prop.owner = None
        self.properties = []