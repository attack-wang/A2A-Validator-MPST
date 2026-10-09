'''
deck.py
Deck creation, shuffling and dealing for Dou Dizhu.
A standard Dou Dizhu deck has 54 cards: 13 ranks x 4 suits + 2 jokers.
Dealing: 17 cards to each of the 3 players, 3 bottom cards go to the landlord.
'''
import random
from card import Card
from constants import RANK_ORDER
SUITS = ('♠', '♥', '♣', '♦')
def create_deck():
    """Build and return a shuffled list of 54 cards."""
    cards = []
    for rank in RANK_ORDER:
        for suit in SUITS:
            cards.append(Card(rank, suit))
    cards.append(Card('joker'))
    cards.append(Card('JOKER'))
    random.shuffle(cards)
    return cards
def deal(deck):
    """Deal the deck into three 17-card hands plus the 3-card bottom."""
    hands = [deck[0:17], deck[17:34], deck[34:51]]
    bottom = deck[51:54]
    return hands, bottom