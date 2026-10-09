'''
player.py: Player and AIPlayer with bidding and play selection strategies.
'''
from itertools import combinations as iter_combinations
from combination import (Combination, SINGLE, PAIR, TRIO, TRIO_SINGLE, TRIO_PAIR,
                         STRAIGHT, PAIR_STRAIGHT, AIRPLANE, AIRPLANE_SINGLE,
                         AIRPLANE_PAIR, FOUR_TWO_SINGLES, FOUR_TWO_PAIRS, BOMB, ROCKET)
from identifier import identify_combination