class Card:
    RANK_NAMES = {3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K',14:'A',15:'2',16:'joker',17:'JOKER'}
    SUITS = ['♠','♥','♣','♦']
    def __init__(self, rank, suit=None):
        self.rank = rank
        self.suit = suit
    def __lt__(self, other): return self.rank < other.rank
    def __eq__(self, other): return self.rank == other.rank and self.suit == other.suit
    def __hash__(self): return hash((self.rank, self.suit))
    def __repr__/__str__: return name