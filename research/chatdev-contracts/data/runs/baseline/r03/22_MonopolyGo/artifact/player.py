'''
player.py
Module defining the Player class for the simplified Monopoly Go! game.
A Player tracks money, board position, owned properties, and jail status.
'''
class Player:
    '''Represents a single player, including money, position and assets.'''
    STARTING_MONEY = 1500
    JAIL_FINE = 50
    MAX_JAIL_TURNS = 3
    def __init__(self, name, starting_money=1500):
        '''Initialize the player with a name, starting money and default state.'''
        self.name = name
        self.money = starting_money
        self.position = 0
        self.properties = []
        self.in_jail = False
        self.jail_turns = 0
        self.bankrupt = False
    def receive(self, amount):
        '''Add money to the player's balance.'''
        self.money += amount
    def pay(self, amount):
        '''
        Attempt to pay an amount. If funds are insufficient the player pays
        everything they have and is declared bankrupt.
        Returns:
            int: the amount actually paid.
        '''
        if self.money >= amount:
            self.money -= amount
            return amount
        paid = self.money
        self.money = 0
        self.bankrupt = True
        return paid
    def can_afford(self, amount):
        '''Return True if the player has at least the given amount.'''
        return self.money >= amount
    def add_property(self, prop):
        '''Add a property to the player's holdings.'''
        self.properties.append(prop)
    def remove_properties(self):
        '''
        Return all owned properties to the bank (used on bankruptcy).
        Returns:
            list: the properties that were released.
        '''
        released = list(self.properties)
        for prop in released:
            prop.owner = None
        self.properties = []
        return released
    def net_worth(self):
        '''Total worth: cash plus the purchase price of owned properties.'''
        return self.money + sum(p.price for p in self.properties)
    def property_names(self):
        '''Return a comma separated string of owned property names.'''
        if not self.properties:
            return "None"
        return ", ".join(p.name for p in self.properties)
    def send_to_jail(self, jail_position):
        '''Move the player to jail and mark them as incarcerated.'''
        self.position = jail_position
        self.in_jail = True
        self.jail_turns = 0
    def release_from_jail(self):
        '''Release the player from jail.'''
        self.in_jail = False
        self.jail_turns = 0
    def is_bankrupt(self):
        '''Return True when the player has run out of money.'''
        return self.bankrupt