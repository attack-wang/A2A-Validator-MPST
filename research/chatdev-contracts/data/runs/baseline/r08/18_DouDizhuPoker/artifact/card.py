'''
card.py
The Card class: a single playing card identified by rank (+ optional suit).
Gameplay comparisons ignore suit; only rank matters in Dou Dizhu.
'''
from cards import RANK_VALUE
class Card:
    __slots__ = ('rank', 'suit')
    def __init__(self, rank, suit=None):
        if rank not in RANK_VALUE:
            raise ValueError(f'Unknown rank: {rank!r}')
        self.rank = rank
        self.suit = suit
    @property
    def value(self):
        return RANK_VALUE[self.rank]
    def is_joker(self):
        return self.rank in ('SJ', 'BJ')
    def __eq__(self, other):
        # Suit is ignored: two cards are equal for gameplay if ranks match.
        return isinstance(other, Card) and self.rank == other.rank
    def __lt__(self, other):
        return self.value < other.value
    def __hash__(self):
        return hash(self.rank)
    def __repr__(self):
        return f'Card({self.rank!r})'
    def __str__(self):
        if self.is_joker() or self.suit is None:
            return self.rank  # 'SJ' / 'BJ'
        return f'{self.suit}{self.rank}'