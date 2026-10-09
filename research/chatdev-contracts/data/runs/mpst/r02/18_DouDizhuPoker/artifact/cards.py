'''
cards.py
Defines the Card class, rank ordering/values, and deck building
utilities for the Dou Dizhu (Fight the Landlord) game.
'''
import random
RANK_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'SJ', 'BJ']
RANK_VALUE = {r: i + 3 for i, r in enumerate(RANK_ORDER)}  # 3 -> 3 ... BJ -> 17
SUITS = ['♠', '♥', '♣', '♦']
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
    def __str__(self):
        return self.__repr__()
    def __eq__(self, other):
        return isinstance(other, Card) and self.rank == other.rank and self.suit == other.suit
    def __hash__(self):
        return hash((self.rank, self.suit))
def build_deck():
    '''Build and shuffle a full 54-card Dou Dizhu deck.'''
    deck = [Card(r, s) for r in RANK_ORDER[:13] for s in SUITS]
    deck.append(Card('SJ', 'Joker'))
    deck.append(Card('BJ', 'Joker'))
    random.shuffle(deck)
    return deck