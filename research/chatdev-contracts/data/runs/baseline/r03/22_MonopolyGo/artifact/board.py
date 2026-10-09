'''
board.py
Module defining the game board for the simplified Monopoly Go! game.
Contains the Space base class, specialised space types (Property, Chance,
Jail, Go To Jail, Free Parking, GO) and the Board class that assembles them.
'''
class Space:
    '''Base class for a single space on the board.'''
    def __init__(self, name, space_type):
        self.name = name
        self.space_type = space_type
    def __str__(self):
        return self.name
class Property(Space):
    '''A purchasable property that charges rent to visiting players.'''
    def __init__(self, name, price, rent):
        super().__init__(name, "property")
        self.price = price
        self.rent = rent
        self.owner = None
    def is_owned(self):
        return self.owner is not None
    def is_owned_by(self, player):
        return self.owner is player
    def __str__(self):
        return self.name
class GoSpace(Space):
    '''The GO space; players collect money for passing/landing here.'''
    def __init__(self):
        super().__init__("GO", "go")
class ChanceSpace(Space):
    '''A space that forces the player to draw a chance card.'''
    def __init__(self):
        super().__init__("Chance", "chance")
class JailSpace(Space):
    '''The jail space; players here are either visiting or incarcerated.'''
    def __init__(self):
        super().__init__("Jail", "jail")
class GoToJailSpace(Space):
    '''Landing here sends the player directly to jail.'''
    def __init__(self):
        super().__init__("Go To Jail", "go_to_jail")
class FreeParkingSpace(Space):
    '''A safe space; with our simplified rules it pays out the fine pot.'''
    def __init__(self):
        super().__init__("Free Parking", "free_parking")
class Board:
    '''The game board: an ordered loop of spaces.'''
    GO_SALARY = 200
    JAIL_POSITION = 10
    def __init__(self):
        self.spaces = self._build()
    def _build(self):
        '''Create the standard 24-space board.'''
        return [
            GoSpace(),                                          # 0
            Property("Mediterranean Avenue", 60, 10),           # 1
            ChanceSpace(),                                      # 2
            Property("Baltic Avenue", 60, 12),                  # 3
            FreeParkingSpace(),                                 # 4
            Property("Reading Railroad", 200, 50),              # 5
            Property("Oriental Avenue", 100, 20),               # 6
            ChanceSpace(),                                      # 7
            Property("Vermont Avenue", 100, 20),                # 8
            Property("Connecticut Avenue", 120, 24),            # 9
            JailSpace(),                                        # 10
            Property("St. Charles Place", 140, 28),             # 11
            Property("States Avenue", 140, 28),                 # 12
            ChanceSpace(),                                      # 13
            Property("Virginia Avenue", 160, 32),               # 14
            GoToJailSpace(),                                    # 15
            Property("St. James Place", 180, 36),               # 16
            Property("Tennessee Avenue", 200, 40),              # 17
            ChanceSpace(),                                      # 18
            FreeParkingSpace(),                                 # 19
            Property("New York Avenue", 200, 40),               # 20
            ChanceSpace(),                                      # 21
            Property("Park Place", 300, 60),                    # 22
            Property("Boardwalk", 400, 80),                     # 23
        ]
    def size(self):
        return len(self.spaces)
    def get_space(self, position):
        '''Return the space at the given position (wraps around).'''
        return self.spaces[position % len(self.spaces)]
    def properties(self):
        '''Return all property spaces on the board.'''
        return [s for s in self.spaces if isinstance(s, Property)]