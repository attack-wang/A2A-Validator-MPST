'''
card.py
Defines the Card class and deck utilities for Dou Dizhu.
'''
import random
# Rank symbols ordered from weakest to strongest.
RANK_ORDER = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'X', 'D']
RANK_VALUES = {rank: i + 3 for i, rank in enumerate(RANK_ORDER)}
# 3->3 ... A->14, 2->15, X(small joker)->16, D(big joker)->17
SUITS = ['♠', '♥', '♣', '♦']
class Card:
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
        self.value = RANK_VALUES[rank]
    def is_joker(self):
        return self.rank in ('X', 'D')
    def __repr__(self):
        return self.rank
    def __str__(self):
        if self.is_joker():
            return '小王' if self.rank == 'X' else '大王'  # hmm encoding
        return f"{self.rank}{self.suit}"