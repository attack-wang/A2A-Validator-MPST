'''
card.py
Defines the Card class and the Deck used in Dou Dizhu.
'''
import random
# Rank constants
RANK_3 = 3
RANK_4 = 4
RANK_5 = 5
RANK_6 = 6
RANK_7 = 7
RANK_8 = 8
RANK_9 = 9
RANK_10 = 10
RANK_J = 11
RANK_Q = 12
RANK_K = 13
RANK_A = 14
RANK_2 = 15
RANK_SMALL_JOKER = 16
RANK_BIG_JOKER = 17
RANK_TO_DISPLAY = {
    3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2',
    16: 'joker', 17: 'JOKER'
}
DISPLAY_TO_RANK = {v: k for k, v in RANK_TO_DISPLAY.items()}
SUITS = ['♠', '♥', '♣', '♦']
class Card:
    __slots__ = ('rank', 'suit')
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit  # None for jokers
    @property
    def is_joker(self):
        return self.rank >= RANK_SMALL_JOKER
    def __repr__(self):
        disp = RANK_TO_DISPLAY[self.rank]
        if self.is_joker:
            return disp
        return f"{disp}{self.suit}"
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit
    def __hash__(self):
        return hash((self.rank, self.suit))
    def __lt__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank
        # Jokers have suit None; never equal rank with suited cards, safe
        if self.suit is None or other.suit is None:
            return False
        return SUITS.index(self.suit) < SUITS.index(other.suit)