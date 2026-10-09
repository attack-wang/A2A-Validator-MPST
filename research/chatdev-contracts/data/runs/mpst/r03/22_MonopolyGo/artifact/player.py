'''
Player module: defines the Player class holding money, position, properties and jail state.
'''
STARTING_MONEY = 1500
JAIL_FINE = 50
GO_SALARY = 200
class Player:
    """Represents one player: cash, board position, owned properties and jail status."""
    def __init__(self, name, money=STARTING_MONEY):
        """Initialise a player with a name, starting money and default state."""
        self.name = name
        self.money = money
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.get_out_of_jail_cards = 0
        self.bankrupt = False
    @property
    def net_worth(self):
        """Return cash plus the purchase price of all owned properties."""
        return self.money + sum(p.price for p in self.properties)
    def receive(self, amount):
        """Add `amount` to the player's cash and confirm the transaction."""
        if amount <= 0:
            return
        self.money += amount
        print(f"  {self.name} receives ${amount} (cash: ${self.money}).")
    def pay(self, amount):
        """Deduct `amount` from cash. Returns True if the payment succeeded."""
        if amount < 0:
            return False
        if self.money < amount:
            return False
        self.money -= amount
        print(f"  {self.name} pays ${amount} (cash: ${self.money}).")
        return True