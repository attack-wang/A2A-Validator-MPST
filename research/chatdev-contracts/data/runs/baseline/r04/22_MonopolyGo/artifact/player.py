"""Player model for Monopoly Go!"""
from game_constants import START_MONEY
class Player:
    def __init__(self, name, money=START_MONEY):
        self.name = name
        self.money = money
        self.position = 0
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_cards = 0
        self.properties = []
        self.bankrupt = False
    @property
    def is_bankrupt(self):
        return self.bankrupt
    def receive(self, amount):
        self.money += amount
    def can_afford(self, amount):
        return self.money >= amount
    def pay(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        self.money = 0
        self.bankrupt = True
        return False
    def add_property(self, space):
        self.properties.append(space)
        space.owner = self
    def remove_properties(self):
        for space in self.properties:
            space.owner = None
        self.properties = []
    def net_worth(self):
        return self.money + sum(p.price for p in self.properties)
    def __str__(self):
        return f"{self.name} (${self.money})"