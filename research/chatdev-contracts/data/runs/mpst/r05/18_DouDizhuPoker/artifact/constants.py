'''
constants.py
Global constants and the CombinationType enumeration for the Dou Dizhu game.
Card value mapping (higher value = stronger card):
    3=3, 4=4, ..., 10=10, J=11, Q=12, K=13, A=14, 2=16,
    small joker=18, big joker=19.
The gap between 2 (16) and A (14) and between jokers makes it easy to
exclude 2s and jokers from straights (max straight value is ACE = 14).
'''
from enum import Enum
ACE = 14
SMALL_JOKER = 18
BIG_JOKER = 19
# Ranks that appear with four suits in the deck (jokers are added separately).
RANK_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
# Value of every rank, including the two jokers.
RANK_VALUES = {
    '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 16,
    'joker': SMALL_JOKER, 'JOKER': BIG_JOKER,
}
# Human readable names for display.
RANK_NAMES = {
    'joker': 'Small Joker',
    'JOKER': 'Big Joker',
}
class CombinationType(Enum):
    """All legal combination types in Dou Dizhu."""
    SINGLE = 'single'
    PAIR = 'pair'
    TRIPLE = 'triple'
    TRIPLE_SINGLE = 'triple_single'      # 3+1
    TRIPLE_PAIR = 'triple_pair'          # 3+2
    STRAIGHT = 'straight'                # >=5 consecutive singles (3..A)
    PAIR_STRAIGHT = 'pair_straight'      # >=3 consecutive pairs (3..A)
    AIRPLANE = 'airplane'                # >=2 consecutive triples (3..A)
    AIRPLANE_SINGLE_WINGS = 'airplane_single_wings'  # airplane + equal # of singles
    AIRPLANE_PAIR_WINGS = 'airplane_pair_wings'      # airplane + equal # of pairs
    FOUR_TWO_SINGLE = 'four_two_single'  # bomb-like four + 2 singles
    FOUR_TWO_PAIR = 'four_two_pair'      # four + 2 pairs
    BOMB = 'bomb'
    ROCKET = 'rocket'                    # both jokers
# Types whose "length" (number of sets) must match to compare against each other.
SEQUENCE_TYPES = {
    CombinationType.STRAIGHT,
    CombinationType.PAIR_STRAIGHT,
    CombinationType.AIRPLANE,
    CombinationType.AIRPLANE_SINGLE_WINGS,
    CombinationType.AIRPLANE_PAIR_WINGS,
}