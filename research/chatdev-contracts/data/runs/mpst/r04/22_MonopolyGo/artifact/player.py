'''player.py — Player model: money, position, properties, jail state.'''
class Player:
    """Represents a player: money, position, properties, jail state."""
    JAIL_FINE = 50
    def __init__(self, name, token, starting_money=1500):
        self.name = name
        self.token = token
        self.money = starting_money
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_cards = 0
        self.bankrupt = False
    @property
    def net_worth(self):
        return self.money + sum(p.price for p in self.properties)
    def receive(self, amount):
        self.money += amount
    def pay(self, amount):
        """Deduct money (may go negative).
        Returns True if fully covered (money >= 0), False if bankrupt.
        The Game layer is responsible for resolving bankruptcy.
        """
        self.money -= amount
        return self.money >= 0
    def can_afford(self, amount):
        return self.money >= amount