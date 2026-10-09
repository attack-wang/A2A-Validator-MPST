class Player:
    def __init__(self, name, money=STARTING_MONEY):
        self.name = name
        self.money = money
        self.position = 0
        self.properties = []  # list of space indices
        self.in_jail = False
        self.jail_turns = 0  # consecutive failed attempts
        self.jail_free_cards = 0
        self.bankrupt = False
    @property
    def token(self): return self.name[0].upper()
    def receive(self, amount): self.money += amount
    def pay(self, amount): 
        """Pay amount; returns actual amount paid (may be less if bankrupt)."""
        self.money -= amount
        if self.money < 0:
            actual = amount + self.money  # what they could actually pay
            self.money = 0
            self.bankrupt = True
            return actual
        return amount
    def net_worth(self): return self.money + sum(price of owned properties)
    def owns_group(self, group, board): check all properties in group owned