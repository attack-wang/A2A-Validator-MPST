"""Player model for the simplified Monopoly Go! game."""
from config import STARTING_MONEY, BOARD_LAYOUT, TYPE_PROPERTY
class Player:
    """Represents a single player, tracking money, position and assets."""
    def __init__(self, token):
        self.token = token
        self.money = STARTING_MONEY
        self.position = 0  # GO_POSITION
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.bankrupt = False
    def receive(self, amount):
        self.money += amount
    def pay(self, amount):
        """Attempt to pay. Returns False (and marks bankrupt) if unaffordable."""
        if self.money < amount:
            self.bankrupt = True
            return False
        self.money -= amount
        return True
    def buy(self, index, price):
        if self.money < price:
            return False
        self.money -= price
        self.properties.append(index)
        return True
    def net_worth(self):
        return self.money + sum(
            BOARD_LAYOUT[i][2] for i in self.properties
            if BOARD_LAYOUT[i][0] == TYPE_PROPERTY
        )