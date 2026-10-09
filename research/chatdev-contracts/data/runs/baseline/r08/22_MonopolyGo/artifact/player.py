'''
player.py
Defines the Player class for the simplified Monopoly Go! game.
A Player tracks their name, board token, money, position, owned
properties, and jail status. Player.pay() is a PURE deduction: it
never triggers bankruptcy by itself. Instead it returns the amount
actually paid, and the caller (Game.charge) is responsible for
detecting shortfalls and declaring bankruptcy. This keeps a single,
unambiguous source of truth for bankruptcy (actual < amount).
'''
class Player:
    """A participant in the game, tracking money, position and assets."""
    STARTING_MONEY = 1500
    def __init__(self, name, token):
        self.name = name
        self.token = token          # single character shown on the board
        self.money = Player.STARTING_MONEY
        self.position = 0           # board index (0 == GO)
        self.properties = []        # list of PropertySpace owned
        self.in_jail = False
        self.jail_turns = 0         # consecutive failed escape attempts
        self.get_out_of_jail_cards = 0
        self.bankrupt = False
    def receive(self, amount):
        """Add money to the player's balance."""
        self.money += amount
    def pay(self, amount):
        """Deduct up to `amount` from the balance.
        Returns the amount actually paid. If the return value is less
        than `amount`, the CALLER (Game.charge) must declare bankruptcy.
        This method never drives the balance negative.
        """
        actual = min(self.money, amount)
        self.money -= actual
        return actual
    def net_worth(self):
        """Cash plus the purchase price of every owned property."""
        return self.money + sum(p.price for p in self.properties)
    def add_property(self, space):
        """Take ownership of a property space."""
        self.properties.append(space)
        space.owner = self
    def owned_groups(self, board):
        """Return the names of colour groups this player monopolises.
        A group is 'monopolised' when the player owns every property
        in it; rent on those properties is doubled by the Game.
        """
        counts = {}
        for space in self.properties:
            counts[space.group] = counts.get(space.group, 0) + 1
        return [g for g, n in counts.items()
                if n == board.group_size(g)]
    def __str__(self):
        return f"{self.name} ({self.token})"