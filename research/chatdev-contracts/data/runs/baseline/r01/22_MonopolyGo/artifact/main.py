class ChanceCard:
    def __init__(self, description, effect):
        self.description = description
        self.effect = effect
class ChanceDeck:
    def __init__(self):
        self._cards = self._build()
        self._jail_free_card = next(c for c in self._cards if c.effect.get("type") == "jail_free")
        self._jail_free_in_play = False
        random.shuffle(self._cards)
    def _build(self):
        return [ ... 13 cards ... ]
    def draw(self):
        card = self._cards.pop(0)
        if card.effect.get("type") == "jail_free":
            self._jail_free_in_play = True  # held by a player; out of deck until used
        else:
            self._cards.append(card)  # cycle to bottom
        return card
    def return_jail_free(self):
        """Return the Get-Out-of-Jail-Free card to the bottom of the deck after a player uses it."""
        if self._jail_free_in_play:
            self._jail_free_in_play = False
            self._cards.append(self._jail_free_card)