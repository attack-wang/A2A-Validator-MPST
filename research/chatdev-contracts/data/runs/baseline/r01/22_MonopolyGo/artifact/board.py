'''
board.py — Board, Space, and Property classes...
'''
class Space:
    """A single space on the board."""
    KIND_GO = "go"
    KIND_PROPERTY = "property"
    KIND_CHANCE = "chance"
    KIND_JAIL = "jail"
    KIND_FREE_PARKING = "free_parking"
    KIND_GO_TO_JAIL = "go_to_jail"
    def __init__(self, name, kind, prop=None):
        self.name = name
        self.kind = kind
        self.prop = prop
    def __str__(self): ...
class Property:
    """A purchasable property..."""
    def __init__(self, name, price, base_rent, group):
        ...
        self.owner = None
    def rent_due(self, all_properties):
        rent = self.base_rent
        if self.owner is not None and self._owner_has_monopoly(all_properties):
            rent *= 2
        return rent
    def _owner_has_monopoly(self, all_properties):
        return all(p.owner is self.owner for p in all_properties if p.group == self.group)
    def __str__ ...
class Board:
    """The game board: builds the 24-space layout..."""
    GO_SALARY = 200
    JAIL_POSITION = 6
    FREE_PARKING_POSITION = 12
    def __init__(self):
        self.spaces = self._build()
    def _build(self):
        layout = [
            ("GO", Space.KIND_GO, None),
            ("Mediterranean Avenue", Space.KIND_PROPERTY, (60, 4, "Brown")),
            ...
        ]
        build Space/Property objects
    @property
    def size(self): return len(self.spaces)
    def get_space(self, position): return self.spaces[position % self.size]
    def all_properties(self): return [s.prop for s in self.spaces if s.kind == Space.KIND_PROPERTY]