'''
Card module: defines the Card class used by the Dou Dizhu game.
'''
class Card:
    RANKS = ['3','4','5','6','7','8','9','10','J','Q','K','A','2','SJ','BJ']
    RANK_TO_VALUE = {'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13,'A':14,'2':15,'SJ':16,'BJ':17}
    def __init__(self, rank):
        if rank not in Card.RANK_TO_VALUE:
            raise ValueError('Invalid card rank: %r' % (rank,))
        self.rank = rank
        self.value = Card.RANK_TO_VALUE[rank]
    def __lt__(self, other):
        return self.value < other.value
    def __eq__(self, other):
        return isinstance(other, Card) and self.value == other.value
    def __hash__(self):
        return hash(self.value)
    def __repr__(self):
        return self.rank
    __str__ = __repr__