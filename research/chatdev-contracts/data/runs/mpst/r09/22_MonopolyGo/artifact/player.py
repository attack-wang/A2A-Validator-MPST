'''
player.py
Defines the Player class...
'''
class Player:
    def __init__(self, name, token, money=1500):
        self.name = name
        self.token = token  # e.g. "P1"
        self.money = money
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.jail_free_cards = 0
        self.bankrupt = False
    def receive(self, amount):
        self.money += amount
    def can_pay(self, amount):
        return self.money >= amount
    def pay(self, amount):
        """Deduct amount; returns True if the player had enough."""
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    def add_property(self, prop):
        self.properties.append(prop)
        prop.owner = self
    def remove_properties(self):
        props = list(self.properties)
        self.properties = []
        return props
    def net_worth(self):
        return self.money + sum(p.price for p in self.properties)
    def property_names(self):
        return ", ".join(p.short for p in self.properties) if self.properties else "none"
    def __str__(self):
        status = "BANKRUPT" if self.bankrupt else ("IN JAIL" if self.in_jail else "active")
        return f"[{self.token}] {self.name}: ${self.money} | pos {self.position} | props: {self.property_names()} | {status}"