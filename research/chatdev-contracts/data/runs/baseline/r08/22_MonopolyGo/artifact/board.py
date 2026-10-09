'''
board.py
Defines the board spaces and the Board for the simplified Monopoly
Go! game. The board has 24 spaces: GO, properties in colour groups,
Chance squares, two tax squares, Jail, Free Parking and Go To Jail.
Every space implements on_land(game, player), called when a player
ends their move on it. Passing GO pays a salary handled by the
Game's movement logic — GoSpace.on_land deliberately does NOT pay
again, so landing on GO pays the salary exactly once.
'''
class Space:
    """A single square on the board."""
    def __init__(self, name, short_name, kind):
        self.name = name
        self.short_name = short_name   # compact label for board rendering
        self.kind = kind               # e.g. "go", "property", "chance"
        self.owner = None              # only meaningful for properties
    def on_land(self, game, player):
        """Hook executed when `player` lands on this space."""
        pass
class GoSpace(Space):
    """GO square. Salary is paid by Game.move_player on pass/land,
    so on_land must not pay again (avoids double salary on landing)."""
    def __init__(self):
        super().__init__("GO", "GO", "go")
    def on_land(self, game, player):
        pass  # salary already granted by the movement logic
class PropertySpace(Space):
    """A buyable property with a fixed rent (no houses, simplified)."""
    def __init__(self, name, short_name, price, rent, group):
        super().__init__(name, short_name, "property")
        self.price = price
        self.rent = rent
        self.group = group
    def on_land(self, game, player):
        game.handle_property(self, player)
class ChanceSpace(Space):
    """Draw a chance card."""
    def __init__(self):
        super().__init__("Chance", "?", "chance")
    def on_land(self, game, player):
        game.handle_chance(player)
class TaxSpace(Space):
    """Pay a flat tax; the money goes to the Free Parking pot."""
    def __init__(self, name, short_name, amount):
        super().__init__(name, short_name, "tax")
        self.amount = amount
    def on_land(self, game, player):
        game.charge(player, self.amount, payee=None,
                    reason=f"{self.name} of ${self.amount}")
class JailSpace(Space):
    """Jail square: players in jail sit here; visitors just pass by."""
    def __init__(self):
        super().__init__("Jail / Just Visiting", "JAIL", "jail")
    def on_land(self, game, player):
        # Landing here by normal movement is just a visit — nothing happens.
        pass
class FreeParkingSpace(Space):
    """Free Parking: landing here collects the whole pot of fines/taxes."""
    def __init__(self):
        super().__init__("Free Parking", "PARK", "free_parking")
    def on_land(self, game, player):
        game.collect_free_parking_pot(player)
class GoToJailSpace(Space):
    """Landing here sends the player directly to jail."""
    def __init__(self):
        super().__init__("Go To Jail", "GOTOJ", "go_to_jail")
    def on_land(self, game, player):
        game.send_to_jail(player)
class Board:
    """The 24-space board and its lookup helpers."""
    SIZE = 24
    GO_POSITION = 0
    JAIL_POSITION = 6
    FREE_PARKING_POSITION = 12
    GO_TO_JAIL_POSITION = 18
    def __init__(self):
        self.spaces = self._build()
        # group name -> number of properties in that group
        self._group_sizes = {}
        for space in self.spaces:
            if isinstance(space, PropertySpace):
                self._group_sizes[space.group] = \
                    self._group_sizes.get(space.group, 0) + 1
    def _build(self):
        """Construct the fixed layout of the board."""
        return [
            GoSpace(),                                            # 0
            PropertySpace("Pine Street", "PINE", 60, 10, "Brown"),    # 1
            PropertySpace("Cedar Lane", "CEDAR", 60, 12, "Brown"),    # 2
            ChanceSpace(),                                        # 3
            PropertySpace("Maple Avenue", "MAPLE", 100, 18, "Light Blue"),  # 4
            TaxSpace("Income Tax", "TAX", 100),                   # 5
            JailSpace(),                                          # 6
            PropertySpace("Birch Boulevard", "BIRCH", 100, 18, "Light Blue"),  # 7
            PropertySpace("Willow Way", "WILLOW", 120, 22, "Pink"),   # 8
            ChanceSpace(),                                        # 9
            PropertySpace("Elm Street", "ELM", 140, 26, "Pink"),      # 10
            PropertySpace("Oak Drive", "OAK", 160, 30, "Orange"),     # 11
            FreeParkingSpace(),                                   # 12
            PropertySpace("Walnut Court", "WALNUT", 160, 30, "Orange"),  # 13
            PropertySpace("Cherry Hill", "CHERRY", 180, 34, "Red"),   # 14
            ChanceSpace(),                                        # 15
            PropertySpace("Rose Garden", "ROSE", 200, 38, "Red"),     # 16
            TaxSpace("Luxury Tax", "LTAX", 75),                   # 17
            GoToJailSpace(),                                      # 18
            PropertySpace("Aspen Heights", "ASPEN", 220, 42, "Yellow"),  # 19
            PropertySpace("Sequoia Square", "SEQUOIA", 220, 44, "Yellow"),  # 20
            ChanceSpace(),                                        # 21
            PropertySpace("Redwood Resort", "REDWOOD", 260, 50, "Green"),  # 22
            PropertySpace("Palm Plaza", "PALM", 280, 55, "Green"),    # 23
        ]
    def get(self, position):
        """Return the space at `position` (wraps around)."""
        return self.spaces[position % Board.SIZE]
    @property
    def size(self):
        return Board.SIZE
    def group_size(self, group):
        """Number of properties belonging to `group`."""
        return self._group_sizes.get(group, 0)
    def unowned_properties(self):
        """All properties currently without an owner."""
        return [s for s in self.spaces
                if isinstance(s, PropertySpace) and s.owner is None]