'''
player.py
Player model: money, position, properties, jail state.
'''
class Player:
    STARTING_MONEY = 1500
    JAIL_POSITION = 10
    def __init__(self, name, money=None):
        self.name = name
        self.money = Player.STARTING_MONEY if money is None else money
        self.position = 0
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_cards = 0
        self.properties = []
        self.bankrupt = False
    def receive(self, amount):
        self.money += amount
        return amount
    def pay(self, amount):
        """Attempt to pay. Returns amount actually paid (may be less if bankrupt)."""
        if self.money >= amount:
            self.money -= amount
            return amount
        paid = self.money
        self.money = 0
        self.bankrupt = True
        return paid
    def can_afford(self, amount):
        return self.money >= amount
    def add_property(self, prop):
        self.properties.append(prop)
        prop.owner = self
    def remove_all_properties(self):
        for prop in self.properties:
            prop.owner = None
        self.properties = []
    def send_to_jail(self):
        self.position = self.JAIL_POSITION
        self.in_jail = True
        self.jail_turns = 0
    def net_worth(self):
        return self.money + sum(p.price for p in self.properties)
    def __str__(self):
        return f"{self.name} (${self.money})"