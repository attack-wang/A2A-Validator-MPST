'''Card module: defines the Card class, rank ordering, and deck creation for Dou Dizhu.'''
import random
RANK_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'SJ', 'BJ']
RANK_VALUE = {rank: i + 3 for i, rank in enumerate(RANK_ORDER)}  # 3..17
VALUE_RANK = {v: k for k, v in RANK_VALUE.items()}
SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
SUIT_SYMBOLS = {'Spades': '♠', 'Hearts': '♥', 'Clubs': '♣', 'Diamonds': '♦'}
class Card:
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUE[rank]
    @property
    def is_joker(self):
        return self.rank in ('SJ', 'BJ')
    def __repr__(self):
        if self.is_joker:
            return 'Small Joker' if self.rank == 'SJ' else 'Big Joker'
        return f'{SUIT_SYMBOLS[self.suit]}{self.rank}'
    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit
    def __hash__(self):
        return hash((self.rank, self.suit))
    def __lt__(self, other):
        return self.value < other.value
def create_deck():
    deck = [Card(rank, suit) for suit in SUITS for rank in RANK_ORDER if rank not in ('SJ', 'BJ')]
    deck.append(Card('SJ'))
    deck.append(Card('BJ'))
    return deck
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck