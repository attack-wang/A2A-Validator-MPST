'''
player.py
Defines the Player class that tracks cash, owned properties,
board position, jail state and Get Out of Jail Free cards.
'''
class Player:
    """A single participant in the game."""
    STARTING_MONEY = 1500
    JAIL_BAIL = 50
    def __init__(self, name):
        self.name = name
        self.money = Player.STARTING_MONEY
        self.position = 0
        self.in_jail = False
        self.jail_turns = 0
        self.jail_free_cards = 0
        self.properties = []
        self.bankrupt = False
    # ----- money -------------------------------------------------
    def receive(self, amount):
        self.money += amount
    def can_afford(self, amount):
        return self.money >= amount
    def pay(self, amount):
        """Pay as much as possible; returns the amount actually paid."""
        paid = min(self.money, amount)
        self.money -= paid
        return paid
    # ----- properties --------------------------------------------
    def add_property(self, prop):
        self.properties.append(prop)
    def release_properties(self):
        """Return all properties to the bank (used on bankruptcy)."""
        released = list(self.properties)
        for prop in released:
            prop.owner = None
        self.properties = []
        return released
    def net_worth(self):
        return self.money + sum(p.price for p in self.properties)
    # ----- jail ---------------------------------------------------
    def send_to_jail(self, jail_position):
        self.position = jail_position
        self.in_jail = True
        self.jail_turns = 0
    def release_from_jail(self):
        self.in_jail = False
        self.jail_turns = 0
    def has_jail_free_card(self):
        return self.jail_free_cards > 0
    def use_jail_free_card(self):
        if self.jail_free_cards > 0:
            self.jail_free_cards -= 1
            return True
        return False
    # ----- helpers -------------------------------------------------
    @property
    def is_active(self):
        return not self.bankrupt
    def __str__(self):
        status = "BANKRUPT" if self.bankrupt else f"${self.money}"
        return f"{self.name} ({status})"