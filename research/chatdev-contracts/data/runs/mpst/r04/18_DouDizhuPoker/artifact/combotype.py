'''
combotype.py
Enumeration of all valid Dou Dizhu combination types.
'''
from enum import Enum, auto
class ComboType(Enum):
    SINGLE = auto()
    PAIR = auto()
    TRIPLE = auto()
    TRIPLE_ONE = auto()      # triple + single kicker ("3+1")
    TRIPLE_PAIR = auto()     # triple + pair kicker ("3+2")
    STRAIGHT = auto()        # >= 5 consecutive single ranks (max rank <= A)
    PAIR_STRAIGHT = auto()   # >= 3 consecutive pairs
    AIRPLANE = auto()        # >= 2 consecutive triples, no wings
    AIRPLANE_SINGLE = auto() # airplane + same number of single wings
    AIRPLANE_PAIR = auto()   # airplane + same number of pair wings
    FOUR_TWO_SINGLE = auto() # bomb used as "4+2 singles"
    FOUR_TWO_PAIR = auto()   # "4+2 pairs"
    BOMB = auto()
    ROCKET = auto()          # both jokers
    INVALID = auto()