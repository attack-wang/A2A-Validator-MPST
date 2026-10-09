'''Card module for Dou Dizhu: defines the Card class and deck utilities.'''
import random
RANK_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
RANK_VALUE = {r: i + 3 for i, r in enumerate(RANK_ORDER)}
SMALL_JOKER_VALUE = 16
BIG_JOKER_VALUE = 17
SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
SUIT_SYMBOLS = {'Spades': '♠', 'Hearts': '♥', 'Clubs': '♣', 'Diamonds': '♦'}
class Card:
    _next_id = 0
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
        if rank == 'X':
            self.value = SMALL_JOKER_VALUE
        elif rank == 'D':
            self.value = BIG_JOKER_VALUE
        else:
            self.value = RANK_VALUE[rank]
        self.id = Card._next_id
        Card._next_id += 1
    def is_joker(self):
        return self.rank in ('X', 'D')
    def display(self):
        if self.rank == 'X':
            return 'joker'
        if self.rank == 'D':
            return 'JOKER'
        return f"{SUIT_SYMBOLS.get(self.suit, '')}{self.rank}"
    def __repr__(self):
        return self.display()
    def __eq__(self, other):
        return isinstance(other, Card) and self.id == other.id
    def __hash__(self):
        return hash(self.id)
def create_deck():
    deck = []
    for rank in RANK_ORDER:
        for suit in SUITS:
            deck.append(Card(rank, suit))
    deck.append(Card('X'))
    deck.append(Card('D'))
    return deck
def sort_cards(cards):
    return sorted(cards, key=lambda c: (c.value, c.id))
def format_hand(cards):
    # display in a grid: indices on top, cards below
    ...