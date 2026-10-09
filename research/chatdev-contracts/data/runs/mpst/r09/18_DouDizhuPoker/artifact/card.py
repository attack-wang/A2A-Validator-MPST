'''
card.py
Defines the Card class representing a single playing card in Dou Dizhu.
Rank ordering: 3 < 4 < ... < 10 < J < Q < K < A < 2 < small joker < big joker.
'''
RANK_NAMES = {
    3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2', 16: 'joker', 17: 'JOKER'
}
SUITS = ['♠', '♥', '♣', '♦']
class Card:
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
    @property
    def name(self):
        return RANK_NAMES[self.rank]
    def __repr__(self):
        if self.rank >= 16:
            return self.name
        return f"{self.name}{self.suit}"
    def __eq__(self, other):
        return self.rank == other.rank
    def __lt__(self, other):
        return self.rank < other.rank
    def __hash__(self):
        return hash(self.rank)