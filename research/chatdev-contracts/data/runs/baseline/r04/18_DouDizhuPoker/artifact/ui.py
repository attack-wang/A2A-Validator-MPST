class Card:
    RANK_NAMES = {3:'3',4:'4',...,11:'J',12:'Q',13:'K',14:'A',15:'2',16:'joker(small)',17:'JOKER(big)'}
    SUITS = ['♠','♥','♣','♦']
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
    def __lt__, __eq__, __hash__, __repr__/__str__