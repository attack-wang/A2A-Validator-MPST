class Deck:
    def __init__(self):
        self.cards = []
        self._build()
    def _build(self):
        self.cards = []
        for rank in range(RANK_3, RANK_2 + 1):  # 3..15
            for suit in SUITS:
                self.cards.append(Card(rank, suit))
        self.cards.append(Card(RANK_SMALL_JOKER))
        self.cards.append(Card(RANK_BIG_JOKER))
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self):
        """Shuffle and deal: returns (hands, bottom) where hands is a list of
        three 17-card lists and bottom is the 3-card list for the landlord."""
        self.shuffle()
        hands = [self.cards[i * 17:(i + 1) * 17] for i in range(3)]
        bottom = self.cards[51:54]
        for h in hands:
            h.sort()
        return hands, bottom