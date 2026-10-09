class Card:
    RANKS = ['3','4','5','6','7','8','9','10','J','Q','K','A','2']
    RANK_VALUES = {'3':3, ..., '2':15}
    JOKERS: 'SJ' (small, 16), 'BJ' (big, 17)
    SUITS = ['♠','♥','♣','♦']
    def __init__(self, rank, suit=None)
    @property value
    def __lt__, __eq__, __repr__/__str__
    def to_dict / from_dict maybe not needed
class Deck:
    def __init__: build 54 cards
    def shuffle()
    def deal(): returns 17,17,17,3