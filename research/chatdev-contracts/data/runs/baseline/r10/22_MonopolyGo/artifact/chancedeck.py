class ChanceDeck:
    def __init__(self):
        self._all_cards = [ChanceCard(*c) for c in CHANCE_CARDS]
        self._available = list(self._all_cards)  # cards in circulation
        self._deck = []
        self._reshuffle()
    def _reshuffle(self):
        self._deck = list(self._available)
        random.shuffle(self._deck)
    def draw(self):
        if not self._deck:
            if not self._available:
                return None
            self._reshuffle()
        return self._deck.pop()
    def remove_from_circulation(self, card):
        """Remove a card from circulation (kept by a player, e.g., Get Out of Jail Free)."""
        if card in self._available:
            self._available.remove(card)
        # also remove from draw pile if present
        if card in self._deck:
            self._deck.remove(card)
    def return_to_circulation(self, card):
        """Return a card to circulation after a player uses it."""
        if card not in self._available:
            self._available.append(card)
    def restore_jail_free_card(self):
        """Return a Get Out of Jail Free card to circulation (e.g., holder went bankrupt)."""
        for card in self._all_cards:
            if card.effect == "get_out_of_jail" and card not in self._available:
                self._available.append(card)
                return True
        return False