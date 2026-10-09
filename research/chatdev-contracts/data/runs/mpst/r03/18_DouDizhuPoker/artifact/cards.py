'''
cards.py
Card representation for Dou Dizhu.
...
'''
import random
SUIT_SYMBOLS = {'spades': '♠', 'hearts': '♥', 'diamonds': '♦', 'clubs': '♣'}
RANK_TO_VALUE = {
    '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 16,
}
VALUE_TO_NAME = {v: k for k, v in RANK_TO_VALUE.items()}
SMALL_JOKER = 18
BIG_JOKER = 19
class Card:
    def __init__(self, value, suit=None):
        self.value = value
        self.suit = suit  # None for jokers
        self.card_id = ...  # unique id for equality? Actually value+suit unique enough.
    ...