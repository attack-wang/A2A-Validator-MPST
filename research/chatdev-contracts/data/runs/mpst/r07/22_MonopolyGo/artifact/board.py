'''
board.py
Defines the board spaces (Go, Property, Railroad, Utility, Chance,
Tax, Jail, GoToJail, FreeParking) and the Board class that builds
the simplified 24-space Monopoly Go! board and renders it as text.
'''
class BoardSpace:
    def __init__(self, position, name, space_type):
        self.position = position
        self.name = name
        self.space_type = space_type  # 'go', 'property', 'railroad', 'utility', 'chance', 'tax', 'jail', 'go_to_jail', 'free_parking'
        self.owner = None
    def land_on(self, game, player):
        """Default behavior: nothing happens. Returns a message."""
        return None
    def short_name(self):
        return self.name
class Property(BoardSpace):
    def __init__(self, position, name, price, rent, group):
        super().__init__(position, name, 'property')
        self.price = price
        self.rent = rent
        self.group = group
    def land_on(self, game, player):
        if self.owner is None or self.owner is player or self.owner.bankrupt:
            return None
        game.pay_rent(player, self)
        return None
class Railroad(BoardSpace):
    def __init__(self, position, name, price, rent):
        super().__init__(position, name, 'railroad')
        self.price = price
        self.rent = rent
    def land_on(self, game, player):
        if self.owner is None or self.owner is player or self.owner.bankrupt:
            return None
        game.pay_rent(player, self)
        return None
class Utility(BoardSpace):
    def __init__(self, position, name, price):
        super().__init__(position, name, 'utility')
        self.price = price
        self.rent = 0  # computed at rent time (dice-based)
    def land_on(self, game, player):
        if self.owner is None or self.owner is player or self.owner.bankrupt:
            return None
        game.pay_rent(player, self)
        return None
class TaxSpace(BoardSpace):
    def __init__(self, position, name, amount):
        super().__init__(position, name, 'tax')
        self.amount = amount
    def land_on(self, game, player):
        game.collect_tax(player, self.amount, self.name)
        return None
class GoSpace(BoardSpace):
    def __init__(self, position):
        super().__init__(position, 'GO', 'go')
class JailSpace(BoardSpace):
    def __init__(self, position):
        super().__init__(position, 'Jail', 'jail')
class GoToJailSpace(BoardSpace):
    def __init__(self, position):
        super().__init__(position, 'Go To Jail', 'go_to_jail')
    def land_on(self, game, player):
        game.send_to_jail(player)
class FreeParkingSpace(BoardSpace):
    def __init__(self, position):
        super().__init__(position, 'Free Parking', 'free_parking')
    def land_on(self, game, player):
        game.collect_free_parking(player)
class ChanceSpace(BoardSpace):
    def __init__(self, position):
        super().__init__(position, 'Chance', 'chance')
    def land_on(self, game, player):
        game.draw_chance(player)
class Board:
    """Builds and renders the simplified 24-space board."""
    SIZE = 24
    def __init__(self):
        self.spaces = self._build()
        self.color_groups = {}
        for space in self.spaces:
            if getattr(space, 'group', None):
                self.color_groups.setdefault(space.group, []).append(space)
    def _build(self):
        spaces = [GoSpace(0)]
        ...
        return spaces
    def get_space(self, position):
        return self.spaces[position % self.SIZE]
    def render(self, players):
        ...