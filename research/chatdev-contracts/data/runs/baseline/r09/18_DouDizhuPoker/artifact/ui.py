class Card:
    RANK_VALUES = {'3':3,...,'2':15}
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
        self.value = ...
    @property
    def is_joker(self)
    def __repr__: f"{suit}{rank}" or "小王"/"大王"