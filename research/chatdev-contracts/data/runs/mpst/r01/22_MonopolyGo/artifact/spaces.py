'''
spaces.py
Board space definitions: a generic Space plus a PropertySpace
subclass that carries price, rent and ownership information.
'''
class Space:
    """A single square on the board."""
    def __init__(self, name, space_type):
        self.name = name
        self.type = space_type  # go, property, chance, jail, free_parking, go_to_jail
    def __str__(self):
        return self.name
class PropertySpace(Space):
    """A purchasable property that pays rent to its owner."""
    def __init__(self, name, price, rent):
        super().__init__(name, "property")
        self.price = price
        self.rent = rent
        self.owner = None
    def is_owned(self):
        return self.owner is not None
    def is_owned_by(self, player):
        return self.owner is player
    def purchase(self, player):
        """Sell the property to the given player (assumes funds available)."""
        self.owner = player
        player.add_property(self)
    def __str__(self):
        owner = self.owner.name if self.owner else "unowned"
        return f"{self.name} (price ${self.price}, rent ${self.rent}, owner: {owner})"