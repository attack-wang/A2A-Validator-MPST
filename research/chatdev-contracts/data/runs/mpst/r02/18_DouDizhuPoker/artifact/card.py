class Card:
    __slots__ = ('rank', 'suit')
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
    @property
    def value(self):
        return RANK_VALUE[self.rank]
    def __repr__(self):
        return self.rank if self.suit is None else f"{self.suit}{self.rank}"
    def __eq__(self, other): return self.rank == other.rank and self.suit == other.suit
    def __hash__(self): return hash((self.rank, self.suit))