class ChanceDeck:
    def __init__(self):
        self._cards = [...all cards...]
        random.shuffle
    def draw(self):
        card = self._cards.pop(0)
        if card.effect type != 'jail_free':
            self._cards.append(card)  # cycle back
        return card
    def restore(self, card):
        self._cards.append(card)