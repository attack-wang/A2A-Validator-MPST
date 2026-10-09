'''
player.py
Defines the Player class for the simplified Monopoly Go! game.
Each player tracks their money, board position, owned properties,
and jail status. Provides methods for receiving/paying money,
buying properties, and bankruptcy handling.
'''
class Player:
    """Represents a single player in the game."""
    STARTING_MONEY = 1500
    JAIL_POSITION = 5  # index of the Jail space on the board
    def __init__(self, name):
        self.name = name
        self.money = Player.STARTING_MONEY
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_cards = 0
        self.bankrupt = False
    @property
    def token(self):
        """Single-character token used for board display."""
        return self.name[0].upper()
    def receive(self, amount):
        """Add money to the player's balance."""
        if amount > 0:
            self.money += amount
    def pay(self, amount):
        """
        Attempt to pay `amount`.
        Returns True if fully paid, False if the player goes bankrupt
        (pays whatever they have left and is marked bankrupt).
        """
        if self.money >= amount:
            self.money -= amount
            return True
        self.money = 0
        self.bankrupt = True
        return False
    def can_afford(self, amount):
        return self.money >= amount
    def buy_property(self, prop):
        """Buy an unowned property if affordable. Returns True on success."""
        if prop is None or prop.owner is not None:
            return False
        if self.money < prop.price:
            return False
        self.pay(prop.price)
        prop.owner = self
        self.properties.append(prop)
        return True
    def add_property(self, prop):
        """Transfer a property to this player without payment (bankruptcy)."""
        if prop is None:
            return
        if prop.owner is not None and prop in prop.owner.properties:
            prop.owner.properties.remove(prop)
        prop.owner = self
        if prop not in self.properties:
            self.properties.append(prop)
    def net_worth(self):
        """Cash + total property value."""
        return self.money + sum(p.price for p in self.properties)
    def owns_color_group(self, board, group):
        """True if the player owns every property in the given color group."""
        group_props = board.color_groups.get(group, [])
        return bool(group_props) and all(p.owner is self for p in group_props)
    def send_to_jail(self):
        self.in_jail = True
        self.jail_turns = 0
        self.position = Player.JAIL_POSITION
    def release_from_jail(self):
        self.in_jail = False
        self.jail_turns = 0
    def reset(self):
        """Reset player state (used when restarting)."""
        self.money = Player.STARTING_MONEY
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_cards = 0
        self.bankrupt = False
    def __str__(self):
        status = " (BANKRUPT)" if self.bankrupt else (" (IN JAIL)" if self.in_jail else "")
        return f"{self.name}{status}: ${self.money}, {len(self.properties)} property(ies)"