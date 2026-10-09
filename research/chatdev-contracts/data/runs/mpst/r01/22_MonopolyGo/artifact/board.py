'''
board.py
Builds the simplified 20-square Monopoly Go! board and provides
movement helpers that handle the GO salary, jail and lookups.
'''
from spaces import Space, PropertySpace
class Board:
    """The game board: a loop of spaces with helper movement methods."""
    SIZE = 20
    GO_BONUS = 200
    GO_POS = 0
    JAIL_POS = 5
    FREE_PARKING_POS = 9
    GO_TO_JAIL_POS = 13
    def __init__(self):
        self.spaces = self._build()
    def _build(self):
        layout = [
            ("GO", "go", None, None),
            ("Mediterranean Avenue", "property", 60, 10),
            ("Chance", "chance", None, None),
            ("Baltic Avenue", "property", 60, 12),
            ("Oriental Avenue", "property", 100, 20),
            ("Jail (Just Visiting)", "jail", None, None),
            ("Vermont Avenue", "property", 100, 20),
            ("Chance", "chance", None, None),
            ("Connecticut Avenue", "property", 120, 24),
            ("Free Parking", "free_parking", None, None),
            ("St. Charles Place", "property", 140, 28),
            ("Chance", "chance", None, None),
            ("States Avenue", "property", 140, 28),
            ("Go To Jail", "go_to_jail", None, None),
            ("Virginia Avenue", "property", 160, 32),
            ("Chance", "chance", None, None),
            ("St. James Place", "property", 180, 36),
            ("Tennessee Avenue", "property", 180, 36),
            ("Chance", "chance", None, None),
            ("New York Avenue", "property", 200, 40),
        ]
        spaces = []
        for name, kind, price, rent in layout:
            if kind == "property":
                spaces.append(PropertySpace(name, price, rent))
            else:
                spaces.append(Space(name, kind))
        return spaces
    # ----- lookups -------------------------------------------------
    def get_space(self, position):
        return self.spaces[position % self.SIZE]
    def property_spaces(self):
        return [s for s in self.spaces if s.type == "property"]
    # ----- movement -------------------------------------------------
    def move_forward(self, player, steps):
        """Move a player forward, collecting the GO salary on a wrap."""
        start = player.position
        player.position = (player.position + steps) % self.SIZE
        if start + steps >= self.SIZE:
            player.receive(self.GO_BONUS)
            return True  # collected GO salary
        return False
    def move_backward(self, player, steps):
        """Move a player backwards; no GO salary is awarded."""
        player.position = (player.position - steps) % self.SIZE
    def advance_to(self, player, target):
        """Teleport a player forward to a space, paying GO salary if wrapped."""
        target %= self.SIZE
        if target != player.position and target < player.position:
            player.receive(self.GO_BONUS)
            return True
        player.position = target
        return False