"""Constants and helper mappings for the Dou Dizhu game."""
from enum import Enum
RANKS = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'BlackJoker', 'RedJoker']
RANK_VALUE = {rank: idx + 3 for idx, rank in enumerate(RANKS)}  # 3..17
VALUE_RANK = {v: k for k, v in RANK_VALUE.items()}
MIN_STRAIGHT_VALUE = RANK_VALUE['3']   # 3
MAX_STRAIGHT_VALUE = RANK_VALUE['A']   # 14 (2 and jokers never run in sequences)
SUITS = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
SUIT_SYMBOLS = {'Spades': '♠', 'Hearts': '♥', 'Clubs': '♣', 'Diamonds': '♦'}
class CombType(Enum):
    INVALID = 0
    SINGLE = 1
    PAIR = 2
    TRIPLE = 3
    TRIPLE_ONE = 4
    TRIPLE_PAIR = 5
    STRAIGHT = 6
    PAIR_STRAIGHT = 7
    AIRPLANE = 8
    AIRPLANE_SINGLE = 9
    AIRPLANE_PAIR = 10
    FOUR_TWO = 11
    FOUR_TWO_PAIR = 12
    BOMB = 13
    ROCKET = 14