RANK_VALUES = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
               '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
               '2': 15, 'SJ': 16, 'BJ': 17}
class Card:
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUES[rank]
    def is_joker(self):
        return self.rank in ('SJ', 'BJ')
    def display(self):
        ...
    def __eq__, __hash__, __repr__