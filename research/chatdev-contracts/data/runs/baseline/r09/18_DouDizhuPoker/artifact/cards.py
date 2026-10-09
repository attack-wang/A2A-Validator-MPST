'''
cards.py: Card and Deck definitions for Dou Dizhu.
'''
import random
class Card:
    """A single playing card; jokers use rank 'joker' with suit 'small'/'big'."""
    RANK_VALUES = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                   '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 15}
    SMALL_JOKER = 16
    BIG_JOKER = 17
    def __init__(self, rank, suit=None):
        """Build a card; for jokers pass rank='joker' and suit='small' or 'big'."""
        self.rank = rank
        self.suit = suit
        if rank == 'joker':
            self.value = Card.SMALL_JOKER if suit == 'small' else Card.BIG_JOKER
            self.joker_type = suit
        else:
            self.value = Card.RANK_VALUES[rank]
            self.joker_type = None
    @property
    def is_joker(self):
        """True when this card is a joker."""
        return self.rank == 'joker'
    def __repr__(self):
        """Human readable name such as '♠A', '小王' or '大王'."""
        if self.is_joker:
            return '小王' if self.joker_type == 'small' else '大王'
        return f"{self.suit}{self.rank}" if self.suit else self.rank
    def __eq__(self, other):
        """Cards are equal when value and suit match."""
        return isinstance(other, Card) and self.value == other.value and self.suit == other.suit
    def __hash__(self):
        """Hash by (value, suit) so cards can live in sets/dicts."""
        return hash((self.value, self.suit))
class Deck:
    """Standard 54-card Dou Dizhu deck: 3..2 in four suits plus two jokers."""
    def __init__(self):
        """Create the full 54-card deck."""
        self.cards = [Card(r, s) for r in Card.RANK_VALUES for s in ('♠', '♥', '♣', '♦')]
        self.cards.append(Card('joker', 'small'))
        self.cards.append(Card('joker', 'big'))
    def deal(self):
        """Shuffle, then split into three 17-card hands and 3 bottom cards."""
        random.shuffle(self.cards)
        hands = [self.cards[i * 17:(i + 1) * 17] for i in range(3)]
        bottom = self.cards[51:]
        return hands, bottom