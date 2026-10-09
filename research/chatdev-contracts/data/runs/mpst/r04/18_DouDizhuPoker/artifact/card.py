'''
card.py
Defines the Card and Deck classes for Dou Dizhu.
Rank encoding: 3..10 -> 3..10, J=11, Q=12, K=13, A=14, 2=15,
Small Joker=16, Big Joker=17.
'''
import random
RANK_NAMES = {
    3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10',
    11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2',
    16: 'joker', 17: 'JOKER'
}
SUITS = ['♠', '♥', '♣', '♦']
class Card:
    __slots__ = ('rank', 'suit')
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
    @property
    def is_joker(self):
        return self.rank >= 16
    @property
    def color(self):
        if self.is_joker:
            return 'red' if self.rank == 17 else 'black'
        return 'red' if self.suit in (1, 3) else 'black'
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        if self.is_joker:
            return RANK_NAMES[self.rank]
        return RANK_NAMES[self.rank] + SUITS[self.suit]
    def __eq__(self, other):
        return isinstance(other, Card) and self.rank == other.rank and self.suit == other.suit
    def __hash__(self):
        return hash((self.rank, self.suit))
    def __lt__(self, other):
        if self.rank != other.rank:
            return self.rank < other.rank
        return (self.suit is not None and other.suit is not None and self.suit < other.suit)
class Deck:
    def __init__(self):
        self.cards = []
        for rank in range(3, 16):
            for suit in range(4):
                self.cards.append(Card(rank, suit))
        self.cards.append(Card(16, None))  # small joker
        self.cards.append(Card(17, None))  # big joker
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self):
        """Shuffle and deal 17/17/17 cards plus a 3-card bottom."""
        self.shuffle()
        hands = (self.cards[0:17], self.cards[17:34], self.cards[34:51])
        bottom = self.cards[51:54]
        for h in hands:
            h.sort()
        return hands[0], hands[1], hands[2], bottom