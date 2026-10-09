'''
constants.py
Shared ranking and combination-type constants for the Dou Dizhu game.
'''
RANK_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
RANK_VALUE = {r: i + 3 for i, r in enumerate(RANK_ORDER)}  # '3'->3 ... '2'->15
SMALL_JOKER_VALUE = 16
BIG_JOKER_VALUE = 17
MAX_STRAIGHT_VALUE = 14  # A; straights/airplanes may not include '2' or jokers
# Combination type identifiers
SINGLE = 'single'
PAIR = 'pair'
TRIO = 'trio'
TRIO_SINGLE = 'trio_single'
TRIO_PAIR = 'trio_pair'
STRAIGHT = 'straight'
PAIR_STRAIGHT = 'pair_straight'
AIRPLANE = 'airplane'
AIRPLANE_SINGLE = 'airplane_single'
AIRPLANE_PAIR = 'airplane_pair'
FOUR_TWO_SINGLES = 'four_two_singles'
FOUR_TWO_PAIRS = 'four_two_pairs'
BOMB = 'bomb'
ROCKET = 'rocket'