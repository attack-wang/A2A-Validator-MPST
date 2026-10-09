'''
card.py
Defines the Card class representing a single playing card in Dou Dizhu.
Ranks: 3-14 are 3..A, 15 is 2, 16 is small joker, 17 is big joker.
'''
RANK_TO_NAME = {
    3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2', 16: 'joker', 17: 'JOKER'
}
class Card:
    """A single playing card. Jokers have suit None."""
    __slots__ = ('rank', 'suit')
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
    def __repr__(self):
        return RANK_TO_NAME[self.rank] if self.suit is None else RANK_TO_NAME[self.rank] + self.suit
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit
    def __hash__(self):
        return hash((self.rank, self.suit))