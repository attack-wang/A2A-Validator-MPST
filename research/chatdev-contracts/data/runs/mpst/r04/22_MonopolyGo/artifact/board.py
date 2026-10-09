'''board.py — Board spaces (GO, properties, chance, jail, free parking) and Board builder.'''
class Space:
    """A space on the board."""
    def __init__(self, name, kind):
        self.name = name
        self.kind = kind  # 'go', 'property', 'chance', 'jail', 'free_parking', 'go_to_jail'
    def short_name(self):
        return self.name[:10]
    def describe(self):
        return self.name
    def info_line(self):
        return self.kind
class Property(Space):
    def __init__(self, name, price, rent, group):
        super().__init__(name, 'property')
        self.price = price
        self.rent = rent
        self.group = group
        self.owner = None
    @property
    def is_owned(self):
        return self.owner is not None
    def info_line(self):
        if self.owner is None:
            return "${} rent ${}".format(self.price, self.rent)
        return "owner: {}".format(self.owner.token)
class GoSpace(Space):
    def __init__(self):
        super().__init__("GO", 'go')
    def info_line(self):
        return "collect $200"
class ChanceSpace(Space):
    def __init__(self):
        super().__init__("Chance", 'chance')
    def info_line(self):
        return "draw a card"
class JailSpace(Space):
    def __init__(self):
        super().__init__("Jail", 'jail')
    def info_line(self):
        return "just visiting"
class FreeParkingSpace(Space):
    def __init__(self):
        super().__init__("Free Parking", 'free_parking')
    def info_line(self):
        return "collect the pot"
class GoToJailSpace(Space):
    def __init__(self):
        super().__init__("Go To Jail", 'go_to_jail')
    def info_line(self):
        return "go to jail!"
class Board:
    """24-space perimeter board with 8 colour groups."""
    GO_SALARY = 200
    JAIL_POSITION = 6
    def __init__(self):
        self.spaces = self._build()
    def _build(self):
        spaces = [
            GoSpace(),
            Property("Old Kent Road", 60, 10, "brown"),
            Property("Whitechapel Rd", 60, 10, "brown"),
            ChanceSpace(),
            Property("Angel Islington", 100, 14, "light blue"),
            Property("Euston Road", 100, 14, "light blue"),
            JailSpace(),
            Property("Pall Mall", 140, 18, "pink"),
            Property("Whitehall", 140, 18, "pink"),
            ChanceSpace(),
            Property("Bow Street", 180, 22, "orange"),
            Property("Marlborough St", 180, 22, "orange"),
            FreeParkingSpace(),
            Property("Strand", 220, 26, "red"),
            Property("Fleet Street", 220, 26, "red"),
            ChanceSpace(),
            Property("Trafalgar Sq", 260, 30, "yellow"),
            Property("Leicester Sq", 260, 30, "yellow"),
            GoToJailSpace(),
            Property("Piccadilly", 300, 34, "green"),
            Property("Regent Street", 300, 34, "green"),
            Property("Bond Street", 350, 40, "dark blue"),
            Property("Oxford Street", 350, 40, "dark blue"),
            Property("Boardwalk", 400, 50, "dark blue"),
        ]
        return spaces
    def __len__(self):
        return len(self.spaces)
    def get_space(self, pos):
        return self.spaces[pos % len(self.spaces)]
    def properties_in_group(self, group):
        return [s for s in self.spaces if isinstance(s, Property) and s.group == group]
    def owns_monopoly(self, player, group):
        props = self.properties_in_group(group)
        return bool(props) and all(p.owner is player for p in props)